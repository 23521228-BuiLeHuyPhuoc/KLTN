import json
import os
from pathlib import Path
import subprocess
import sys

from kiemchung.thu_llm import Extraction, evaluate, messages_for

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "data/thu_llm/cases.json").read_text())


def test_cases_are_development_examples_and_verbatim():
    source = (ROOT / "CHI_TIET_TUYEN_TINH_KHOA_LUAN.md").read_text()
    assert 5 <= len(CASES) <= 10
    assert len({c["id"] for c in CASES}) == len(CASES)
    for c in CASES:
        assert c["text"] in source
        assert c["expected"]["san_pham"] in {"iPhone 17", "Galaxy Buds3 Pro", "Apple Watch SE 3", "Xiaomi 15T"}
        Extraction.model_validate(c["expected"] | {"trich": {}, "mac_dinh": []})
        assert messages_for(c)[1]["content"] == c["text"]
        assert "expected" not in messages_for(c)[1]["content"]


def test_evaluator_detects_invented_omitted_and_wrong_conditions():
    case = CASES[0]
    data = case["expected"] | {"trich": {"san_pham": "not present"}, "mac_dinh": []}
    data["dieu_kien"] = {"moc_sac": "100%", "che_do_chong_on": "bat"}
    metrics = evaluate(json.dumps(data), case)
    assert metrics["schema_valid"]
    assert metrics["omitted_conditions"] == ["cong_suat_sac"]
    assert metrics["invented_conditions"] == ["che_do_chong_on"]
    assert metrics["wrong_conditions"] == ["moc_sac"]
    assert metrics["bad_quotes"] == ["san_pham"]
    assert "gia_tri" in metrics["missing_quotes"]


def test_invalid_schema_scores_no_fields():
    for output in ['{"gia_tri":20}', 'not json', '[]']:
        metrics = evaluate(output, CASES[0])
        assert not metrics["schema_valid"]
        assert not any(metrics["field_correct"].values())


def test_cli_offline_and_live_preflight(tmp_path):
    env = dict(os.environ, GEMINI_API_KEY="", GROQ_API_KEY="", GOOGLE_API_KEY="")
    base = [sys.executable, str(ROOT / "scripts/thu_llm.py"),
            "--cache-dir", str(tmp_path / "cache")]
    offline = subprocess.run(base + ["--mode", "offline", "--output", str(tmp_path / "offline")],
                             env=env, cwd=ROOT, capture_output=True, text=True)
    assert offline.returncode == 0, offline.stderr
    manifest = json.loads((tmp_path / "offline/manifest.json").read_text())
    assert len(manifest["source_sha256"]) == 5
    assert all(s["metrics"] is None and s["api_calls_successful"] == 0
               and s["cache_repeats"] == 10 for s in manifest["summaries"])
    live = subprocess.run(base + ["--mode", "live", "--output", str(tmp_path / "live")],
                          env=env, cwd=ROOT, capture_output=True, text=True)
    assert live.returncode == 2
    manifest = json.loads((tmp_path / "live/manifest.json").read_text())
    assert all(s["status"] == "blocked" and s["completed_samples"] == 0
               and any(r.startswith("missing_api_key") for r in s["reasons"])
               for s in manifest["summaries"])
    assert not (tmp_path / "live/calls.jsonl").exists()
