<div align="center">

# SPECTRE
by [an1zy](https://github.com/an1zy)

<p>
  <b>English</b> · <a href="README.ru.md">Русский</a>
</p>

[![Platform](https://img.shields.io/badge/Platform-Windows_10%20%7C%2011-0078D6?style=flat-square&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-EBAF8E?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-white?style=flat-square&logo=python&logoColor=141414)](https://python.org)

<br/>

<a href="https://github.com/an1zy/spectre-discord/releases/latest">
  <img src="https://img.shields.io/badge/DOWNLOAD%20FOR%20WINDOWS%20(.EXE)-EBAF8E?style=for-the-badge&logo=windows&logoColor=141414" height="40" alt="Download" />
</a>

<p>
  <b><a href="https://github.com/an1zy/spectre-discord/releases/latest">Latest Release (.exe)</a></b><br/>
  Portable build. Download and run, no terminal or Python setup needed.
</p>

</div>

---

## Installation

### Option 1: Standalone file (recommended)

1. Open your **Discord desktop app**.
2. Download **[`spectre_windows_x64.exe`](https://github.com/an1zy/spectre-discord/releases/latest)** from the releases page.
3. Run the executable and choose your mode.

*(If Windows SmartScreen appears, click "More info" → "Run anyway", as open-source indie tools do not carry paid Microsoft signing certificates).*

### Option 2: Run via console / from source

If you prefer running directly from terminal or editing the code:

```bash
git clone https://github.com/an1zy/spectre-discord.git
cd spectre-discord

pip install -r requirements.txt
python main.py
```
*(Or double-click `start.bat`)*

To compile your own single executable:
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
