import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

# Warm Minimalist Palette (inspired by portfolio aesthetic)
COLOR_ACCENT = "#EBAF8E"      # Warm peach / sand accent
COLOR_DOT = "#E68A52"         # Warm amber-orange dot
COLOR_WHITE = "#FFFFFF"       # Crisp white
COLOR_MUTED = "#8C8C8C"       # Muted slate grey
COLOR_DIM = "#5A5A5A"         # Subtle dark grey
COLOR_BORDER = "#2E2E2E"      # Minimal dark border

console = Console(force_terminal=True)


def clear():
    console.clear()


def make_header_panel(discord_online: bool, total_games: int, boosted: int) -> Panel:
    status_dot = f"[{COLOR_ACCENT}]●[/] [{COLOR_WHITE}]в сети[/]" if discord_online else f"[{COLOR_DIM}]○[/] [{COLOR_MUTED}]не запущен[/]"
    pct = (boosted / total_games * 100) if total_games else 0.0

    header_table = Table.grid(expand=True)
    header_table.add_column()
    header_table.add_column(justify="right")

    header_table.add_row(
        f"[{COLOR_DIM}]/[/] [bold {COLOR_WHITE}]spectre[/] [{COLOR_DIM}].dev[/]",
        f"[{COLOR_DOT}]●[/] [{COLOR_MUTED}]discord activity engine[/]"
    )

    content = Table.grid(padding=(0, 2), expand=True)
    content.add_column()
    content.add_row(header_table)
    content.add_row(Text(""))
    content.add_row(
        f"[bold {COLOR_WHITE}]Виртуализация игровой активности.[/]\n"
        f"[bold {COLOR_ACCENT}]Прокачка значков и времени в играх[/]"
    )
    content.add_row(Text(""))

    # Bottom stats row
    stats_table = Table.grid(padding=(0, 3))
    stats_table.add_column(style=COLOR_MUTED)
    stats_table.add_column(style=COLOR_WHITE)
    stats_table.add_column(style=COLOR_MUTED)
    stats_table.add_column(style=COLOR_WHITE)
    stats_table.add_column(style=COLOR_MUTED)
    stats_table.add_column(style=COLOR_WHITE)

    stats_table.add_row(
        "Discord:", status_dot,
        "База тайтлов:", f"[bold {COLOR_WHITE}]{total_games:,}[/]",
        "Прогресс значка:", f"[{COLOR_ACCENT}]{boosted:,}[/] / 10,000 [{COLOR_MUTED}]({pct:.1f}%)[/]"
    )

    content.add_row(stats_table)

    return Panel(
        content,
        border_style=COLOR_BORDER,
        box=box.ROUNDED,
        padding=(1, 2)
    )


def make_menu_table() -> Table:
    table = Table(
        show_header=False,
        box=None,
        padding=(0, 1),
        expand=True
    )
    table.add_column("Key", style=f"bold {COLOR_ACCENT}", width=6, justify="center")
    table.add_column("Title", style=f"bold {COLOR_WHITE}", width=22)
    table.add_column("Desc", style=COLOR_MUTED)
    table.add_column("Badge", style=COLOR_ACCENT, justify="right", width=22)

    table.add_row(
        "01", "Универсал (Variety)",
        "Автоматический перебор 10 400+ игр батчами",
        "Значок «Универсал»"
    )
    table.add_row(
        "02", "Множитель часов",
        "Параллельный запуск до 20 игр (умножение времени x20)",
        "Значок «Время в играх»"
    )
    table.add_row(
        "03", "Имитация игрока",
        "Естественные игровые сессии со сменой игр и AFK",
        "Беспалевный фарм"
    )
    table.add_row(
        "04", "Кузница игр (Forge)",
        "Кастомные процессы (GTA VI Alpha, Half-Life 3 и др.)",
        "Кастомный статус"
    )
    table.add_row(
        "05", "Одиночный запуск",
        "Быстрый поиск и запуск любой игры из базы",
        "Статус активности"
    )
    table.add_row(
        "06", "Статистика",
        "История обработанных игр и сброс прогресса",
        "Аналитика"
    )
    table.add_row(
        "07", "Синхронизация",
        "Обновить официальный список игр Discord",
        "API обновление"
    )
    table.add_row(
        "00", "Выход",
        "Завершить работу всех виртуальных процессов",
        ""
    )

    return Panel(
        table,
        border_style=COLOR_BORDER,
        box=box.ROUNDED,
        padding=(1, 1)
    )


def make_batch_table(batch_games: List[Dict[str, Any]], batch_num: int, total_batches: int) -> Table:
    table = Table(
        title=f"[{COLOR_MUTED}]Батч #{batch_num} из {total_batches}[/]",
        box=box.SIMPLE,
        show_header=True,
        header_style=f"bold {COLOR_ACCENT}",
        expand=True
    )
    table.add_column("#", style=COLOR_DIM, width=4, justify="center")
    table.add_column("Игра", style=f"bold {COLOR_WHITE}")
    table.add_column("Исполняемый файл", style=COLOR_MUTED)
    table.add_column("Статус", style=COLOR_ACCENT, width=12, justify="center")

    for idx, g in enumerate(batch_games, 1):
        table.add_row(
            str(idx),
            g["name"][:45],
            g["exe"],
            "● в игре"
        )

    return table


def make_multiplier_table(games: List[Dict[str, Any]]) -> Table:
    table = Table(
        title=f"[{COLOR_MUTED}]Запущено {len(games)} процессов параллельно (множитель {len(games)}x)[/]",
        box=box.SIMPLE,
        show_header=True,
        header_style=f"bold {COLOR_ACCENT}",
        expand=True
    )
    table.add_column("#", style=COLOR_DIM, width=4, justify="center")
    table.add_column("Игра", style=f"bold {COLOR_WHITE}")
    table.add_column("Процесс", style=COLOR_MUTED)
    table.add_column("Поток", style=COLOR_ACCENT, width=12, justify="center")

    for idx, g in enumerate(games, 1):
        table.add_row(
            str(idx),
            g["name"],
            g.get("exe", "game.exe"),
            "● активен"
        )

    return table
