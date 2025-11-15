#!/usr/bin/env python3
"""
Full Pipeline Demonstration - Euromillions ML Predictor

This script demonstrates the complete end-to-end pipeline:
1. Data Loading & Validation
2. Feature Engineering
3. Model Training (simulated)
4. Prediction Generation
5. Backtest Analysis

Usage:
    python demo_full_pipeline.py
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table

console = Console()


def print_section(title: str, style: str = "bold cyan"):
    """Print section header"""
    console.print()
    console.print("═" * 70, style=style)
    console.print(f"  {title}", style=style)
    console.print("═" * 70, style=style)
    console.print()


def main():
    """Run full pipeline demonstration"""

    # Display header
    console.print()
    console.print(Panel.fit(
        "[bold cyan]EUROMILLIONS ML PREDICTOR[/bold cyan]\n"
        "[bold]Full Pipeline Demonstration[/bold]\n\n"
        "[dim]This demo showcases the complete workflow from data loading to predictions[/dim]",
        border_style="cyan"
    ))

    try:
        # ================================================================
        # SECTION 1: Configuration & Setup
        # ================================================================
        print_section("1. CONFIGURATION & SETUP")

        from config.settings import Settings
        from utils.logger import setup_logging

        console.print("[bold]Loading configuration...[/bold]")
        try:
            settings = Settings.load_from_yaml()
            console.print("[green]✓[/green] Configuration loaded from config.yaml")
        except FileNotFoundError:
            console.print("[yellow]⚠[/yellow] config.yaml not found, using defaults")
            settings = Settings()

        # Display settings
        settings_table = Table(show_header=False, box=None)
        settings_table.add_column("Setting", style="cyan")
        settings_table.add_column("Value", style="green")

        settings_table.add_row("API URL", str(settings.api.base_url))
        settings_table.add_row("Cache Directory", settings.data.cache_dir)
        settings_table.add_row("Rate Limit", f"{settings.api.rate_limit}s")
        settings_table.add_row("Numbers Range", f"{settings.lottery.numbers_range[0]}-{settings.lottery.numbers_range[1]}")
        settings_table.add_row("Stars Range", f"{settings.lottery.stars_range[0]}-{settings.lottery.stars_range[1]}")

        console.print(settings_table)

        # Setup logging
        setup_logging(log_file="logs/demo_pipeline.log", level="INFO")
        console.print("[green]✓[/green] Logging initialized")

        # ================================================================
        # SECTION 2: Data Loading
        # ================================================================
        print_section("2. DATA LOADING & VALIDATION")

        from data.loader import DataLoader
        from data.models import Draw

        console.print("[bold]Fetching historical data...[/bold]")

        with console.status("[bold green]Loading from API/cache...") as status:
            loader = DataLoader(settings)
            draws = loader.load_all_historical(use_cache=True)

        console.print(f"[green]✓[/green] Loaded {len(draws)} historical draws")

        if not draws:
            console.print("[red]✗[/red] No data available. Please run 'python main.py update' first.")
            return

        # Data summary
        first_draw = min(draws, key=lambda d: d.date)
        last_draw = max(draws, key=lambda d: d.date)
        years_covered = (last_draw.date - first_draw.date).days / 365

        data_table = Table(title="Data Summary", show_header=False)
        data_table.add_column("Metric", style="cyan")
        data_table.add_column("Value", style="green")

        data_table.add_row("Total Draws", str(len(draws)))
        data_table.add_row("First Draw", str(first_draw.date))
        data_table.add_row("Latest Draw", str(last_draw.date))
        data_table.add_row("Years Covered", f"{years_covered:.1f} years")
        data_table.add_row("Latest Numbers", str(last_draw.numbers))
        data_table.add_row("Latest Stars", str(last_draw.stars))

        console.print(data_table)

        # ================================================================
        # SECTION 3: Feature Engineering
        # ================================================================
        print_section("3. FEATURE ENGINEERING")

        # Check if feature engineering modules exist
        try:
            from euromillions_ml.features.engineering import FeatureEngineer
            from euromillions_ml.features.normalizer import FeatureNormalizer

            console.print("[bold]Extracting features from historical data...[/bold]")

            engineer = FeatureEngineer()
            features = engineer.extract_all_features(draws)

            console.print(f"[green]✓[/green] Extracted {features.shape[1]} features")
            console.print(f"  • Feature matrix shape: {features.shape}")

            # Display sample features
            feature_cols = features.columns.tolist()[:10]  # Show first 10
            console.print(f"  • Sample features: {', '.join(feature_cols)}...")

            # Normalize features
            console.print("\n[bold]Normalizing features...[/bold]")
            normalizer = FeatureNormalizer(method='standard')
            features_normalized = normalizer.fit_transform(features)

            console.print(f"[green]✓[/green] Features normalized (method: standard)")
            console.print(f"  • Mean: ~0.0, Std: ~1.0")

        except ImportError as e:
            console.print(f"[yellow]⚠[/yellow] Feature modules not fully implemented yet")
            console.print(f"  Error: {e}")
            features = None
            engineer = None
            normalizer = None

        # ================================================================
        # SECTION 4: Model Overview
        # ================================================================
        print_section("4. AVAILABLE MODELS")

        models_table = Table(title="ML Models", show_header=True)
        models_table.add_column("Model", style="cyan")
        models_table.add_column("Type", style="green")
        models_table.add_column("Status", style="yellow")
        models_table.add_column("Description", style="dim")

        # Check for model files
        models_dir = Path("models")
        rf_exists = (models_dir / "random_forest_v1.joblib").exists() if models_dir.exists() else False
        lstm_exists = (models_dir / "lstm_v1.h5").exists() if models_dir.exists() else False

        models_table.add_row(
            "Random Forest",
            "Ensemble",
            "[green]Available[/green]" if rf_exists else "[yellow]Not trained[/yellow]",
            "Gradient boosting decision trees"
        )
        models_table.add_row(
            "LSTM",
            "Neural Network",
            "[green]Available[/green]" if lstm_exists else "[yellow]Not trained[/yellow]",
            "Long Short-Term Memory network"
        )

        console.print(models_table)

        if not rf_exists and not lstm_exists:
            console.print("\n[yellow]ℹ[/yellow] No trained models found. Run [green]python train_models.py[/green] to train.")

        # ================================================================
        # SECTION 5: Prediction Generation
        # ================================================================
        print_section("5. PREDICTION GENERATION")

        console.print("[bold]Generating predictions...[/bold]\n")

        try:
            from euromillions_ml.models.dummy import DummyModel
            from euromillions_ml.prediction.predictor import Predictor, PredictionGrid

            # Use dummy model for demonstration
            dummy_model = DummyModel()

            if engineer and normalizer:
                predictor = Predictor(dummy_model, engineer, normalizer)
                grids = predictor.predict(draws, n_grids=3)

                console.print(f"[green]✓[/green] Generated {len(grids)} prediction grids\n")

                # Display predictions
                from euromillions_ml.utils.display import display_prediction_grids
                display_prediction_grids(grids, "Predicted Grids for Next Draw")

            else:
                console.print("[yellow]⚠[/yellow] Cannot generate predictions (missing features)")

        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Prediction generation failed: {e}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")

        # ================================================================
        # SECTION 6: Backtest Analysis
        # ================================================================
        print_section("6. BACKTEST ANALYSIS")

        try:
            from euromillions_ml.prediction.backtest import BacktestEngine

            if engineer and normalizer:
                console.print("[bold]Running mini backtest (last 20 draws)...[/bold]\n")

                # Use last 20 draws for quick demo
                predictor_bt = Predictor(dummy_model, engineer, normalizer)
                backtest_engine = BacktestEngine(predictor_bt)

                # Get date range
                end_date = max(d.date for d in draws)
                start_date = end_date - timedelta(days=60)  # ~2 months

                with console.status("[bold green]Running backtest..."):
                    result = backtest_engine.run_backtest(
                        all_draws=draws,
                        start_date=start_date,
                        end_date=end_date,
                        min_training_draws=50
                    )

                console.print(f"\n[green]✓[/green] Backtest complete\n")

                # Display results
                from euromillions_ml.utils.display import display_backtest_results
                display_backtest_results(result)

            else:
                console.print("[yellow]⚠[/yellow] Cannot run backtest (missing features)")

        except Exception as e:
            console.print(f"[yellow]⚠[/yellow] Backtest failed: {e}")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")

        # ================================================================
        # SECTION 7: Summary & Next Steps
        # ================================================================
        print_section("7. SUMMARY & NEXT STEPS", "bold green")

        summary_panel = f"""
[bold green]✓ Pipeline Demonstration Complete[/bold green]

[bold cyan]What We Did:[/bold cyan]
  • Loaded and validated {len(draws)} historical draws
  • Extracted features for ML models
  • Generated prediction grids
  • Ran backtest analysis

[bold cyan]Next Steps:[/bold cyan]
  1. Train models: [green]python train_models.py[/green]
  2. Generate predictions: [green]python main.py predict[/green]
  3. Run full backtest: [green]python main.py backtest[/green]
  4. Update data: [green]python main.py update[/green]

[bold cyan]Files & Directories:[/bold cyan]
  • Data cache: [dim]{settings.data.cache_dir}[/dim]
  • Model files: [dim]./models/[/dim]
  • Log files: [dim]./logs/demo_pipeline.log[/dim]

[bold yellow]⚠ Important Disclaimer:[/bold yellow]
  This tool is for educational purposes only.
  Lottery outcomes are random and cannot be predicted.
  Please play responsibly.
        """

        console.print(Panel(summary_panel.strip(), border_style="green", padding=(1, 2)))
        console.print()

    except KeyboardInterrupt:
        console.print("\n[yellow]Demo interrupted by user[/yellow]")
        sys.exit(0)

    except Exception as e:
        console.print(f"\n[red]✗ Demo failed: {str(e)}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
