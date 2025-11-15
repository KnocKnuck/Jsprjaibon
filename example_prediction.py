#!/usr/bin/env python3
"""
Example script demonstrating the prediction and backtest engines

This script shows how to:
1. Load historical data
2. Initialize the prediction pipeline
3. Generate predictions
4. Run backtests
5. Analyze results
"""

from euromillions_ml.config.settings import Settings
from euromillions_ml.data.loader import DataLoader
from euromillions_ml.models.dummy import DummyModel
from euromillions_ml.features.engineering import FeatureEngineer
from euromillions_ml.features.normalizer import FeatureNormalizer
from euromillions_ml.prediction.predictor import Predictor
from euromillions_ml.prediction.backtest import BacktestEngine


def main():
    print("=" * 60)
    print("EuroMillions ML Predictor - Example Demo")
    print("=" * 60)
    print()

    # 1. Load historical data
    print("1. Loading historical data...")
    settings = Settings()
    loader = DataLoader(settings)
    draws = loader.load_all_historical(use_cache=True)
    print(f"   Loaded {len(draws)} historical draws")
    print(f"   Date range: {min(d.date for d in draws)} to {max(d.date for d in draws)}")
    print()

    # 2. Initialize components
    print("2. Initializing prediction components...")
    model = DummyModel()
    feature_engineer = FeatureEngineer()
    normalizer = FeatureNormalizer()
    print(f"   Model: {model.name}")
    print(f"   Model trained: {model.trained}")
    print()

    # 3. Extract and normalize features
    print("3. Feature engineering...")
    features = feature_engineer.extract_all_features(draws)
    print(f"   Extracted features shape: {features.shape}")
    print(f"   Number of features: {len(feature_engineer.get_feature_names())}")
    print(f"   Sample features: {feature_engineer.get_feature_names()[:5]}")
    print()

    print("4. Normalizing features...")
    normalizer.fit(features)
    features_normalized = normalizer.transform(features)
    print(f"   Normalized features shape: {features_normalized.shape}")
    print()

    # 5. Create predictor
    print("5. Creating predictor...")
    predictor = Predictor(model, feature_engineer, normalizer)
    print("   Predictor initialized")
    print()

    # 6. Generate predictions
    print("6. Generating predictions...")
    n_grids = 3
    prediction_grids = predictor.predict(draws, n_grids=n_grids)
    print(f"   Generated {len(prediction_grids)} prediction grids:")
    print()
    for i, grid in enumerate(prediction_grids, 1):
        print(f"   Grid #{i}:")
        print(f"     Numbers: {grid.numbers}")
        print(f"     Stars: {grid.stars}")
        print(f"     Confidence: {grid.confidence:.2%}")
        print(f"     Method: {grid.method}")
        print()

    # 7. Run backtest
    print("7. Running backtest...")
    backtest_engine = BacktestEngine(predictor)
    result = backtest_engine.run_backtest(draws, window_months=3)
    print()

    # 8. Display backtest results
    print("8. Backtest Results:")
    print(f"   Total draws tested: {result.metrics['total_draws']}")
    print(f"   Avg numbers accuracy: {result.metrics['avg_numbers_accuracy']:.2%}")
    print(f"   Avg stars accuracy: {result.metrics['avg_stars_accuracy']:.2%}")
    print(f"   Avg confidence: {result.metrics['avg_confidence']:.2%}")
    print()

    print("   Hits distribution:")
    for pattern, count in sorted(result.metrics['hits_distribution'].items(), reverse=True):
        percentage = count / result.metrics['total_draws'] * 100
        print(f"     {pattern}: {count} ({percentage:.1f}%)")
    print()

    if result.metrics['best_prediction']:
        best = result.metrics['best_prediction']
        print("   Best prediction:")
        print(f"     Date: {best['date']}")
        print(f"     Predicted: {best['predicted_numbers']} + {best['predicted_stars']}")
        print(f"     Actual: {best['actual_numbers']} + {best['actual_stars']}")
        print(f"     Hits: {best['numbers_hit']} numbers + {best['stars_hit']} stars")
        print()

    # 9. Export results
    print("9. Exporting results...")
    df = result.to_dataframe()
    output_file = "/home/user/Jsprjaibon/backtest_results.csv"
    df.to_csv(output_file, index=False)
    print(f"   Results exported to: {output_file}")
    print()

    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)
    print()
    print("Note: This demo uses DummyModel which generates random predictions.")
    print("For better predictions, train actual ML models (LSTM, Random Forest).")
    print()


if __name__ == "__main__":
    main()
