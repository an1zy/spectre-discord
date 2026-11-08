import os
import sys
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
    make_multiplier_table
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
    console.print(Panel("[bold cyan]MODULE 01: VARIETY RUNNER // GAME VARIETY BADGE[/bold cyan]", border_style="cyan"))

    if not is_discord_running():
        console.print("[yellow][!] Warning: Discord desktop application is not detected in processes.[/yellow]")
        console.print("[dim]Ensure Discord is running so game activity is captured.[/dim]")
        if not Confirm.ask("Continue anyway?", default=True):
            return

    unboosted = [g for g in games if not history.is_boosted(g["id"])]
    console.print(f"Games awaiting execution: [bold cyan]{len(unboosted):,}[/bold cyan]")

    if Confirm.ask("Filter out adult/erotic classified titles?", default=True):
        unboosted = [g for g in unboosted if not g["adult"]]
        console.print(f"Queue size after 18+ filter: [bold cyan]{len(unboosted):,}[/bold cyan]")

    if not unboosted:
        console.print("\n[bold green][✓] All available games in the database have been processed![/bold green]")
        Prompt.ask("\nPress Enter to return")
        return

    batch_size = int(Prompt.ask("Concurrent batch size (games per cycle)", default="8"))
    duration = int(Prompt.ask("Holding duration per batch (seconds)", default="15"))

    total_to_boost = len(unboosted)
    total_batches = (total_to_boost + batch_size - 1) // batch_size
    est_total_sec = total_batches * duration

    console.print(f"\n[dim]Session Scope: [bold white]{total_batches:,}[/bold white] batches | [bold white]{batch_size}[/bold white] concurrent | [bold white]{duration}s[/bold white] hold | Est. duration: ~{est_total_sec // 3600}h {(est_total_sec % 3600) // 60}m[/dim]")
    Prompt.ask("\nPress Enter to begin batch virtualization")

    runner = SpooferRunner()
    current_index = 0
    start_time = time.time()

    progress = Progress(
        SpinnerColumn("dots", style="bold cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=35, style="cyan", complete_style="bold green"),
        TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
        TextColumn("•"),
        TextColumn("[bold white]{task.completed}/{task.total} games"),
        TextColumn("•"),
        TimeRemainingColumn(),
        console=console
    )

    task_id = progress.add_task("Total Progression", total=total_to_boost)

    try:
        for batch_num in range(1, total_batches + 1):
            batch_games = unboosted[current_index : current_index + batch_size]
            if not batch_games:
                break

            clear()
            elapsed = int(time.time() - start_time)
            speed = (current_index / (elapsed / 60)) if elapsed > 10 else 0.0

            stats_panel = Panel(
                f"[bold cyan]Batch {batch_num}/{total_batches}[/bold cyan] │ "
                f"Elapsed: [white]{elapsed // 60:02d}:{elapsed % 60:02d}[/white] │ "
                f"Speed: [green]{speed:.1f} games/min[/green] │ "
                f"[dim](Press Ctrl+C to safely pause)[/dim]",
                border_style="dim",
                box=box.HORIZONTALS
            )
            console.print(stats_panel)
            console.print(progress)

            # Spawn virtual processes
            for g in batch_games:
                runner.launch_game(g)

            # Display active batch table
            batch_table = make_batch_table(batch_games, batch_num, total_batches)
            console.print(batch_table)

            # Hold countdown
            for _ in range(duration * 10):
                time.sleep(0.1)

            # Terminate and record
            runner.kill_batch()
            for g in batch_games:
                history.mark_boosted(g["id"], g["name"])
            history.save()

            current_index += len(batch_games)
            progress.update(task_id, advance=len(batch_games))

        console.print("\n[bold green][✓] Session complete! All queued titles virtualized.[/bold green]")
    except KeyboardInterrupt:
        console.print("\n\n[bold yellow][!] Interrupted by user. Gracefully terminating virtual processes...[/bold yellow]")
    finally:
        runner.cleanup_temp()
        history.save()
        console.print("[green][✓] Virtual handles cleaned up and history saved.[/green]")
        Prompt.ask("\nPress Enter to return to menu")


def run_hour_farm_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel("[bold magenta]MODULE 02: MULTIPLIER // GAME TIME BADGE BOOSTER[/bold magenta]", border_style="magenta"))

    if not is_discord_running():
        console.print("[yellow][!] Warning: Discord client not detected.[/yellow]")

    console.print("Select farm preset:")
    console.print("  [bold cyan]1[/bold cyan] Top-20 Popular Steam/PC Games (x20 Multiplier: 1 real hour = 20 Discord hours)")
    console.print("  [bold cyan]2[/bold cyan] Top-10 Popular Games (x10 Multiplier)")
    console.print("  [bold cyan]3[/bold cyan] Custom Game Selection")

    ch = Prompt.ask("\nChoice", choices=["1", "2", "3"], default="1")

    selected = []
    if ch == "2":
        target = POPULAR_GAMES_PRESET[:10]
    elif ch == "3":
        console.print("\n[dim]Enter game names to add (empty line to finish):[/dim]")
        while len(selected) < 20:
            q = Prompt.ask(f"Game #{len(selected)+1}").strip()
            if not q:
                break
            match = next((g for g in games if q.lower() in g["name"].lower()), None)
            if match and match not in selected:
                selected.append(match)
                console.print(f"  [green]+ Added:[/green] {match['name']}")
            else:
                console.print("  [red]Not found in database or already added.[/red]")
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
                    f"[bold white]Real Time Elapsed:[/bold white] [bold cyan]{h:02d}:{m:02d}:{s:02d}[/bold cyan]   │   "
                    f"[bold white]Discord Hours Farmed:[/bold white] [bold green]{farmed_hours:5.2f} hrs[/bold green]   │   "
                    f"[bold white]Multiplier:[/bold white] [bold magenta]{mult}x[/bold magenta]\n"
                    f"[dim]All {mult} game processes streaming concurrently to Discord IPC. Press Ctrl+C to stop.[/dim]",
                    title=f"[bold green]STREAMING ACTIVE ●[/bold green]",
                    border_style="green",
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
        console.print("\n\n[bold yellow][!] Terminating farm processes...[/bold yellow]")
    finally:
        runner.cleanup_temp()
        console.print("[green][✓] All processes closed successfully.[/green]")
        Prompt.ask("\nPress Enter to return")


def run_humanizer_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel("[bold cyan]MODULE 03: HUMANIZER // STEALTH ORGANIC GAMER SIMULATION[/bold cyan]", border_style="cyan"))
    console.print("[dim]Simulates realistic player habits: natural session durations, dynamic game switching, and AFK pauses.[/dim]\n")

    console.print("Select pacing schedule:")
    console.print("  [bold cyan]1[/bold cyan] Realistic Simulation (30-50 min play sessions + 5-10 min AFK breaks)")
    console.print("  [bold cyan]2[/bold cyan] Accelerated / Demo (2-4 min play sessions + 30s AFK breaks)")

    mode = Prompt.ask("\nPacing", choices=["1", "2"], default="1")
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
                        f"[bold green]STATE: IN-GAME ACTIVE[/bold green]\n\n"
                        f"Current Title : [bold white]{active_game['name']}[/bold white]\n"
                        f"Executable    : [cyan]{active_game['exe']}[/cyan]\n"
                        f"Session Time  : [bold cyan]{el // 60:02d}:{el % 60:02d}[/bold cyan] / [dim]{duration // 60:02d}:{duration % 60:02d}[/dim]\n"
                        f"Next Rotation : [yellow]{rem // 60:02d}:{rem % 60:02d}[/yellow]\n\n"
                        f"[dim]Session #{session_num} │ Press Ctrl+C to terminate[/dim]",
                        title="[bold cyan]SPECTRE HUMANIZER ENGINE[/bold cyan]",
                        border_style="cyan"
                    )
                    live.update(live_box)
                    time.sleep(0.5)

            # AFK Break
            runner.cleanup_temp()
            afk_duration = random.randint(afk_min, afk_max)
            afk_start = time.time()
            with Live(console=console, refresh_per_second=2) as live:
                while time.time() - afk_start < afk_duration:
                    rem = int(afk_duration - (time.time() - afk_start))
                    live_box = Panel(
                        f"[bold yellow]STATE: AFK BREAK (No games active)[/bold yellow]\n\n"
                        f"Player Status : [dim]Away from keyboard / Idle[/dim]\n"
                        f"Break Time    : [bold yellow]{(time.time() - afk_start):.0f}s[/bold yellow] / [dim]{afk_duration}s[/dim]\n"
                        f"Resuming in   : [bold white]{rem // 60:02d}:{rem % 60:02d}[/bold white]\n\n"
                        f"[dim]Simulating organic downtime between gaming sessions[/dim]",
                        title="[bold yellow]SPECTRE HUMANIZER ENGINE[/bold yellow]",
                        border_style="yellow"
                    )
                    live.update(live_box)
                    time.sleep(0.5)

            session_num += 1

    except KeyboardInterrupt:
        console.print("\n\n[bold yellow][!] Humanizer halted by user.[/bold yellow]")
    finally:
        runner.cleanup_temp()
        console.print("[green][✓] Processes terminated.[/green]")
        Prompt.ask("\nPress Enter to return")


def run_forge_mode():
    clear()
    console.print(Panel("[bold magenta]MODULE 04: GAME FORGE // UNRELEASED & CUSTOM PRESENCE[/bold magenta]", border_style="magenta"))

    table = Table(box=box.ROUNDED, expand=True)
    table.add_column("Key", style="bold yellow", width=6, justify="center")
    table.add_column("Preset Title", style="bold white")
    table.add_column("Executable Target", style="cyan")

    for idx, p in enumerate(FORGE_PRESETS, 1):
        table.add_row(str(idx), p["name"], p["exe"])
    table.add_row("C", "[bold green]Custom Forge[/bold green] (Enter any title & exe name)", "[dim]user_defined.exe[/dim]")

    console.print(table)
    ch = Prompt.ask("\nSelect target", default="1").strip()

    if ch.upper() == "C":
        title = Prompt.ask("Custom Game Title").strip()
        exe = Prompt.ask("Custom Executable Name (e.g. game.exe)", default="custom_game.exe").strip()
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
        f"[bold green]VIRTUAL PROCESS RUNNING[/bold green]\n\n"
        f"Game Title : [bold white]{title}[/bold white]\n"
        f"Executable : [bold cyan]{exe}[/bold cyan]\n"
        f"Status     : [green]Broadcasting on Discord IPC[/green]\n\n"
        f"[dim]Check your Discord profile. Press Enter to terminate.[/dim]",
        border_style="green",
        box=box.ROUNDED
    ))

    Prompt.ask("\nPress Enter to stop")
    runner.cleanup_temp()
    console.print("[green][✓] Custom process terminated.[/green]")
    time.sleep(0.8)


def run_single_mode(games: List[Dict[str, Any]]):
    clear()
    console.print(Panel("[bold cyan]MODULE 05: SINGLE SPOOF // DIRECT LAUNCH[/bold cyan]", border_style="cyan"))

    q = Prompt.ask("Search verified title in database").strip()
    if not q:
        return

    matches = [g for g in games if q.lower() in g["name"].lower()][:10]
    if not matches:
        console.print("[red]No matching games found in Discord index.[/red]")
        Prompt.ask("\nPress Enter to return")
        return

    table = Table(box=box.ROUNDED)
    table.add_column("#", style="bold yellow", width=4)
    table.add_column("Title", style="bold white")
    table.add_column("Executable", style="cyan")

    for idx, m in enumerate(matches, 1):
        table.add_row(str(idx), m["name"], m["exe"])
    console.print(table)

    c = Prompt.ask("\nSelect game number", choices=[str(i) for i in range(1, len(matches) + 1)])
    sel = matches[int(c) - 1]

    runner = SpooferRunner()
    runner.launch_game(sel)

    console.print(f"\n[bold green][✓] {sel['name']} is now active in Discord![/bold green]")
    Prompt.ask("Press Enter to stop the game")
    runner.cleanup_temp()


def show_stats(history: HistoryManager, total_games: int):
    clear()
    boosted = history.total_count()
    pct = (boosted / total_games * 100) if total_games else 0.0

    stat_table = Table(box=box.ROUNDED, show_header=False, expand=True)
    stat_table.add_column(style="bold cyan", width=30)
    stat_table.add_column(style="bold white")

    stat_table.add_row("Verified Discord Titles Index", f"{total_games:,}")
    stat_table.add_row("Titles Farmed in History", f"[green]{boosted:,}[/green] ({pct:.2f}%)")
    stat_table.add_row("Remaining to Mythic Tier (10k)", f"[yellow]{max(0, 10000 - boosted):,}[/yellow]")

    console.print(Panel(stat_table, title="[bold cyan]TELEMETRY & BADGE ANALYTICS[/bold cyan]", border_style="cyan"))

    if boosted > 0:
        history_table = Table(title="Recent Activity Log (Last 5 Titles)", box=box.SIMPLE)
        history_table.add_column("App ID", style="dim")
        history_table.add_column("Game Title", style="bold white")
        history_table.add_column("Processed At", style="cyan")

        items = list(history.data.items())[-5:]
        for gid, data in reversed(items):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data.get("timestamp", 0)))
            history_table.add_row(gid, data.get("name", "Unknown"), ts)
        console.print(history_table)

    console.print("\nActions:")
    console.print("  [bold red]1[/bold red] Reset history (purge history.json)")
    console.print("  [bold white]0[/bold white] Back to menu")

    ch = Prompt.ask("\nChoice", choices=["0", "1"], default="0")
    if ch == "1":
        if Confirm.ask("[bold red]Are you sure you want to erase all farmed history?[/bold red]", default=False):
            history.clear()
            console.print("[green][✓] History cleared.[/green]")
            time.sleep(1)


def main():
    if os.name == "nt":
        os.system("")

    history = HistoryManager()
    with console.status("[bold cyan]Loading Discord detectable database...", spinner="dots"):
        games = fetch_games()

    while True:
        clear()
        console.print(make_header_panel(is_discord_running(), len(games), history.total_count()))
        console.print(make_menu_table())

        choice = Prompt.ask("   [bold cyan]spectre>[/bold cyan]", choices=["0", "1", "2", "3", "4", "5", "6", "7"], default="1")

        if choice == "1":
            run_variety_mode(games, history)
        elif choice == "2":
            run_hour_farm_mode(games)
        elif choice == "3":
            run_humanizer_mode(games)
        elif choice == "4":
            run_forge_mode()
        elif choice == "5":
            run_single_mode(games)
        elif choice == "6":
            show_stats(history, len(games))
        elif choice == "7":
            with console.status("[bold cyan]Synchronizing with Discord REST API...", spinner="dots"):
                games = fetch_games(force_refresh=True)
            console.print(f"[bold green][✓] Index synchronized! Total titles: {len(games):,}[/bold green]")
            time.sleep(1)
        elif choice == "0":
            clear()
            console.print("[bold cyan]SPECTRE Engine successfully shut down.[/bold cyan]")
            break


if __name__ == "__main__":
    main()
