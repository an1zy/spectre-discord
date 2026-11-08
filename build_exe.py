import os
import sys
import subprocess
from pathlib import Path

def build():
    root = Path(__file__).resolve().parent
    dummy_exe = root / "dummy.exe"
    cache_json = root / "games_cache.json"

    if not dummy_exe.exists():
        from core import ensure_dummy_executable
        ensure_dummy_executable()

    if not cache_json.exists():
        from core import fetch_games
        fetch_games()

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        "spectre",
        "--add-data",
        f"{dummy_exe};.",
        "--add-data",
        f"{cache_json};.",
        "main.py"
    ]

    print("Executing build command:", " ".join(cmd))
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print("\n[✓] Binary successfully built at: dist/spectre.exe")
    else:
        print("\n[!] Build failed with exit code:", res.returncode)

if __name__ == "__main__":
    build()
