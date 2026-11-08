<div align="center">

# SPECTRE
### High-Performance Discord Activity & Badge Virtualization Engine
*Created by [an1zy](https://github.com/an1zy)*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows_10%20%7C%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Discord](https://img.shields.io/badge/Discord-Detectable_API_v9-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com)

<br/>

<a href="https://github.com/an1zy/spectre-discord/releases/latest">
  <img src="https://img.shields.io/badge/СКАЧАТЬ%20ДЛЯ%20WINDOWS%20(.EXE)-EBAF8E?style=for-the-badge&logo=windows&logoColor=141414" height="42" alt="Скачать для Windows" />
</a>

<p>
  <b><a href="https://github.com/an1zy/spectre-discord/releases/latest">👉 Перейти к последней версии (Releases)</a></b><br/>
  <i>Терминал и Python не нужны. Скачал, запустил — работает.</i>
</p>

<p>
  <b><a href="#-english">English</a></b> · <b><a href="#-русская-версия">Русский</a></b>
</p>

</div>

---

## ⚡ Быстрый старт (Терминал не нужен)

Для обычных пользователей доступна готовая сборка:

| Система | Файл | Описание |
| :--- | :--- | :--- |
| **Windows 10 / 11** | **[`spectre_windows_x64.exe`](https://github.com/an1zy/spectre-discord/releases/latest)** | **Portable-версия:** скачал и запустил, установка не требуется |

1. Откройте приложение **Discord для ПК**.
2. Скачайте **`spectre_windows_x64.exe`** со страницы релизов.
3. Запустите файл и выберите нужный режим.
*(Если Windows покажет предупреждение SmartScreen — нажмите «Подробнее» → «Выполнить в любом случае», так как у инди-утилит нет платного цифрового сертификата Microsoft).*

---

## 🛠 Возможности

- **🏆 Прокачка значка «Универсал»:** автоматический высокоскоростной батч-раннер по 10 400+ проверенным играм из базы Discord. Открывает значок вплоть до Мифического ранга (~10 000 игр).
- **⏱️ Множитель времени («Время в играх»):** запуск до 20 параллельных процессов. Умножает часы в **x20** раз (1 реальный час = 20 часов в статистику Discord).
- **🕶️ Режим Humanizer:** умный планировщик, имитирующий живого игрока со сменой игр и AFK-паузами. Полная естественность для друзей в сети.
- **🎮 Кузница игр (Game Forge):** запуск кастомных и невышедших тайтлов (*Grand Theft Auto VI Dev Alpha*, *Half-Life 3 Closed Alpha*, *Bloodborne PC* и др.).
- **🛡️ 100% безопасность:** не требует токена Discord, ничего не внедряет в память и не модифицирует клиент. Discord видит процессы естественным образом через стандартный Win32 API.

---

## 🧑‍💻 Для разработчиков (Запуск из исходников)

Если вы хотите вносить изменения в код или запускать проект напрямую через Python:

```bash
# Клонировать репозиторий
git clone https://github.com/an1zy/spectre-discord.git
cd spectre-discord

# Установить зависимости
pip install -r requirements.txt

# Запустить движок
python main.py
```
*(Или запустите `start.bat`)*

### Сборка своего .exe
```bash
pip install pyinstaller
python build_exe.py
```
Скомпилированный файл появится в `dist/spectre.exe`.

---

## ⚙️ Модули и горячие клавиши

| Клавиша | Модуль | Описание | Целевой значок |
|:---:|:---|:---|:---|
| `[1]` | **Универсал (Variety)** | Перебор 10 400+ игр батчами (по 8 шт. на 15 сек) | *«Универсал» (Mythic)* |
| `[2]` | **Множитель часов** | Параллельный запуск до 20 процессов (x20 буст) | *«Время в играх»* |
| `[3]` | **Имитация игрока** | Сессии с естественной сменой игр и AFK-паузами | *Органичный фарм* |
| `[4]` | **Кузница игр** | Запуск редких и невышедших тайтлов (GTA VI, HL3) | *Кастомный статус* |
| `[5]` | **Одиночный запуск** | Быстрый поиск и запуск любой игры из базы | *Статус активности* |
| `[6]` | **Статистика** | Аналитика, история сессий и сброс прогресса | *Телеметрия* |

---

## ❓ Частые вопросы (FAQ)

#### Почему значок в Discord обновляется не сразу?
Клиент Discord фиксирует активность моментально, но сервера Discord пересчитывают уровни значков **пакетно раз в 2–24 часа**, чтобы не перегружать базы данных профилей. Если в Discord отображается статус *«В игре: ...»* — активность засчитана.

#### Могут ли забанить?
Нет. SPECTRE не трогает память Discord, не перехватывает веб-сокеты и не использует приватные токены. Для Discord эти процессы неотличимы от реально установленных на компьютере игр.

---

<a id="-english"></a>

## 🌐 English

**SPECTRE** is a native Win32 game virtualization engine that boosts Discord profile badges (*Game Variety* and *Game Time*) with zero memory injection, no tokens, and a clean minimalist terminal interface.

### Download Portable
Download the standalone executable from **[GitHub Releases](https://github.com/an1zy/spectre-discord/releases/latest)**. No Python installation required.

---

## License

Distributed under the [MIT License](LICENSE).
