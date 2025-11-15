# EuroMillions Prediction & Backtest Engine Documentation

## Overview

This document explains how the prediction and backtest engines work in the EuroMillions ML Predictor system. These components are the core of Sprint 3 (Prediction) and Sprint 4 (Backtest).

## Table of Contents

1. [Architecture](#architecture)
2. [Prediction Engine](#prediction-engine)
3. [Backtest Engine](#backtest-engine)
4. [Usage Examples](#usage-examples)
5. [API Reference](#api-reference)
6. [Performance Metrics](#performance-metrics)

---

## Architecture

The prediction system consists of several components:

```
┌─────────────────────┐
│   Historical Data   │
│    (DataLoader)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│Feature Engineering  │
│  (FeatureEngineer)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Normalization     │
│(FeatureNormalizer)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    ML Model         │
│  (BaseModel impl)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Predictor Engine   │
│   (Predictor)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Prediction Grids    │
└─────────────────────┘
```

---

## Prediction Engine

### How It Works

The prediction engine generates EuroMillions grids using a hybrid approach:

1. **ML Model Predictions**: Uses trained models (LSTM, Random Forest) to predict number probabilities
2. **Statistical Analysis**: Calculates frequency-based probabilities from historical data
3. **Probability Fusion**: Combines ML and statistical predictions (50/50 weighted)
4. **Grid Generation**: Uses different strategies to generate diverse predictions

### Generation Strategies

#### 1. Top Probabilities (Grid 1)
- Selects the numbers and stars with highest combined probabilities
- Most conservative approach
- Highest confidence scores

#### 2. Weighted Sampling (Grid 2+)
- Random sampling weighted by probabilities
- More diverse predictions
- Balances exploration vs exploitation

### Code Example

```python
from euromillions_ml.prediction.predictor import Predictor
from euromillions_ml.models.dummy import DummyModel
from euromillions_ml.features.engineering import FeatureEngineer
from euromillions_ml.features.normalizer import FeatureNormalizer
from euromillions_ml.data.loader import DataLoader
from euromillions_ml.config.settings import Settings

# Load data
settings = Settings()
loader = DataLoader(settings)
draws = loader.load_all_historical(use_cache=True)

# Initialize components
model = DummyModel()  # Replace with trained model
feature_engineer = FeatureEngineer()
normalizer = FeatureNormalizer()

# Extract and normalize features
features = feature_engineer.extract_all_features(draws)
normalizer.fit(features)

# Create predictor
predictor = Predictor(model, feature_engineer, normalizer)

# Generate predictions
grids = predictor.predict(draws, n_grids=3)

# Display results
for i, grid in enumerate(grids, 1):
    print(f"Grid {i}: {grid.numbers} + {grid.stars} ({grid.confidence:.2%})")
```

### Validation Rules

All predictions are validated to ensure:
- Exactly 5 numbers between 1-50 (no duplicates)
- Exactly 2 stars between 1-12 (no duplicates)
- Numbers and stars are sorted
- Confidence scores between 0-1

---

## Backtest Engine

### How It Works

The backtest engine evaluates model performance on historical data using walk-forward validation:

1. **Time-Based Splitting**: For each test draw, only uses data BEFORE that draw for training
2. **Prediction Generation**: Generates predictions for each test draw
3. **Comparison**: Compares predictions to actual results
4. **Metrics Calculation**: Computes accuracy and hit distribution

### Metrics

#### Accuracy Metrics
- **Numbers Accuracy**: Average percentage of numbers matched (0-100%)
- **Stars Accuracy**: Average percentage of stars matched (0-100%)
- **Confidence**: Average model confidence scores

#### Hit Distribution
Shows the frequency of different match patterns:
- `0+0`: No matches
- `1+0`: 1 number match, 0 stars
- `2+1`: 2 numbers, 1 star
- `3+2`: 3 numbers, 2 stars (jackpot pattern: 5+2)
- etc.

### Code Example

```python
from euromillions_ml.prediction.backtest import BacktestEngine

# Create backtest engine (using predictor from above)
backtest_engine = BacktestEngine(predictor)

# Run backtest on last 6 months
result = backtest_engine.run_backtest(draws, window_months=6)

# Display metrics
print(f"Total draws tested: {result.metrics['total_draws']}")
print(f"Numbers accuracy: {result.metrics['avg_numbers_accuracy']:.2%}")
print(f"Stars accuracy: {result.metrics['avg_stars_accuracy']:.2%}")
print(f"\nHit distribution:")
for pattern, count in result.metrics['hits_distribution'].items():
    print(f"  {pattern}: {count}")

# Export to CSV
df = result.to_dataframe()
df.to_csv('backtest_results.csv', index=False)
```

### Walk-Forward Validation

For more robust testing, use walk-forward validation:

```python
# Split data into multiple folds
results = backtest_engine.walk_forward_validation(
    draws,
    test_size=50,   # 50 draws per test fold
    step_size=10    # Move forward 10 draws each fold
)

# Analyze across all folds
avg_accuracy = sum(r.metrics['avg_numbers_accuracy'] for r in results) / len(results)
print(f"Average accuracy across {len(results)} folds: {avg_accuracy:.2%}")
```

---

## Usage Examples

### Command Line Interface

```bash
# Generate predictions
python cli_predict_backtest.py predict --grids 5

# Run backtest
python cli_predict_backtest.py backtest --window 12 --export results.csv

# Verbose output
python cli_predict_backtest.py predict --grids 3 --verbose
```

### Running Example Script

```bash
# Run the complete example
python example_prediction.py
```

This will:
1. Load historical data
2. Extract features
3. Generate 3 prediction grids
4. Run a 3-month backtest
5. Export results to CSV

---

## API Reference

### PredictionGrid

Represents a single prediction grid.

**Attributes:**
- `numbers: List[int]` - 5 predicted numbers (1-50)
- `stars: List[int]` - 2 predicted stars (1-12)
- `confidence: float` - Confidence score (0-1)
- `method: str` - Generation method used
- `generated_at: datetime` - Timestamp

**Methods:**
- `to_dict() -> dict` - Convert to dictionary
- `__str__() -> str` - Human-readable representation

### Predictor

Main prediction engine.

**Constructor:**
```python
Predictor(model: BaseModel, feature_engineer: FeatureEngineer, normalizer: FeatureNormalizer)
```

**Methods:**
- `predict(draws: List[Draw], n_grids: int = 2) -> List[PredictionGrid]`
  - Generate N prediction grids
  - Returns list of PredictionGrid objects

### BacktestEngine

Backtesting and validation engine.

**Constructor:**
```python
BacktestEngine(predictor: Predictor)
```

**Methods:**
- `run_backtest(draws, start_date=None, end_date=None, window_months=None, min_training_draws=50) -> BacktestResult`
  - Run backtest on specified period
  - Returns BacktestResult with metrics

- `walk_forward_validation(draws, test_size=50, step_size=10) -> List[BacktestResult]`
  - Perform walk-forward validation
  - Returns list of BacktestResult for each fold

### BacktestResult

Container for backtest results.

**Attributes:**
- `predictions: List[PredictionGrid]` - All predictions made
- `actuals: List[Draw]` - Actual draw results
- `metrics: dict` - Performance metrics
- `hits_distribution: dict` - Match pattern frequencies

**Methods:**
- `calculate_metrics()` - Compute all metrics
- `to_dataframe() -> pd.DataFrame` - Convert to DataFrame
- `__repr__() -> str` - Summary representation

---

## Performance Metrics

### Expected Performance (DummyModel)

Since DummyModel uses random predictions:
- **Numbers Accuracy**: ~10% (1 in 10 numbers match)
- **Stars Accuracy**: ~17% (1 in 6 stars match)
- **Most Common Pattern**: 0+0, 1+0

### Expected Performance (Trained Models)

With properly trained ML models:
- **Numbers Accuracy**: 15-25% (better than random)
- **Stars Accuracy**: 20-35% (better than random)
- **Jackpot Pattern (5+2)**: Extremely rare (1 in 139 million)

### Baseline Comparison

Random selection:
- Numbers: 10% accuracy (5/50)
- Stars: 16.7% accuracy (2/12)

Any model performing significantly above baseline demonstrates learned patterns.

---

## Integration with ML Models

### Using Real Models

To use trained models instead of DummyModel:

```python
from euromillions_ml.models.lstm import LSTMModel  # When implemented

# Load trained model
model = LSTMModel.load('models/lstm_trained.pkl')

# Use with predictor
predictor = Predictor(model, feature_engineer, normalizer)
grids = predictor.predict(draws, n_grids=5)
```

### Training Pipeline

```python
# 1. Load and prepare data
draws = loader.load_all_historical()
features = feature_engineer.extract_all_features(draws)

# 2. Split data
train_size = int(len(features) * 0.8)
X_train = features[:train_size]
X_test = features[train_size:]

# 3. Normalize
normalizer.fit(X_train)
X_train_norm = normalizer.transform(X_train)

# 4. Train model
model = LSTMModel()
model.train(X_train_norm, y_numbers, y_stars)

# 5. Evaluate
predictor = Predictor(model, feature_engineer, normalizer)
backtest_engine = BacktestEngine(predictor)
result = backtest_engine.run_backtest(draws, window_months=6)
```

---

## Testing

Run the test suite:

```bash
# Test prediction engine
pytest tests/test_prediction/test_predictor.py -v

# Test backtest engine
pytest tests/test_prediction/test_backtest.py -v

# Run all prediction tests
pytest tests/test_prediction/ -v
```

---

## Troubleshooting

### Common Issues

**Issue**: `ValueError: Not enough historical data`
- **Solution**: Ensure at least 100 draws are available. The feature engineer needs minimum data.

**Issue**: Normalizer not fitted
- **Solution**: Call `normalizer.fit(features)` before using predictor.

**Issue**: Low accuracy in backtest
- **Solution**: This is expected with DummyModel. Train actual ML models for better results.

**Issue**: Memory errors with large backtests
- **Solution**: Use smaller windows or walk-forward validation with smaller test sizes.

---

## Future Improvements

1. **Advanced Models**: Implement LSTM and Random Forest models
2. **Ensemble Predictions**: Combine multiple models
3. **Pattern Analysis**: Identify hot/cold numbers
4. **Probability Calibration**: Better confidence scores
5. **Real-time Updates**: Automatic data refresh
6. **API Endpoints**: REST API for predictions

---

## References

- EuroMillions Rules: 5 numbers (1-50) + 2 stars (1-12)
- Win probability (jackpot): 1 in 139,838,160
- Data source: pedro-mealha/euromillions-api

---

## License

MIT License - For educational and research purposes only.

**Disclaimer**: Lottery outcomes are random and cannot be predicted with certainty. This tool is for entertainment and educational purposes only.
