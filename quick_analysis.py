#!/usr/bin/env python3
"""
QUICK REAL DATA ANALYSIS - Fetch recent data and train models

This script:
1. Fetches ONLY 2023-2024 data (~100 draws)
2. Trains Random Forest model
3. Runs 3-month backtest
4. Calculates precision, hit rates, and PNL
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import datetime
import time

from config.settings import Settings
from data.loader import DataLoader

print("=" * 80)
print("QUICK EUROMILLIONS ML ANALYSIS - 2023-2024 DATA")
print("=" * 80)
print("\nFetching recent data (2023-2024)...")
print("Note: Using 15-second delays between API calls to avoid rate limiting")
print("This will take approximately 30-60 seconds...\n")

# Load settings
settings = Settings.load_from_yaml('/home/user/Jsprjaibon/config.yaml')

# Fetch only recent data
loader = DataLoader(settings)
all_draws = []

for year in [2023, 2024]:
    print(f"Fetching {year} data...")
    start_time = time.time()
    try:
        year_draws = loader.load_draws(year=year, use_cache=True)
        all_draws.extend(year_draws)
        elapsed = time.time() - start_time
        print(f"  ✓ Loaded {len(year_draws)} draws from {year} ({elapsed:.1f}s)")
    except Exception as e:
        print(f"  ✗ Failed to load {year}: {e}")

print(f"\nTotal draws loaded: {len(all_draws)}")

if len(all_draws) < 50:
    print("\nERROR: Insufficient data. Need at least 50 draws.")
    print("The API may still be rate limiting. Consider:")
    print("1. Waiting 5-10 minutes before retrying")
    print("2. Using cached data if available")
    print("3. Creating sample data for testing")
    sys.exit(1)

print(f"\n✓ Successfully loaded {len(all_draws)} draws")
print(f"  Date range: {min(d.date for d in all_draws).date()} to {max(d.date for d in all_draws).date()}")

# Now run the full analysis
print("\n" + "=" * 80)
print("Running full ML analysis pipeline...")
print("=" * 80)

# Import the main analysis function
from real_data_analysis import (
    prepare_training_data,
    train_random_forest,
    run_backtest,
    calculate_pnl,
    generate_report,
    save_results_csv
)

# Phase 2: Training
X, y_numbers, y_stars, engineer, normalizer = prepare_training_data(all_draws)
rf_model, rf_time = train_random_forest(X, y_numbers, y_stars)

# Phase 3: Backtest (3 months instead of 6 for smaller dataset)
backtest_results = run_backtest(rf_model, engineer, normalizer, all_draws, months=3)

# Phase 4: PNL
pnl_results = calculate_pnl(backtest_results)

# Phase 5: Report
report_path = generate_report(
    all_draws,
    backtest_results,
    pnl_results,
    rf_time,
    lstm_training_time=0
)

csv_path = save_results_csv(backtest_results)

# Final summary
print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print(f"\n📊 Performance Report: {report_path}")
print(f"📊 Detailed Results: {csv_path}")
print(f"📊 Trained Model: /home/user/Jsprjaibon/models/random_forest_real_data.pkl")
print("\nKEY METRICS:")
print(f"  • Backtest draws: {pnl_results['total_draws']}")
print(f"  • Numbers accuracy: {backtest_results.metrics['avg_numbers_accuracy']*100:.2f}%")
print(f"  • Stars accuracy: {backtest_results.metrics['avg_stars_accuracy']*100:.2f}%")
print(f"  • Net PNL: €{pnl_results['pnl']:,.2f}")
print(f"  • ROI: {pnl_results['roi']:.2f}%")
print(f"  • Win rate: {pnl_results['win_rate']:.2f}%")
print("\n" + "=" * 80)
print("\n⚠️  DISCLAIMER: This analysis is for educational purposes only.")
print("    Lottery outcomes are random. Past performance ≠ future results.")
print("=" * 80 + "\n")
