<div align="center">

# SPECTRE
### High-Performance Discord Activity & Badge Virtualization Engine
*Created by [an1zy](https://github.com/an1zy)*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows_10%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Detectable_API_v9-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com)
[![Interface](https://img.shields.io/badge/TUI-Rich_15.0-magenta?style=for-the-badge)](https://github.com/Textualize/rich)

<p>
  <b>[English](README.md)</b> · <b><a href="#-русская-версия">Русский</a></b>
</p>

```
  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗ ███████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝
  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝█████╗  
  ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══╝  
  ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║███████╗
  ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
```
*A lightweight, native Win32 virtualization tool that boosts Discord profile badges ("Game Variety" and "Game Time") with zero memory injection, no user tokens, and clean terminal telemetry.*

</div>

---

## Highlights

- **Game Variety Booster ("Универсал"):** High-throughput automated batching through 10,400+ verified titles from Discord's official database. Unlocks the Mythic tier badge (~10,000 games).
- **Time Multiplier ("Время в играх"):** Runs up to 20 concurrent native Win32 dummy processes. Multiplies farmed hours by **x20** (1 real-world hour = 20 hours recorded in Discord profile).
- **Organic Humanizer:** Natural play session scheduler that rotates between select games and inserts realistic AFK pauses. Simulates authentic gamer activity without raising suspicion among friends.
- **Custom Game Forge:** Spawn custom presence states with arbitrary titles (*"Grand Theft Auto VI (Dev Playtest)"*, *"Half-Life 3 (Closed Alpha)"*, etc.) directly into Windows process tables.
- **100% Non-Invasive & Safe:** Does not touch Discord's memory, requires no Discord token, and installs no modified clients. Discord detects dummy processes naturally via standard OS handles.

---

## How It Works

Discord's desktop client regularly scans the OS process table using standard Windows Win32 APIs (`EnumProcesses` and `GetWindowTextW`) and compares active executables against its public database (`https://discord.com/api/v9/applications/detectable`).

```
┌────────────────────────┐         ┌────────────────────────┐
│     SPECTRE Engine     │         │     Discord Client     │
└───────────┬────────────┘         └───────────┬────────────┘
            │                                  │
    Spawns micro-dummy                         │
    (WS_EX_TOOLWINDOW)                         │
            │                                  │
            ▼                                  │
┌────────────────────────┐                     │
│  Target Win32 Process  │ ◄─────── Scans OS process table
│   (e.g., cs2.exe)      │          & window handles
└────────────────────────┘                     │
                                               ▼
                                   ┌────────────────────────┐
                                   │  Sends telemetry to    │
                                   │  Discord backend       │
                                   └────────────────────────┘
```

1. SPECTRE creates a micro-binary (`dummy.exe`, 4.5 KB) compiled with `WS_EX_TOOLWINDOW` and `WS_EX_NOACTIVATE`.
2. Windows treats it as a native process, but it renders offscreen (-10000, -10000) with **zero taskbar presence, zero focus stealing, and negligible CPU usage (<0.01%)**.
3. Discord reads the process name and window title, logging verified game activity.

---

## Quick Start

### Prerequisites
- **Windows 10 / 11**
- **Python 3.8+**
- **Discord Desktop App** (web versions cannot inspect local processes)

### Installation
```bash
git clone https://github.com/your-username/spectre-discord.git
cd spectre-discord

# Install rich terminal library
pip install -r requirements.txt

# Run the engine
python main.py
```
*(Or simply double-click `start.bat` on Windows)*

---

## Packaging into Standalone Executable (.exe)

You can compile SPECTRE into a single standalone `.exe` without needing Python installed on the target machine:

```bash
pip install pyinstaller
python build_exe.py
```
The compiled binary will be placed at `dist/spectre.exe`.

---

## Modules Overview

| Key | Module | Description | Badge Target |
|:---:|:---|:---|:---|
| `[1]` | **VARIETY RUNNER** | Cycles 10,400+ games in configurable batches (8 per 15s) | *Game Variety (Mythic)* |
| `[2]` | **MULTIPLIER** | Runs up to 20 concurrent processes in parallel (x20 boost) | *Game Time* |
| `[3]` | **HUMANIZER** | Organic session manager with dynamic game switches & AFK | *Stealth Realism* |
| `[4]` | **GAME FORGE** | Spawns unreleased titles (GTA VI, Half-Life 3, Silksong) | *Custom Status* |
| `[5]` | **SINGLE SPOOF** | Instant search and launch for any single verified game | *Activity Status* |
| `[6]` | **TELEMETRY** | View database stats, history logs, and progress metrics | *Analytics* |

---

## FAQ

#### Why doesn't my badge update immediately in Discord?
Discord's desktop client registers the game in real-time, but Discord backend servers process badge levels **in asynchronous batch jobs (every 2 to 24 hours)** to prevent server overload. As long as your Discord profile displays *"Playing <Game>"* while SPECTRE runs, your activity is verified.

#### Can I get banned?
No. SPECTRE does not inject into Discord's memory space, does not intercept web sockets, and uses no private API tokens. To Discord, it is indistinguishable from running legitimate executables on Windows.

---

<a id="-русская-версия"></a>

## 🇷🇺 Русская версия

**SPECTRE** — это инструмент для прокачки значков профиля Discord («Универсал» и «Время в играх») через нативную виртуализацию Win32 процессов.

### Возможности
- 🏆 **Значок «Универсал»:** Автоматический батч-прогон по 10 400+ официальным играм Discord.
- ⏱️ **Значок «Время в играх»:** Мультипликатор часов до x20 (1 реальный час = 20 часов в Discord).
- 🎮 **Humanizer:** Имитация живого игрока со сменой игр и AFK-перерывами для полной естественности.
- 🛠 **Game Forge:** Запуск фейковых статусов невышедших игр (GTA VI, Half-Life 3 и др.).
- 🛡 **100% безопасность:** Без инъекций в память, без токенов, клиент Discord не модифицируется.

### Запуск
```bash
pip install -r requirements.txt
python main.py
```
или запустите `start.bat`.

---

## License

Distributed under the [MIT License](LICENSE).
