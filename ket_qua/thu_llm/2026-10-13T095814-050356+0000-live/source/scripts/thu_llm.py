"""Run from repo root after pip install -e .; --help lists offline/live modes."""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys
import time

from dotenv import load_dotenv

from kiemchung.llm import KEY_ENV, LLMClient, LLMError, canonical_json, redact, utc_now
from kiemchung.thu_llm import SCORE_FIELDS, evaluate, messages_for, mock_transport

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["offline", "live"], default="offline")
    parser.add_argument("--config", type=Path, default=ROOT / "data/thu_llm/models.json")
    parser.add_argument("--cases", type=Path, default=ROOT / "data/thu_llm/cases.json")
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "ket_qua/llm_cache")
    parser.add_argument("--model", action="append", help="Model ID to select; repeatable")
    parser.add_argument("--confirm-free-tier", action="store_true",
                        help="Use only after checking the actual account/project free tier")
    parser.add_argument("--output", type=Path,
                        help="New directory only; defaults to a timestamped run")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env", override=False, interpolate=False)
    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    for value in (cases, config):
        if redact(canonical_json(value)) != canonical_json(value):
            parser.error("Credentials must not occur in cases or model configuration.")
    candidates = [m for m in config["models"] if not args.model or m["model"] in args.model]
    if not candidates or (args.model and set(args.model) - {m["model"] for m in candidates}):
        parser.error("Unknown --model; edit the config first.")
    stamp = utc_now().replace(":", "").replace(".", "-")
    output = args.output or ROOT / "ket_qua/thu_llm" / f"{stamp}-{args.mode}"
    output.mkdir(parents=True, exist_ok=False)  # Never overwrite a previous run.
    (output / "cases.json").write_text(canonical_json(cases) + "\n", encoding="utf-8")
    (output / "config.json").write_text(canonical_json(config) + "\n", encoding="utf-8")
    def progress(message: str) -> None:
        print(message, file=sys.stderr, flush=True)

    progress(f"Bắt đầu {args.mode}. Kết quả: {output}")
    summaries, all_rows = [], []
    for candidate in candidates:
        provider, model = candidate["provider"], candidate["model"]
        client = LLMClient(args.cache_dir, output / "calls.jsonl",
                           timeout_s=config["timeout_s"], max_retries=config["max_retries"],
                           transport=mock_transport if args.mode == "offline" else None)
        summary = {"provider": provider, "model": model, "mode": args.mode,
                   "status": "mock_only" if args.mode == "offline" else "completed",
                   "samples": len(cases), "metrics": None}
        if args.mode == "live" and (not os.environ.get(KEY_ENV[provider]) or not args.confirm_free_tier):
            reasons = []
            if not os.environ.get(KEY_ENV[provider]):
                reasons.append(f"missing_api_key:{KEY_ENV[provider]}")
            if not args.confirm_free_tier:
                reasons.append("free_tier_not_confirmed")
            summary.update(status="blocked", reasons=reasons, completed_samples=0,
                           api_calls_successful=0, cache_repeats=0)
            summaries.append(summary)
            progress(f"{model}: bị chặn ({', '.join(reasons)})")
            continue
        for index, case in enumerate(cases, start=1):
            progress(f"{model} — câu {index}/{len(cases)} ({case['id']}): đang xử lý...")
            params = dict(config["parameters"], **candidate.get("parameters", {}))
            call_args = dict(provider=provider, model=model, messages=messages_for(case),
                             parameters=params, json_output=True)
            try:
                first = client.call(**call_args)
                # A fresh client verifies persistence, not merely an in-memory hit.
                second = LLMClient(client.cache_dir, client.log_path,
                                   transport=client.transport).call(**call_args)
                assert second.cache_hit and second.text == first.text
            except LLMError as exc:
                summary.update(status="blocked" if exc.code.startswith("missing_api_key")
                               else "failed", reason=exc.code)
                all_rows.append({"id": case["id"], "provider": provider, "model": model,
                                 "mode": args.mode, "error": exc.code})
                progress(f"{model}: lỗi {exc.code}")
                break  # Avoid repeating authentication, quota or model errors 10 times.
            row = {"id": case["id"], "provider": provider, "model": model,
                   "mode": args.mode, "first": asdict(first), "repeat": asdict(second),
                   "evaluation": evaluate(first.text, case) if args.mode == "live" else None}
            all_rows.append(row)
            progress(f"  Xong ({'cache' if first.cache_hit else args.mode}); kiểm tra cache OK.")
            if args.mode == "live" and not first.cache_hit:
                progress(f"  Chờ {config['interval_s']} giây theo cấu hình giới hạn tốc độ...")
                time.sleep(config["interval_s"])  # Small budget; account quotas still apply.
        rows = [r for r in all_rows if r["model"] == model and r["provider"] == provider
                and "first" in r]
        summary["completed_samples"] = len(rows)
        summary["api_calls_successful"] = sum(not r["first"]["cache_hit"] for r in rows) if args.mode == "live" else 0
        summary["cache_repeats"] = sum(r["repeat"]["cache_hit"] for r in rows)
        if rows:
            live_ms = [r["first"]["elapsed_ms"] for r in rows if not r["first"]["cache_hit"]]
            summary["median_api_ms" if args.mode == "live" else "median_mock_ms"] = statistics.median(live_ms) if live_ms else None
            summary["median_cache_ms"] = statistics.median(r["repeat"]["elapsed_ms"] for r in rows)
            if args.mode == "live":
                summary["metrics"] = {
                    "evaluated_samples": len(rows),
                    "schema_valid": sum(r["evaluation"]["schema_valid"] for r in rows),
                    "field_correct": {f: sum(r["evaluation"]["field_correct"][f] for r in rows)
                                      for f in SCORE_FIELDS},
                    "field_total": len(rows) * len(SCORE_FIELDS),
                    "condition_errors_on_valid_outputs": {
                        k: sum(len(r["evaluation"][k] or []) for r in rows)
                        for k in ["omitted_conditions", "invented_conditions", "wrong_conditions"]},
                }
        summaries.append(summary)
        # Save completed models immediately, so a later interruption loses less work.
        (output / "results.jsonl").write_text(
            "".join(canonical_json(r) + "\n" for r in all_rows), encoding="utf-8")
    source_paths = [args.cases, args.config, ROOT / "src/kiemchung/llm.py",
                    ROOT / "src/kiemchung/thu_llm.py", Path(__file__)]
    for path in source_paths[2:]:
        destination = output / "source" / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    manifest = {"timestamp": utc_now(), "mode": args.mode, "summaries": summaries,
                "quota_account": "user_confirmed_free_tier_not_verified_by_script" if args.confirm_free_tier else "unverified",
                "git_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "source_sha256": {str(p.resolve().relative_to(ROOT)) if p.resolve().is_relative_to(ROOT) else str(p):
                                  hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
                "prompt_sha256": hashlib.sha256(canonical_json(messages_for(cases[0])[:1]).encode()).hexdigest()}
    (output / "manifest.json").write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "summaries": summaries}, ensure_ascii=False, indent=2))
    return 2 if any(s["status"] in {"blocked", "failed"} for s in summaries) else 0


if __name__ == "__main__":
    raise SystemExit(main())
