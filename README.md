<div align="center">

<img src="assets/logo.jpg" alt="SPECTRE Logo" width="160" height="160" style="border-radius: 32px;" />

# SPECTRE
### High-Performance Discord Activity & Badge Virtualization Engine
*Created by [an1zy](https://github.com/an1zy)*

<p align="center">
  <b>English</b> · <a href="README.ru.md">Русский</a>
</p>

<p align="center">
  <a href="https://python.org"><img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://microsoft.com"><img src="https://img.shields.io/badge/Platform-Windows_10_%7C_11-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Platform"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-EBAF8E?style=for-the-badge" alt="License"></a>
  <a href="https://discord.com"><img src="https://img.shields.io/badge/Discord-API_v9-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Discord"></a>
</p>

```
  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗ ███████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝
  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝█████╗  
  ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══╝  
  ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║███████╗
  ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
```

<p align="center">
  <a href="https://github.com/an1zy/spectre-discord/releases/latest">
    <img src="https://img.shields.io/badge/DOWNLOAD_FOR_WINDOWS-spectre__windows__x64.exe-EBAF8E?style=for-the-badge&logo=windows&logoColor=141414" height="42" alt="Download for Windows">
  </a>
</p>

<p align="center">
  <b><a href="https://github.com/an1zy/spectre-discord/releases/latest">Go to Latest Release (.exe)</a></b><br/>
  <i>Portable standalone build. No terminal or Python installation required.</i>
</p>

</div>

---

## How It Works

Discord desktop scans local running processes via standard Windows APIs (`EnumProcesses` and `GetWindowTextW`) and compares them against its public verified games database (`https://discord.com/api/v9/applications/detectable`).

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

1. SPECTRE launches a 4 KB native binary (`dummy.exe`) configured with `WS_EX_TOOLWINDOW` and `WS_EX_NOACTIVATE`.
2. Windows handles it as an active game process, but it renders completely offscreen (-10000, -10000) with **zero taskbar icons, zero focus stealing, and 0% CPU footprint**.
3. Discord reads the process and registers activity without requiring accounts, tokens, or memory hacks.

---

## Installation

### Option 1: Standalone executable (recommended)

1. Open the **Discord desktop app**.
2. Download **[`spectre_windows_x64.exe`](https://github.com/an1zy/spectre-discord/releases/latest)** from the releases section.
3. Launch the file and choose your desired mode.

*(If Windows SmartScreen appears, click "More info" → "Run anyway". Open-source independent binaries do not carry costly commercial Microsoft signing certificates).*

### Option 2: Run via console / from source

If you prefer running from terminal or modifying the source code:

```bash
git clone https://github.com/an1zy/spectre-discord.git
cd spectre-discord

pip install -r requirements.txt
python main.py
```
*(Or double-click `start.bat`)*

To package into a single standalone `.exe`:
```bash
pip install pyinstaller
python build_exe.py
```

---

## Features

- **Game Variety badge:** Iterates through 10,400+ titles from Discord's official database in batches of 8 games for 15 seconds each (up to Mythic tier / 10,000 games).
- **Game Time multiplier:** Runs up to 20 lightweight dummy processes concurrently. Multiplies playtime by up to 20x (1 real hour = 20 hours recorded in Discord).
- **Humanizer mode:** Cycles between selected games and adds natural AFK breaks, simulating organic gameplay throughout the day.
- **Custom game titles (Forge):** Allows launching processes with arbitrary names (GTA VI, Half-Life 3, or any custom title).
- **Safe:** Requires no Discord token, no memory modification, and no client modifications. Discord naturally detects dummy Win32 processes through standard Windows handles.

---

## Menu Options

| Key | Mode | Description |
|:---:|:---|:---|
| `[1]` | **Variety Runner** | Cycles 10,400+ games in batches (8 games per 15s) |
| `[2]` | **Multiplier** | Up to 20 concurrent processes (multiplier up to 20x) |
| `[3]` | **Humanizer** | Natural play sessions with rotation and AFK breaks |
| `[4]` | **Game Forge** | Custom and unreleased title presence |
| `[5]` | **Single Spoof** | Search and run any single verified game |
| `[6]` | **Telemetry** | Badge stats and history logs |

---

## FAQ

#### Why is the badge not updating immediately?
The Discord desktop app captures the process in real time, but Discord servers recalculate profile badge tiers in batches every 2 to 24 hours. As long as your profile shows "Playing <Game>", the telemetry was recorded.

#### Is there a risk of a ban?
No. SPECTRE does not inject into Discord processes or intercept network packets. To Discord, it looks like normal software running in Windows.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
