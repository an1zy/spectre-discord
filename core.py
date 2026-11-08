import os
import sys
import json
import time
import shutil
import urllib.request
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple

if getattr(sys, "frozen", False):
    SCRIPT_DIR = Path(sys._MEIPASS)
else:
    SCRIPT_DIR = Path(__file__).resolve().parent
DUMMY_CS_PATH = SCRIPT_DIR / "dummy.cs"
DUMMY_EXE_PATH = SCRIPT_DIR / "dummy.exe"
CACHE_PATH = SCRIPT_DIR / "games_cache.json"
HISTORY_PATH = SCRIPT_DIR / "history.json"
TEMP_DIR = Path(os.environ.get("TEMP", ".")) / "spectre_engine_temp"

DISCORD_API_URL = "https://discord.com/api/v9/applications/detectable"
CACHE_TTL = 12 * 3600  # 12 hours
ESRB_ADULTS_ONLY = 5

FORGE_PRESETS = [
    {"name": "Grand Theft Auto VI (Dev Playtest)", "exe": "gta6_alpha.exe"},
    {"name": "Half-Life 3 (Closed Alpha)", "exe": "hl3.exe"},
    {"name": "Bloodborne PC Remaster", "exe": "bloodborne.exe"},
    {"name": "Hollow Knight: Silksong (Review Build)", "exe": "silksong.exe"},
    {"name": "S.T.A.L.K.E.R. 2 (Internal QA)", "exe": "stalker2_qa.exe"},
    {"name": "The Elder Scrolls VI (Pre-Production)", "exe": "tes6.exe"}
]


def is_discord_running() -> bool:
    try:
        out = subprocess.check_output(["tasklist"], text=True, errors="ignore")
        return "discord.exe" in out.lower()
    except Exception:
        return False


def ensure_dummy_executable() -> Path:
    if DUMMY_EXE_PATH.exists() and DUMMY_EXE_PATH.stat().st_size > 0:
        return DUMMY_EXE_PATH

    csc_path = Path(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe")
    if not csc_path.exists():
        csc_path = Path(r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe")

    if not csc_path.exists():
        raise RuntimeError("Windows .NET csc.exe compiler not found")

    if not DUMMY_CS_PATH.exists():
        raise RuntimeError(f"Missing {DUMMY_CS_PATH}")

    cmd = [
        str(csc_path),
        "/target:winexe",
        "/optimize+",
        f"/out:{DUMMY_EXE_PATH}",
        str(DUMMY_CS_PATH)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Compilation error:\n{res.stderr}\n{res.stdout}")

    return DUMMY_EXE_PATH


def is_adult_game(app: Dict[str, Any]) -> bool:
    themes = app.get("themes") or []
    for t in themes:
        if isinstance(t, str) and t.lower() == "erotic":
            return True
    classification = app.get("content_classification") or {}
    esrb = classification.get("esrb") or {}
    return esrb.get("code") == ESRB_ADULTS_ONLY


def sanitize_rel_path(raw_name: str) -> Optional[str]:
    if not raw_name:
        return None
    cleaned = raw_name.strip().lstrip('>').strip()
    if not cleaned:
        return None
    cleaned = cleaned.replace('/', '\\')
    if not cleaned.lower().endswith('.exe'):
        cleaned += '.exe'
    return cleaned


def fetch_games(force_refresh: bool = False) -> List[Dict[str, Any]]:
    if not force_refresh and CACHE_PATH.exists():
        try:
            mtime = CACHE_PATH.stat().st_mtime
            if (time.time() - mtime) < CACHE_TTL:
                with open(CACHE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
        except Exception:
            pass

    req = urllib.request.Request(
        DISCORD_API_URL,
        headers={"User-Agent": "spectre-discord-agent/2.4"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw_apps = json.loads(resp.read().decode("utf-8"))

    processed_games = []
    for app in raw_apps:
        app_id = str(app.get("id", ""))
        name = app.get("name", "").strip()
        if not name:
            continue
        
        executables = app.get("executables") or []
        win_candidates = [e for e in executables if (e.get("os") or "").lower() == "win32"]
        if not win_candidates:
            continue

        best = next((e for e in win_candidates if not e.get("is_launcher")), win_candidates[0])
        rel_path = sanitize_rel_path(best.get("name", ""))
        if not rel_path:
            continue

        processed_games.append({
            "id": app_id,
            "name": name,
            "exe": rel_path,
            "adult": is_adult_game(app),
            "args": best.get("arguments")
        })

    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(processed_games, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return processed_games


class HistoryManager:
    def __init__(self, file_path: Path = HISTORY_PATH):
        self.file_path = file_path
        self.data: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        if not self.file_path.exists():
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, list):
                    return {str(gid): {"name": "", "timestamp": int(time.time())} for gid in content}
                elif isinstance(content, dict):
                    return content
                return {}
        except Exception:
            return {}

    def is_boosted(self, game_id: str) -> bool:
        return str(game_id) in self.data

    def mark_boosted(self, game_id: str, game_name: str):
        self.data[str(game_id)] = {
            "name": game_name,
            "timestamp": int(time.time())
        }

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERR] Failed saving history: {e}")

    def total_count(self) -> int:
        return len(self.data)

    def clear(self):
        self.data = {}
        self.save()


class SpooferRunner:
    def __init__(self):
        self.dummy_exe = ensure_dummy_executable()
        self.temp_root = TEMP_DIR
        self.active_processes: List[Tuple[subprocess.Popen, Path]] = []
        self._init_temp()

    def _init_temp(self):
        self.cleanup_temp()
        os.makedirs(self.temp_root, exist_ok=True)

    def cleanup_temp(self):
        for p, _ in self.active_processes:
            try:
                p.terminate()
                p.wait(timeout=0.8)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        self.active_processes.clear()

        if self.temp_root.exists():
            try:
                shutil.rmtree(self.temp_root, ignore_errors=True)
            except Exception:
                pass

    def launch_game(self, game: Dict[str, Any]) -> Optional[subprocess.Popen]:
        rel_path = game["exe"]
        target_path = self.temp_root / rel_path
        
        os.makedirs(target_path.parent, exist_ok=True)

        if not target_path.exists():
            try:
                os.link(str(self.dummy_exe), str(target_path))
            except Exception:
                try:
                    shutil.copy2(str(self.dummy_exe), str(target_path))
                except Exception:
                    return None

        cmd = [str(target_path), game["name"]]
        if game.get("args"):
            cmd.extend(game["args"].split())

        try:
            p = subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            self.active_processes.append((p, target_path))
            return p
        except Exception:
            return None

    def launch_custom(self, title: str, exe_filename: str) -> Optional[subprocess.Popen]:
        if not exe_filename.lower().endswith(".exe"):
            exe_filename += ".exe"
        target_path = self.temp_root / exe_filename
        os.makedirs(target_path.parent, exist_ok=True)

        if not target_path.exists():
            try:
                os.link(str(self.dummy_exe), str(target_path))
            except Exception:
                shutil.copy2(str(self.dummy_exe), str(target_path))

        cmd = [str(target_path), title]
        try:
            p = subprocess.Popen(
                cmd,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )
            self.active_processes.append((p, target_path))
            return p
        except Exception:
            return None

    def kill_batch(self):
        for p, path in self.active_processes:
            try:
                p.terminate()
                p.wait(timeout=0.8)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
            try:
                if path.exists():
                    path.unlink(missing_ok=True)
            except Exception:
                pass
        self.active_processes.clear()
