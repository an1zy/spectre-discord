import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import time
import random
from pathlib import Path
from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.layout import Layout
from rich import box

from core import (
    is_discord_running,
    fetch_games,
    HistoryManager,
    SpooferRunner,
    FORGE_PRESETS
)
from ui import (
    clear,
    console,
    make_header_panel,
    make_menu_table,
    make_batch_table,
    make_multiplier_table,
    COLOR_ACCENT,
    COLOR_WHITE,
    COLOR_MUTED,
    COLOR_DIM,
    COLOR_BORDER
)

POPULAR_GAMES_PRESET = [
    "Counter-Strike 2",
    "Dota 2",
    "Grand Theft Auto V",
    "Cyberpunk 2077",
    "The Witcher 3: Wild Hunt",
    "Baldur's Gate 3",
    "Rust",
    "Apex Legends",
    "Team Fortress 2",
    "Terraria",
    "Tom Clancy's Rainbow Six Siege",
    "Garry's Mod",
    "Wallpaper Engine",
    "ELDEN RING",
    "Warframe",
    "Destiny 2",
    "Stardew Valley",
    "Dead by Daylight",
    "Payday 2",
    "Left 4 Dead 2"
]


def run_variety_mode(games: List[Dict[str, Any]], history: HistoryManager):
    clear()
    console.print(Panel(
        f"[bold {COLOR_WHITE}]Прокачка значка «Универсал»[/]\n"
        f"[{COLOR_MUTED}]Автоматический перебор официальной базы игр батчами[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    if not is_discord_running():
        console.print(f"[{COLOR_ACCENT}]Предупреждение:[/] [{COLOR_MUTED}]Приложение Discord не запущено. Запустите Discord, чтобы засчитывались игры.[/]")
        if not Confirm.ask("Продолжить?", default=True):
            return

    unboosted = [g for g in games if not history.is_boosted(g["id"])]
    console.print(f"Осталось в очереди: [bold {COLOR_WHITE}]{len(unboosted):,}[/] игр")

    if Confirm.ask("Исключить игры 18+ (Erotic / Adults Only)?", default=True):
        unboosted = [g for g in unboosted if not g["adult"]]
        console.print(f"Игр к прогону: [bold {COLOR_WHITE}]{len(unboosted):,}[/]")

    if not unboosted:
        console.print(f"\n[{COLOR_ACCENT}]Все доступные игры из базы уже пройдены.[/]")
        Prompt.ask("\nНажмите Enter для возврата")
        return

    batch_size = int(Prompt.ask("Игр в одном батче", default="8"))
    duration = int(Prompt.ask("Секунд на один батч", default="15"))

    total_to_boost = len(unboosted)
    total_batches = (total_to_boost + batch_size - 1) // batch_size
    est_total_sec = total_batches * duration

    console.print(f"\n[{COLOR_MUTED}]Батчей: {total_batches:,} │ По {batch_size} шт. │ Задержка {duration}с │ Расчетное время: ~{est_total_sec // 3600} ч {(est_total_sec % 3600) // 60} мин[/]")
    Prompt.ask(f"\nНажмите [{COLOR_ACCENT}]Enter[/] для старта")

    runner = SpooferRunner()
    current_index = 0
    start_time = time.time()

    progress = Progress(
        SpinnerColumn(style=COLOR_ACCENT),
        TextColumn(f"[bold {COLOR_WHITE}]{{task.description}}"),
        BarColumn(bar_width=25, style=COLOR_DIM, complete_style=COLOR_ACCENT),
        TextColumn(f"[{COLOR_ACCENT}]{{task.percentage:>3.1f}}%"),
        TextColumn(f"[{COLOR_MUTED}]•[/]"),
        TextColumn(f"[{COLOR_WHITE}]{{task.completed}}/{{task.total}}[/]"),
        TextColumn(f"[{COLOR_MUTED}]•[/]"),
        TimeRemainingColumn(),
        console=console
    )

    task_id = progress.add_task("Общий прогресс", total=total_to_boost)

    try:
        for batch_num in range(1, total_batches + 1):
            batch_games = unboosted[current_index : current_index + batch_size]
            if not batch_games:
                break

            clear()
            elapsed = int(time.time() - start_time)
            speed = (current_index / (elapsed / 60)) if elapsed > 10 else 0.0

            stats_panel = Panel(
                f"Батч [{COLOR_WHITE}]{batch_num}/{total_batches}[/] │ "
                f"Время: [{COLOR_WHITE}]{elapsed // 60:02d}:{elapsed % 60:02d}[/] │ "
                f"Скорость: [{COLOR_ACCENT}]{speed:.1f} игр/мин[/] │ "
                f"[{COLOR_DIM}]Ctrl+C для паузы[/]",
                border_style=COLOR_BORDER,
                box=box.ROUNDED
            )
            console.print(stats_panel)
            console.print(progress)

            for g in batch_games:
                runner.launch_game(g)

            batch_table = make_batch_table(batch_games, batch_num, total_batches)
            console.print(batch_table)

            for _ in range(duration * 10):
                time.sleep(0.1)

            runner.kill_batch()
            for g in batch_games:
                history.mark_boosted(g["id"], g["name"])
            history.save()

            current_index += len(batch_games)
            progress.update(task_id, advance=len(batch_games))

        console.print(f"\n[bold {COLOR_ACCENT}]Сессия успешно завершена.[/]")
    except KeyboardInterrupt:
        console.print(f"\n\n[{COLOR_MUTED}]Остановка по запросу. Прогресс сохранен.[/]")
    finally:
        runner.cleanup_temp()
        history.save()
        console.print(f"[{COLOR_MUTED}]Процессы завершены, файлы очищены.[/]")
        Prompt.ask("\nНажмите Enter для возврата")


def run_hour_farm_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel(
        f"[bold {COLOR_WHITE}]Фарм «Времени в играх»[/]\n"
        f"[{COLOR_MUTED}]Параллельный запуск процессов для умножения часов[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    if not is_discord_running():
        console.print(f"[{COLOR_ACCENT}]Предупреждение:[/] Discord не запущен.")

    console.print(f"  [{COLOR_ACCENT}]1[/] Топ-20 популярных игр (Множитель 20x: 1 час = 20 часов в Discord)")
    console.print(f"  [{COLOR_ACCENT}]2[/] Топ-10 популярных игр (Множитель 10x)")
    console.print(f"  [{COLOR_ACCENT}]3[/] Выбрать свои игры вручную")

    ch = Prompt.ask("\nВыбор", choices=["1", "2", "3"], default="1", show_choices=False, show_default=False)

    selected = []
    if ch == "2":
        target = POPULAR_GAMES_PRESET[:10]
    elif ch == "3":
        console.print(f"\n[{COLOR_MUTED}]Введите названия игр (пустой Enter для старта):[/]")
        while len(selected) < 20:
            q = Prompt.ask(f"Игра #{len(selected)+1}").strip()
            if not q:
                break
            match = next((g for g in games if q.lower() in g["name"].lower()), None)
            if match and match not in selected:
                selected.append(match)
                console.print(f"  [{COLOR_ACCENT}]+[/] {match['name']}")
            else:
                console.print(f"  [{COLOR_DIM}]Не найдено или уже в списке[/]")
        target = [g["name"] for g in selected]
    else:
        target = POPULAR_GAMES_PRESET

    if not selected:
        for t in target:
            m = next((g for g in games if g["name"].lower() == t.lower()), None)
            if m:
                selected.append(m)

    clear()
    mult = len(selected)
    mult_table = make_multiplier_table(selected)

    runner = SpooferRunner()
    for g in selected:
        runner.launch_game(g)

    start_time = time.time()
    try:
        with Live(console=console, refresh_per_second=2) as live:
            while True:
                elapsed = int(time.time() - start_time)
                h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
                farmed_hours = (elapsed * mult) / 3600.0

                live_panel = Panel(
                    f"Реальное время: [bold {COLOR_WHITE}]{h:02d}:{m:02d}:{s:02d}[/]   │   "
                    f"Засчитано в Discord: [bold {COLOR_ACCENT}]{farmed_hours:5.2f} ч[/]   │   "
                    f"Множитель: [bold {COLOR_WHITE}]{mult}x[/]\n"
                    f"[{COLOR_MUTED}]Процессы активны в фоне. Нажмите Ctrl+C для остановки.[/]",
                    border_style=COLOR_BORDER,
                    box=box.ROUNDED
                )

                layout = Layout()
                layout.split_column(
                    Layout(live_panel, size=5),
                    Layout(mult_table)
                )
                live.update(layout)
                time.sleep(0.5)

    except KeyboardInterrupt:
        console.print(f"\n\n[{COLOR_MUTED}]Остановка фарма часов...[/]")
    finally:
        runner.cleanup_temp()
        console.print(f"[{COLOR_MUTED}]Все процессы закрыты.[/]")
        Prompt.ask("\nНажмите Enter для возврата")


def run_humanizer_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel(
        f"[bold {COLOR_WHITE}]Имитация живого игрока (Humanizer)[/]\n"
        f"[{COLOR_MUTED}]Естественные игровые сессии со сменой игр и AFK-паузами[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    console.print(f"  [{COLOR_ACCENT}]1[/] Реалистичный режим (сессии 30-50 мин + перерыв 5-10 мин)")
    console.print(f"  [{COLOR_ACCENT}]2[/] Ускоренный / Демо (сессии 2-4 мин + перерыв 30 сек)")

    mode = Prompt.ask("\nРежим", choices=["1", "2"], default="1", show_choices=False, show_default=False)
    is_demo = (mode == "2")
    sess_min, sess_max = (120, 240) if is_demo else (1800, 3000)
    afk_min, afk_max = (20, 45) if is_demo else (300, 600)

    pool = [g for g in games if g["name"] in POPULAR_GAMES_PRESET[:6]]
    if not pool:
        pool = games[:4]

    clear()
    runner = SpooferRunner()
    session_num = 1

    try:
        while True:
            active_game = random.choice(pool)
            duration = random.randint(sess_min, sess_max)

            runner.cleanup_temp()
            runner.launch_game(active_game)

            start = time.time()
            with Live(console=console, refresh_per_second=2) as live:
                while time.time() - start < duration:
                    rem = int(duration - (time.time() - start))
                    el = int(time.time() - start)
                    live_box = Panel(
                        f"[{COLOR_ACCENT}]● В игре:[/] [bold {COLOR_WHITE}]{active_game['name']}[/]\n"
                        f"[{COLOR_MUTED}]Процесс: {active_game['exe']}[/]\n\n"
                        f"Текущая сессия : [bold {COLOR_WHITE}]{el // 60:02d}:{el % 60:02d}[/] / [{COLOR_MUTED}]{duration // 60:02d}:{duration % 60:02d}[/]\n"
                        f"До смены игры  : [{COLOR_ACCENT}]{rem // 60:02d}:{rem % 60:02d}[/]\n\n"
                        f"[{COLOR_DIM}]Сессия #{session_num} │ Ctrl+C для выхода[/]",
                        border_style=COLOR_BORDER,
                        box=box.ROUNDED
                    )
                    live.update(live_box)
                    time.sleep(0.5)

            runner.cleanup_temp()
            afk_duration = random.randint(afk_min, afk_max)
            afk_start = time.time()
            with Live(console=console, refresh_per_second=2) as live:
                while time.time() - afk_start < afk_duration:
                    rem = int(afk_duration - (time.time() - afk_start))
                    live_box = Panel(
                        f"[{COLOR_DIM}]○ Статус:[/] [{COLOR_MUTED}]AFK / Перерыв (активность снята)[/]\n\n"
                        f"Перерыв длится : [{COLOR_MUTED}]{(time.time() - afk_start):.0f}с / {afk_duration}с[/]\n"
                        f"Следующая игра : [bold {COLOR_WHITE}]{rem // 60:02d}:{rem % 60:02d}[/]\n\n"
                        f"[{COLOR_DIM}]Имитация естественного поведения игрока[/]",
                        border_style=COLOR_BORDER,
                        box=box.ROUNDED
                    )
                    live.update(live_box)
                    time.sleep(0.5)

            session_num += 1

    except KeyboardInterrupt:
        console.print(f"\n\n[{COLOR_MUTED}]Humanizer остановлен.[/]")
    finally:
        runner.cleanup_temp()
        console.print(f"[{COLOR_MUTED}]Процессы завершены.[/]")
        Prompt.ask("\nНажмите Enter для возврата")


def run_forge_mode():
    clear()
    console.print(Panel(
        f"[bold {COLOR_WHITE}]Кузница игр (Game Forge)[/]\n"
        f"[{COLOR_MUTED}]Запуск процессов с кастомными названиями (невышедшие игры / фейки)[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    table = Table(box=box.SIMPLE, expand=True)
    table.add_column("#", style=COLOR_ACCENT, width=4, justify="center")
    table.add_column("Пресет", style=f"bold {COLOR_WHITE}")
    table.add_column("Имя процесса", style=COLOR_MUTED)

    for idx, p in enumerate(FORGE_PRESETS, 1):
        table.add_row(str(idx), p["name"], p["exe"])
    table.add_row("C", "Создать свою игру (любое название)", "custom_game.exe")

    console.print(table)
    ch = Prompt.ask("\nВыбор", default="1").strip()

    if ch.upper() == "C":
        title = Prompt.ask("Название игры (как будет отображаться в Discord)").strip()
        exe = Prompt.ask("Имя exe-файла", default="custom_game.exe").strip()
        if not title:
            return
    elif ch.isdigit() and 1 <= int(ch) <= len(FORGE_PRESETS):
        preset = FORGE_PRESETS[int(ch) - 1]
        title, exe = preset["name"], preset["exe"]
    else:
        return

    runner = SpooferRunner()
    runner.launch_custom(title, exe)

    clear()
    console.print(Panel(
        f"[{COLOR_ACCENT}]● Активен кастомный процесс[/]\n\n"
        f"Название : [bold {COLOR_WHITE}]{title}[/]\n"
        f"Процесс  : [{COLOR_MUTED}]{exe}[/]\n\n"
        f"[{COLOR_DIM}]Проверьте статус в Discord. Нажмите Enter для остановки.[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    Prompt.ask("\nНажмите Enter для остановки")
    runner.cleanup_temp()
    console.print(f"[{COLOR_MUTED}]Процесс остановлен.[/]")
    time.sleep(0.8)


def run_single_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel(
        f"[bold {COLOR_WHITE}]Одиночный запуск из базы[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    q = Prompt.ask("Поиск игры по названию").strip()
    if not q:
        return

    matches = [g for g in games if q.lower() in g["name"].lower()][:10]
    if not matches:
        console.print(f"[{COLOR_MUTED}]Игр не найдено.[/]")
        Prompt.ask("\nНажмите Enter для возврата")
        return

    table = Table(box=box.SIMPLE)
    table.add_column("#", style=COLOR_ACCENT, width=4)
    table.add_column("Название", style=f"bold {COLOR_WHITE}")
    table.add_column("Файл", style=COLOR_MUTED)

    for idx, m in enumerate(matches, 1):
        table.add_row(str(idx), m["name"], m["exe"])
    console.print(table)

    c = Prompt.ask("\nВыберите номер", choices=[str(i) for i in range(1, len(matches) + 1)])
    sel = matches[int(c) - 1]

    runner = SpooferRunner()
    runner.launch_game(sel)

    console.print(f"\n[{COLOR_ACCENT}]● {sel['name']} активна в Discord[/]")
    Prompt.ask("\nНажмите Enter для завершения")
    runner.cleanup_temp()


def show_stats(history: HistoryManager, total_games: int):
    clear()
    boosted = history.total_count()
    pct = (boosted / total_games * 100) if total_games else 0.0

    stat_table = Table(box=box.SIMPLE, show_header=False, expand=True)
    stat_table.add_column(style=COLOR_MUTED, width=30)
    stat_table.add_column(style=f"bold {COLOR_WHITE}")

    stat_table.add_row("Всего игр в базе Discord:", f"{total_games:,}")
    stat_table.add_row("Пройдено в истории:", f"[{COLOR_ACCENT}]{boosted:,}[/] ({pct:.2f}%)")
    stat_table.add_row("Осталось до Мифика (10k):", f"{max(0, 10000 - boosted):,}")

    console.print(Panel(
        stat_table,
        title=f"[{COLOR_MUTED}]Статистика профиля[/]",
        border_style=COLOR_BORDER,
        box=box.ROUNDED
    ))

    if boosted > 0:
        history_table = Table(title=f"[{COLOR_DIM}]Последние 5 игр[/]", box=box.SIMPLE)
        history_table.add_column("ID", style=COLOR_DIM)
        history_table.add_column("Игра", style=f"bold {COLOR_WHITE}")
        history_table.add_column("Время", style=COLOR_MUTED)

        items = list(history.data.items())[-5:]
        for gid, data in reversed(items):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("timestamp", 0)))
            history_table.add_row(gid, data.get("name", "Unknown"), ts)
        console.print(history_table)

    console.print(f"\n  [{COLOR_ACCENT}]1[/] Очистить историю сессий")
    console.print(f"  [{COLOR_WHITE}]0[/] Назад")

    ch = Prompt.ask("\nВыбор", choices=["0", "1"], default="0", show_choices=False, show_default=False)
    if ch == "1":
        if Confirm.ask("Точно очистить историю?", default=False):
            history.clear()
            console.print(f"[{COLOR_MUTED}]История сброшена.[/]")
            time.sleep(1)


def main():
    if os.name == "nt":
        os.system("")

    history = HistoryManager()
    with console.status(f"[{COLOR_MUTED}]Загрузка базы игр...[/]", spinner="dots", spinner_style=COLOR_ACCENT):
        games = fetch_games()

    while True:
        clear()
        console.print(make_header_panel(is_discord_running(), len(games), history.total_count()))
        console.print(make_menu_table())

        choice = Prompt.ask(
            f"   [{COLOR_MUTED}]выбор[/] [{COLOR_ACCENT}]>[/]",
            choices=["0", "00", "1", "01", "2", "02", "3", "03", "4", "04", "5", "05", "6", "06", "7", "07"],
            default="1",
            show_choices=False,
            show_default=False
        )

        ch = choice.lstrip("0") or "0"

        if ch == "1":
            run_variety_mode(games, history)
        elif ch == "2":
            run_hour_farm_mode(games)
        elif ch == "3":
            run_humanizer_mode(games)
        elif ch == "4":
            run_forge_mode()
        elif ch == "5":
            run_single_mode(games)
        elif ch == "6":
            show_stats(history, len(games))
        elif ch == "7":
            with console.status(f"[{COLOR_MUTED}]Синхронизация с Discord API...[/]", spinner="dots", spinner_style=COLOR_ACCENT):
                games = fetch_games(force_refresh=True)
            console.print(f"[{COLOR_ACCENT}]База обновлена. Всего игр: {len(games):,}[/]")
            time.sleep(1)
        elif ch == "0":
            clear()
            console.print(f"[{COLOR_MUTED}]Работа завершена.[/]")
            break


if __name__ == "__main__":
    main()
