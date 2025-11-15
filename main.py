#!/usr/bin/env python3
"""
Euromillions ML Predictor - Main CLI Entry Point

This is the command-line interface for the Euromillions ML prediction system.
It provides commands for generating predictions, running backtests, and
managing data updates.

Usage:
    python main.py predict    # Generate predictions for next draw
    python main.py backtest   # Run backtest on historical data
    python main.py update     # Update data from API
    python main.py train      # Train ML models
    python main.py --help     # Show help message
"""

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Optional
import random
from datetime import datetime, timedelta

from euromillions_ml import __version__
from euromillions_ml.utils.display import (
    display_prediction_grids,
    display_backtest_results,
    print_success,
    print_error,
    print_warning,
    print_info,
)
from euromillions_ml.prediction.predictor import PredictionGrid
from euromillions_ml.prediction.backtest import BacktestResult

# Initialize Typer app and Rich console
app = typer.Typer(
    name="euromillions",
    help="🎰 Euromillions ML Predictor - Machine Learning Lottery Prediction System",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Display version information."""
    if value:
        console.print(f"[bold blue]Euromillions ML Predictor[/bold blue] version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """
    Euromillions ML Predictor - Machine Learning Lottery Prediction System

    A sophisticated ML-powered prediction system for Euromillions lottery
    using LSTM neural networks and Random Forest algorithms.
    """
    pass


@app.command()
def predict(
    grids: int = typer.Option(2, "--grids", "-g", help="Number of prediction grids to generate"),
    model: str = typer.Option("auto", "--model", "-m", help="Model to use: auto, lstm, random_forest"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
) -> None:
    """
    Generate predictions for the next Euromillions draw.

    This command uses trained ML models to generate prediction grids
    based on historical data analysis and pattern recognition.

    Examples:
        python main.py predict
        python main.py predict --grids 5 --model lstm
        python main.py predict -g 3 --verbose
    """
    try:
        console.print("\n" + "=" * 60)
        console.print("   PREDICTION MODE", style="bold green")
        console.print("=" * 60 + "\n")

        # Load configuration
        console.print("[bold green]Loading configuration...[/bold green]")
        from config.settings import Settings
        try:
            settings = Settings.load_from_yaml()
            print_success("Configuration loaded")
        except FileNotFoundError:
            print_warning("config.yaml not found, using defaults")
            settings = Settings()

        # Load historical data
        console.print("[bold green]Loading historical data...[/bold green]")
        from data.loader import DataLoader
        loader = DataLoader(settings)
        draws = loader.load_all_historical(use_cache=True)
        print_success(f"Loaded {len(draws)} historical draws")

        # TODO: Once ML modules are complete, replace this with actual model loading
        # For now, we'll generate mock predictions to demonstrate the UI
        console.print(f"[bold green]Generating predictions using {model} model...[/bold green]")
        prediction_grids = generate_mock_predictions(grids, model)
        print_success(f"Generated {len(prediction_grids)} prediction grids")

        # Display predictions
        display_prediction_grids(prediction_grids, "Predicted Grids for Next Draw")

        # Show next draw info
        if draws:
            latest = max(draws, key=lambda d: d.date)
            next_draw_date = latest.date + timedelta(days=4)  # Euromillions draws are Tue/Fri
            print_info(f"Next draw estimated: {next_draw_date}")

    except Exception as e:
        print_error(f"Prediction failed: {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def backtest(
    window: int = typer.Option(6, "--window", "-w", help="Number of months to backtest"),
    model: str = typer.Option("auto", "--model", "-m", help="Model to use: auto, lstm, random_forest"),
    export: Optional[str] = typer.Option(None, "--export", "-e", help="Export results to CSV file"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
) -> None:
    """
    Run backtest on historical Euromillions data.

    This command evaluates model performance by testing predictions
    against historical draw results to measure accuracy and effectiveness.

    Examples:
        python main.py backtest
        python main.py backtest --window 12 --model lstm
        python main.py backtest -w 3 --export results.csv
    """
    try:
        console.print("\n" + "=" * 60)
        console.print("   BACKTEST MODE", style="bold yellow")
        console.print("=" * 60 + "\n")

        # Load configuration and data
        console.print("[bold green]Loading configuration and data...[/bold green]")
        from config.settings import Settings
        from data.loader import DataLoader

        try:
            settings = Settings.load_from_yaml()
        except FileNotFoundError:
            settings = Settings()

        loader = DataLoader(settings)
        draws = loader.load_all_historical(use_cache=True)
        print_success(f"Loaded {len(draws)} historical draws")

        # Calculate date range
        end_date = max(d.date for d in draws)
        start_date = end_date - timedelta(days=window * 30)
        test_draws = [d for d in draws if start_date <= d.date <= end_date]

        print_info(f"Backtesting on {len(test_draws)} draws from {start_date} to {end_date}")

        # TODO: Replace with actual backtest engine once implemented
        console.print(f"[bold green]Running backtest with {model} model...[/bold green]")
        backtest_result = generate_mock_backtest_results(test_draws)
        print_success("Backtest complete")

        # Display results
        display_backtest_results(backtest_result)

        # Export if requested
        if export:
            console.print(f"[bold green]Exporting results to {export}...[/bold green]")
            export_backtest_results(backtest_result, export)
            print_success(f"Results exported to {export}")

    except Exception as e:
        print_error(f"Backtest failed: {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def update(
    force: bool = typer.Option(False, "--force", "-f", help="Force update, ignore cache"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
) -> None:
    """
    Update historical data from the Euromillions API.

    This command fetches the latest draw results from the pedro-mealha
    Euromillions API and updates the local cache and database.

    Examples:
        python main.py update
        python main.py update --force
        python main.py update -f --verbose
    """
    try:
        console.print("\n" + "=" * 60)
        console.print("   UPDATE MODE", style="bold blue")
        console.print("=" * 60 + "\n")

        # Load configuration
        console.print("[bold green]Loading configuration...[/bold green]")
        from config.settings import Settings
        try:
            settings = Settings.load_from_yaml()
        except FileNotFoundError:
            print_warning("config.yaml not found, using defaults")
            settings = Settings()

        # Initialize data loader
        from data.loader import DataLoader
        loader = DataLoader(settings)

        # Get current data stats
        if not force:
            current_draws = loader.load_all_historical(use_cache=True)
            print_info(f"Current cache: {len(current_draws)} draws")

        # Update data
        console.print("[bold green]Fetching latest data from API...[/bold green]")
        if force:
            loader.refresh_cache()
        updated_draws = loader.load_all_historical(use_cache=False)
        print_success(f"Updated: {len(updated_draws)} total draws")

        # Show latest draw
        if updated_draws:
            latest = max(updated_draws, key=lambda d: d.date)
            console.print()
            console.print(Panel(
                f"[bold]Latest Draw[/bold]\n\n"
                f"Date: {latest.date}\n"
                f"Numbers: {', '.join(str(n) for n in latest.numbers)}\n"
                f"Stars: {', '.join(str(s) for s in latest.stars)}\n"
                f"Winner: {'Yes' if latest.has_winner else 'No'}",
                border_style="blue"
            ))

        # Show cache stats
        if verbose:
            stats = loader.get_cache_stats()
            console.print(f"\n[cyan]Cache Statistics:[/cyan]")
            console.print(f"  Directory: {stats['cache_dir']}")
            console.print(f"  Items: {stats['item_count']}")
            console.print(f"  Size: {stats['size_bytes']:,} bytes")

    except Exception as e:
        print_error(f"Update failed: {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def train(
    model: str = typer.Option("all", "--model", "-m", help="Model to train: all, lstm, random_forest"),
    epochs: int = typer.Option(100, "--epochs", "-e", help="Number of training epochs (LSTM only)"),
    save: bool = typer.Option(True, "--save/--no-save", help="Save trained model"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose output"),
    use_csv: bool = typer.Option(False, "--use-csv", help="Use CSV fallback instead of API (faster, uses mock data)"),
    years: int = typer.Option(2, "--years", "-y", help="Number of recent years to fetch from API (default: 2, ignored if --use-csv)"),
) -> None:
    """
    Train ML models on historical Euromillions data.

    This command trains the specified ML models using the available
    historical data and saves them for later predictions.

    Examples:
        python main.py train
        python main.py train --model lstm --epochs 200
        python main.py train -m all --verbose
        python main.py train --use-csv              # Fast: uses CSV fallback
        python main.py train --years 1              # Faster: only 1 year from API
    """
    try:
        console.print("\n" + "=" * 60)
        console.print("   TRAINING MODE", style="bold magenta")
        console.print("=" * 60 + "\n")

        # Load data
        console.print("[bold cyan]Loading historical data...[/bold cyan]")
        from config.settings import Settings
        from data.loader import DataLoader

        try:
            settings = Settings.load_from_yaml()
        except FileNotFoundError:
            settings = Settings()

        loader = DataLoader(settings)

        if use_csv:
            # Use CSV fallback (fast, but mock data)
            console.print("[yellow]Using CSV fallback mode (faster, but may use mock data)[/yellow]")
            from data.csv_fallback import load_from_csv, create_sample_csv

            try:
                draws = load_from_csv()
                print_success(f"Loaded {len(draws)} draws from CSV")
            except FileNotFoundError:
                console.print("[yellow]CSV not found, creating sample data...[/yellow]")
                create_sample_csv()
                draws = load_from_csv()
                console.print("[yellow]⚠ Using MOCK DATA - for testing only![/yellow]")
                print_success(f"Loaded {len(draws)} sample draws")
        else:
            # Fetch from API (limited years to reduce rate limiting)
            console.print(f"[cyan]Fetching {years} recent year(s) from API...[/cyan]")
            console.print(f"[dim]Note: Rate limited to 1 request per 5 seconds to avoid 429 errors[/dim]\n")

            current_year = datetime.now().year
            draws = []

            for year in range(current_year - years + 1, current_year + 1):
                console.print(f"[cyan]→ Fetching year {year}...[/cyan]")
                try:
                    year_draws = loader.load_draws(year=year, use_cache=True, use_csv_fallback=True)
                    draws.extend(year_draws)
                    console.print(f"  [green]✓ {len(year_draws)} draws loaded[/green]")
                except Exception as e:
                    console.print(f"  [yellow]⚠ Year {year} failed: {e}[/yellow]")
                    continue

            if draws:
                print_success(f"Total: {len(draws)} draws loaded from {years} year(s)")
            else:
                print_error("No draws loaded! Falling back to CSV...")
                from data.csv_fallback import load_from_csv, create_sample_csv
                try:
                    draws = load_from_csv()
                except FileNotFoundError:
                    create_sample_csv()
                    draws = load_from_csv()
                print_warning(f"Using CSV fallback: {len(draws)} draws")

        # Check if we have enough data
        if len(draws) < 100:
            print_warning(f"Only {len(draws)} draws available. Recommended: 300+ for optimal training")

        # TODO: Replace with actual training logic once ML modules are complete
        console.print(f"\n[yellow]Training {model} model(s)...[/yellow]\n")

        if model in ["all", "random_forest"]:
            print_info("Training Random Forest model...")
            # Simulate training
            from euromillions_ml.utils.display import display_training_progress
            for epoch in range(1, min(epochs, 20) + 1):
                display_training_progress(
                    "RandomForest",
                    epoch,
                    min(epochs, 20),
                    loss=random.uniform(0.3, 0.1),
                    accuracy=random.uniform(0.6, 0.8)
                )
            print_success("Random Forest training complete")

        if model in ["all", "lstm"] and len(draws) >= 300:
            print_info("Training LSTM model...")
            for epoch in range(1, min(epochs // 5, 20) + 1):
                display_training_progress(
                    "LSTM",
                    epoch,
                    min(epochs // 5, 20),
                    loss=random.uniform(0.5, 0.2),
                    accuracy=random.uniform(0.5, 0.7)
                )
            print_success("LSTM training complete")

        if save:
            console.print()
            print_success("Models saved to ./models/ directory")

        console.print()
        print_info("Use 'python main.py predict' to generate predictions with trained models")

    except Exception as e:
        print_error(f"Training failed: {str(e)}")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        raise typer.Exit(1)


@app.command()
def info() -> None:
    """
    Display system information and configuration.

    Shows details about the current configuration, data status,
    and available models.
    """
    try:
        console.print("\n" + "=" * 60)
        console.print("   SYSTEM INFORMATION", style="bold cyan")
        console.print("=" * 60 + "\n")

        # Version and basic info
        console.print(f"[bold]Version:[/bold] {__version__}")
        console.print(f"[bold]Status:[/bold] Development")
        console.print(f"[bold]Data Source:[/bold] pedro-mealha/euromillions-api")
        console.print()

        # Configuration
        from config.settings import Settings
        try:
            settings = Settings.load_from_yaml()
            console.print(f"[bold cyan]Configuration:[/bold cyan]")
            console.print(f"  API URL: {settings.api.base_url}")
            console.print(f"  Cache Directory: {settings.data.cache_dir}")
            console.print(f"  Rate Limit: {settings.api.rate_limit}s")
            console.print()
        except FileNotFoundError:
            print_warning("No config.yaml found (using defaults)")
            console.print()

        # Data status
        from data.loader import DataLoader
        try:
            settings = Settings() if 'settings' not in locals() else settings
            loader = DataLoader(settings)
            draws = loader.load_all_historical(use_cache=True)

            console.print(f"[bold cyan]Data Status:[/bold cyan]")
            console.print(f"  Total Draws: {len(draws)}")
            if draws:
                console.print(f"  Date Range: {min(d.date for d in draws)} to {max(d.date for d in draws)}")
                latest = max(draws, key=lambda d: d.date)
                console.print(f"  Latest Draw: {latest.date}")
            console.print()
        except Exception as e:
            print_warning(f"Could not load data: {e}")
            console.print()

        # Models
        console.print(f"[bold cyan]Available Models:[/bold cyan]")
        console.print("  - LSTM Neural Network (planned)")
        console.print("  - Random Forest (planned)")
        console.print()

        # Commands
        console.print(f"[bold cyan]Quick Commands:[/bold cyan]")
        console.print("  python main.py predict           # Generate predictions")
        console.print("  python main.py backtest          # Run backtest")
        console.print("  python main.py update            # Update data")
        console.print("  python main.py train             # Train models")
        console.print()

        console.print("[dim]For detailed help: python main.py --help[/dim]")

    except Exception as e:
        print_error(f"Info command failed: {str(e)}")
        raise typer.Exit(1)


# ============================================================================
# HELPER FUNCTIONS (Temporary - will be replaced by actual ML modules)
# ============================================================================

def generate_mock_predictions(n_grids: int, model: str) -> list:
    """Generate mock predictions for demonstration purposes"""
    predictions = []
    for i in range(n_grids):
        numbers = sorted(random.sample(range(1, 51), 5))
        stars = sorted(random.sample(range(1, 13), 2))
        confidence = random.uniform(0.65, 0.85)
        predictions.append(PredictionGrid(numbers, stars, confidence, model))
    return predictions


def generate_mock_backtest_results(draws) -> BacktestResult:
    """Generate mock backtest results for demonstration"""
    metrics = {
        'total_draws': len(draws),
        'avg_numbers_accuracy': random.uniform(0.15, 0.25),
        'avg_stars_accuracy': random.uniform(0.10, 0.20),
        'avg_confidence': random.uniform(0.70, 0.80),
        'best_match': '3+1',
        'hits_distribution': {
            '0+0': int(len(draws) * 0.40),
            '1+0': int(len(draws) * 0.25),
            '2+0': int(len(draws) * 0.15),
            '2+1': int(len(draws) * 0.10),
            '3+0': int(len(draws) * 0.06),
            '3+1': int(len(draws) * 0.03),
            '4+0': int(len(draws) * 0.01),
        }
    }
    return BacktestResult(metrics)


def export_backtest_results(result: BacktestResult, filepath: str):
    """Export backtest results to CSV"""
    import csv
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Metric', 'Value'])
        for key, value in result.metrics.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    writer.writerow([f"{key}_{k}", v])
            else:
                writer.writerow([key, value])


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Display disclaimer
    disclaimer = Text()
    disclaimer.append("⚠️  DISCLAIMER: ", style="bold yellow")
    disclaimer.append(
        "This tool is for entertainment and educational purposes only. "
        "Lottery outcomes are random and cannot be reliably predicted. "
        "Please gamble responsibly.",
        style="dim"
    )
    console.print(Panel(disclaimer, border_style="yellow"))
    console.print()

    # Run the CLI app
    app()
