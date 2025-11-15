"""Terminal display utilities for predictions and results"""
from typing import List, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from ..prediction.predictor import PredictionGrid
from ..prediction.backtest import BacktestResult
from ..data.models import Draw


console = Console()


def display_prediction_grids(grids: List[PredictionGrid], title: str = "Predictions"):
    """Display prediction grids in a formatted table

    Args:
        grids: List of PredictionGrid objects
        title: Table title
    """
    table = Table(title=title, box=box.ROUNDED, show_header=True, header_style="bold cyan")

    table.add_column("Grid", style="dim", width=6)
    table.add_column("Numbers", style="bold green", width=20)
    table.add_column("Stars", style="bold yellow", width=10)
    table.add_column("Confidence", justify="right", style="magenta")
    table.add_column("Method", style="dim")

    for i, grid in enumerate(grids, 1):
        numbers = ' '.join(f'{n:2d}' for n in grid.numbers)
        stars = ' '.join(f'{s:2d}' for s in grid.stars)
        confidence = f"{grid.confidence:.1%}"

        table.add_row(
            f"#{i}",
            numbers,
            stars,
            confidence,
            grid.method
        )

    console.print(table)


def display_backtest_results(result: BacktestResult):
    """Display backtest results

    Args:
        result: BacktestResult object
    """
    metrics = result.metrics

    # Summary panel
    summary = Text()
    summary.append(f"Total Draws: ", style="bold")
    summary.append(f"{metrics['total_draws']}\n")
    summary.append(f"Avg Numbers Accuracy: ", style="bold")
    summary.append(f"{metrics['avg_numbers_accuracy']:.2%}\n", style="green")
    summary.append(f"Avg Stars Accuracy: ", style="bold")
    summary.append(f"{metrics['avg_stars_accuracy']:.2%}\n", style="yellow")
    summary.append(f"Avg Confidence: ", style="bold")
    summary.append(f"{metrics['avg_confidence']:.2%}\n", style="magenta")

    console.print(Panel(summary, title="Backtest Summary", border_style="cyan"))

    # Hits distribution
    if metrics['hits_distribution']:
        table = Table(title="Hits Distribution", box=box.SIMPLE, show_header=True)
        table.add_column("Match Pattern", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")

        total = sum(metrics['hits_distribution'].values())
        for pattern, count in sorted(metrics['hits_distribution'].items(), reverse=True):
            percentage = f"{count / total:.1%}"
            table.add_row(pattern, str(count), percentage)

        console.print(table)

    # Best prediction
    if metrics['best_prediction']:
        best = metrics['best_prediction']
        best_text = Text()
        best_text.append(f"Date: ", style="bold")
        best_text.append(f"{best['date']}\n")
        best_text.append(f"Predicted: ", style="bold")
        best_text.append(f"{best['predicted_numbers']} + {best['predicted_stars']}\n", style="green")
        best_text.append(f"Actual: ", style="bold")
        best_text.append(f"{best['actual_numbers']} + {best['actual_stars']}\n", style="yellow")
        best_text.append(f"Hits: ", style="bold")
        best_text.append(f"{best['numbers_hit']} numbers + {best['stars_hit']} stars\n", style="magenta")

        console.print(Panel(best_text, title="Best Prediction", border_style="green"))


def display_comparison(prediction: PredictionGrid, actual: Draw):
    """Display prediction vs actual comparison

    Args:
        prediction: Predicted grid
        actual: Actual draw result
    """
    numbers_hit = set(prediction.numbers) & set(actual.numbers)
    stars_hit = set(prediction.stars) & set(actual.stars)

    table = Table(title="Prediction vs Actual", box=box.ROUNDED)

    table.add_column("", style="bold")
    table.add_column("Numbers", style="green")
    table.add_column("Stars", style="yellow")
    table.add_column("Hits", style="magenta")

    # Prediction row
    pred_numbers = ' '.join(
        f"[bold green]{n:2d}[/]" if n in numbers_hit else f"{n:2d}"
        for n in prediction.numbers
    )
    pred_stars = ' '.join(
        f"[bold yellow]{s:2d}[/]" if s in stars_hit else f"{s:2d}"
        for s in prediction.stars
    )
    table.add_row("Predicted", pred_numbers, pred_stars, "")

    # Actual row
    act_numbers = ' '.join(
        f"[bold green]{n:2d}[/]" if n in numbers_hit else f"{n:2d}"
        for n in actual.numbers
    )
    act_stars = ' '.join(
        f"[bold yellow]{s:2d}[/]" if s in stars_hit else f"{s:2d}"
        for s in actual.stars
    )
    table.add_row("Actual", act_numbers, act_stars, "")

    # Summary row
    summary = f"{len(numbers_hit)}+{len(stars_hit)}"
    table.add_row("Match", "", "", summary)

    console.print(table)


def display_progress_bar(current: int, total: int, prefix: str = ""):
    """Display a simple progress bar

    Args:
        current: Current progress
        total: Total items
        prefix: Prefix text
    """
    from rich.progress import Progress

    with Progress() as progress:
        task = progress.add_task(f"[cyan]{prefix}", total=total)
        progress.update(task, completed=current)


def print_success(message: str):
    """Print success message"""
    console.print(f"[bold green]✓[/bold green] {message}")


def print_error(message: str):
    """Print error message"""
    console.print(f"[bold red]✗[/bold red] {message}")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[bold yellow]⚠[/bold yellow] {message}")


def print_info(message: str):
    """Print info message"""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")
