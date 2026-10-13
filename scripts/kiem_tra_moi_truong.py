"""Record the execution environment and smoke-test installed libraries; no secrets."""
from datetime import datetime, timezone
import importlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=15, cwd=ROOT)
        return {"exit_code": p.returncode, "stdout": p.stdout.strip()}
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return {"exit_code": None, "stdout": "unavailable"}


def main():
    assert sys.version_info >= (3, 10), "Python >= 3.10 required"
    assert sys.prefix != sys.base_prefix, "Run in a dedicated virtual environment"
    modules = ["rank_bm25", "pyvi", "pydantic", "yaml", "google.genai", "groq",
               "fastapi", "uvicorn", "pytest", "sklearn", "statsmodels.api",
               "pandas", "matplotlib", "playwright.sync_api", "dotenv", "kiemchung"]
    imports = {}
    for module in modules:
        importlib.import_module(module)
        imports[module] = "ok"
    from pyvi import ViTokenizer
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure()
    plt.close(fig)
    memory = {}
    if Path("/proc/meminfo").exists():
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, value = line.split(":", 1)
            if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
                memory[key + "_KiB"] = int(value.split()[0])
    disk = shutil.disk_usage(ROOT)
    hardware = command(["lspci", "-nn"])
    graphics = [line for line in hardware["stdout"].splitlines()
                if any(word in line for word in ["VGA", "3D controller", "Display controller"])]
    cpu_info = Path("/proc/cpuinfo").read_text() if Path("/proc/cpuinfo").exists() else ""
    cpu = next((line.split(":", 1)[1].strip() for line in cpu_info.splitlines()
                if line.startswith("model name")), platform.processor())
    limits = {}
    for name in ["memory.max", "cpu.max"]:
        p = Path("/sys/fs/cgroup") / name
        limits[name] = p.read_text().strip() if p.exists() else None
    packages = {d.metadata["Name"]: {"version": d.version,
                "requires_python": d.metadata.get("Requires-Python")} for d in metadata.distributions()}
    output = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Environment executing this script; ownership/personal-machine status not established",
        "os": platform.freedesktop_os_release() if Path("/etc/os-release").exists() else platform.system(),
        "kernel": platform.release(), "python": platform.python_version(),
        "python_executable": sys.executable, "virtualenv": sys.prefix,
        "cpu": cpu, "logical_cpus": os.cpu_count(),
        "cpu_affinity": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
        "memory": memory, "disk_bytes": {"total": disk.total, "used": disk.used, "free": disk.free},
        "graphics": graphics, "nvidia": command(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"]),
        "virtualization": command(["systemd-detect-virt"]), "cgroup_limits": limits,
        "packages": packages, "imports": imports,
        "pyvi_example": ViTokenizer.tokenize("Điện thoại có thời lượng pin tốt"),
        "pip_check": command([sys.executable, "-m", "pip", "check"]),
    }
    out = ROOT / "ket_qua/thu_llm/environment.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(out), "imports_ok": len(imports),
                      "python": output["python"], "pip_check": output["pip_check"]}, ensure_ascii=False))
    return output["pip_check"]["exit_code"] or 0


if __name__ == "__main__":
    raise SystemExit(main())
