import time
from typing import List, Dict, Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.text import Text
from rich.layout import Layout
from rich import box

console = Console()

TITLE_ASCII = """[bold cyan]
  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗ ███████╗
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝
  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝█████╗  
  ╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══╝  
  ███████║██║     ███████╗╚██████╗   ██║   ██║  ██║███████╗
  ╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝[/bold cyan]"""

SUBTITLE = "[dim]DISCORD ACTIVITY & BADGE VIRTUALIZATION ENGINE // v3.0[/dim]"


def clear():
    console.clear()


def make_header_panel(discord_online: bool, total_games: int, boosted: int) -> Panel:
    status_text = "[bold green]ONLINE[/bold green]" if discord_online else "[bold red]OFFLINE (Discord not running)[/bold red]"
    pct = (boosted / total_games * 100) if total_games else 0.0

    info_table = Table.grid(padding=(0, 2))
    info_table.add_column(style="dim", justify="right")
    info_table.add_column(style="bold white")
    info_table.add_column(style="dim", justify="right")
    info_table.add_column(style="bold white")

    info_table.add_row(
        "Discord IPC:", status_text,
        "Database Index:", f"[cyan]{total_games:,}[/cyan] games"
    )
    info_table.add_row(
        "Farmed Badges:", f"[green]{boosted:,}[/green] / {total_games:,} ([yellow]{pct:.1f}%[/yellow])",
        "Target:", "[magenta]Mythic (10,000 games)[/magenta]"
    )

    header_content = Text.from_markup(f"{TITLE_ASCII}\n  {SUBTITLE}\n\n")
    
    table_wrapper = Table(show_header=False, box=None, padding=0)
    table_wrapper.add_row(header_content)
    table_wrapper.add_row(info_table)

    return Panel(
        table_wrapper,
        border_style="cyan",
        box=box.ROUNDED,
        padding=(1, 2)
    )


def make_menu_table() -> Table:
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.SIMPLE_HEAVY,
        expand=True,
        padding=(0, 1)
    )
    table.add_column("Key", style="bold yellow", width=6, justify="center")
    table.add_column("Module", style="bold white", width=18)
    table.add_column("Description", style="dim")
    table.add_column("Target Metric", style="cyan", width=22)

    table.add_row(
        "[1]", "VARIETY RUNNER",
        "High-throughput batch cycle across 10,400+ Discord games",
        "[bold green]Game Variety Badge[/bold green]"
    )
    table.add_row(
        "[2]", "MULTIPLIER",
        "Parallel background execution (x20 concurrent game sessions)",
        "[bold green]Game Time Multiplier[/bold green]"
    )
    table.add_row(
        "[3]", "HUMANIZER",
        "Natural play session simulator with dynamic game switching & AFK breaks",
        "[bold green]Stealth Organic Play[/bold green]"
    )
    table.add_row(
        "[4]", "GAME FORGE",
        "Generate custom or unreleased game processes (GTA VI, HL3, Silksong)",
        "[bold magenta]Custom Rich Presence[/bold magenta]"
    )
    table.add_row(
        "[5]", "SINGLE SPOOF",
        "Instant launch of any single game from Discord's verified database",
        "[bold white]Status Spoof[/bold white]"
    )
    table.add_row(
        "[6]", "TELEMETRY",
        "View detailed badge progression stats and cache analytics",
        "[dim]Analytics[/dim]"
    )
    table.add_row(
        "[7]", "SYNC INDEX",
        "Force re-fetch verified detectable titles from Discord REST API",
        "[dim]Maintenance[/dim]"
    )
    table.add_row(
        "[0]", "EXIT",
        "Graceful termination of all active virtual handles",
        "[dim]System[/dim]"
    )

    return table


def make_batch_table(batch_games: List[Dict[str, Any]], batch_num: int, total_batches: int) -> Table:
    table = Table(
        title=f"[bold cyan]Active Process Batch #{batch_num} of {total_batches}[/bold cyan]",
        box=box.ROUNDED,
        header_style="bold magenta",
        expand=True
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Game Title", style="bold white")
    table.add_column("Virtual Executable", style="cyan")
    table.add_column("Platform", style="dim", width=10, justify="center")
    table.add_column("Status", style="bold green", width=12, justify="center")

    for idx, g in enumerate(batch_games, 1):
        table.add_row(
            str(idx),
            g["name"][:45],
            g["exe"],
            "Win32",
            "[green]ACTIVE ●[/green]"
        )

    return table


def make_multiplier_table(games: List[Dict[str, Any]]) -> Table:
    table = Table(
        title=f"[bold magenta]Active Multiplier Farm ({len(games)} concurrent processes - {len(games)}x Speed)[/bold magenta]",
        box=box.ROUNDED,
        header_style="bold cyan",
        expand=True
    )
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("Game Title", style="bold white")
    table.add_column("Process Name", style="cyan")
    table.add_column("Stream State", style="bold green", width=14, justify="center")

    for idx, g in enumerate(games, 1):
        table.add_row(
            str(idx),
            g["name"],
            g.get("exe", "game.exe"),
            "[green]STREAMING ●[/green]"
        )

    return table
