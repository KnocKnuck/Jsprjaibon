#!/usr/bin/env python3
"""
Simple CLI for prediction and backtest engines
This integrates the actual prediction/backtest engines built in Sprint 3/4
"""

import typer
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

from euromillions_ml.config.settings import Settings
from euromillions_ml.data.loader import DataLoader
from euromillions_ml.models.dummy import DummyModel
from euromillions_ml.features.engineering import FeatureEngineer
from euromillions_ml.features.normalizer import FeatureNormalizer
from euromillions_ml.prediction.predictor import Predictor
from euromillions_ml.prediction.backtest import BacktestEngine
from euromillions_ml.utils.display import (
    display_prediction_grids,
    display_backtest_results,
    print_info,
    print_success,
    print_error
)

app = typer.Typer(
    name="euromillions-predict",
    help="EuroMillions Prediction & Backtest CLI"
)
console = Console()


@app.command()
def predict(
    grids: int = typer.Option(2, "--grids", "-g", help="Number of grids to generate"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Generate predictions for next draw"""
    try:
        console.print(Panel("[bold green]PREDICTION MODE[/bold green]", border_style="green"))

        # Load data
        print_info("Loading historical data...")
        settings = Settings()
        loader = DataLoader(settings)
        draws = loader.load_all_historical(use_cache=True)
        print_success(f"Loaded {len(draws)} historical draws")

        # Initialize components
        print_info("Initializing prediction engine...")
        model = DummyModel()
        feature_engineer = FeatureEngineer()
        normalizer = FeatureNormalizer()

        # Extract and normalize features
        if verbose:
            print_info("Extracting features...")
        features = feature_engineer.extract_all_features(draws)
        normalizer.fit(features)

        # Create predictor
        predictor = Predictor(model, feature_engineer, normalizer)

        # Generate predictions
        print_info(f"Generating {grids} prediction grids...")
        prediction_grids = predictor.predict(draws, n_grids=grids)

        # Display results
        console.print()
        display_prediction_grids(prediction_grids, title="Next Draw Predictions")
        console.print()
        print_success(f"Generated {len(prediction_grids)} prediction grids successfully!")

        console.print("\n[dim italic]Note: Using DummyModel for demo. Train actual models for better predictions.[/dim italic]")

    except Exception as e:
        print_error(f"Prediction failed: {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def backtest(
    window: int = typer.Option(6, "--window", "-w", help="Months to backtest"),
    export: str = typer.Option(None, "--export", "-e", help="Export to CSV"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output"),
):
    """Run backtest on historical data"""
    try:
        console.print(Panel("[bold yellow]BACKTEST MODE[/bold yellow]", border_style="yellow"))

        # Load data
        print_info("Loading historical data...")
        settings = Settings()
        loader = DataLoader(settings)
        draws = loader.load_all_historical(use_cache=True)
        print_success(f"Loaded {len(draws)} historical draws")

        # Initialize components
        print_info("Initializing backtest engine...")
        model = DummyModel()
        feature_engineer = FeatureEngineer()
        normalizer = FeatureNormalizer()

        # Extract and normalize features
        features = feature_engineer.extract_all_features(draws)
        normalizer.fit(features)

        # Create predictor and backtest engine
        predictor = Predictor(model, feature_engineer, normalizer)
        backtest_engine = BacktestEngine(predictor)

        # Run backtest
        console.print()
        result = backtest_engine.run_backtest(draws, window_months=window)

        # Display results
        console.print()
        display_backtest_results(result)

        # Export if requested
        if export:
            print_info(f"Exporting results to {export}...")
            df = result.to_dataframe()
            df.to_csv(export, index=False)
            print_success(f"Results exported to {export}")

        console.print("\n[dim italic]Note: Using DummyModel for demo. Train actual models for better results.[/dim italic]")

    except Exception as e:
        print_error(f"Backtest failed: {e}")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


if __name__ == "__main__":
    # Disclaimer
    console.print(Panel(
        "[bold yellow]DISCLAIMER:[/bold yellow] For educational purposes only. "
        "Lottery outcomes are random and cannot be predicted.",
        border_style="yellow"
    ))
    console.print()

    app()
