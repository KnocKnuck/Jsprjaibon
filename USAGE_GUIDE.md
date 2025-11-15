# Euromillions ML Predictor - Usage Guide

**Version:** 0.1.0
**Last Updated:** November 2025

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Usage](#basic-usage)
- [Advanced Features](#advanced-features)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)
- [Tips & Best Practices](#tips--best-practices)

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Internet connection (for API data fetching)
- ~500MB disk space for data cache

### Quick Start

1. **Clone and Setup**
   ```bash
   cd Jsprjaibon
   pip install -r requirements.txt
   ```

2. **Initialize Configuration**
   ```bash
   cp .env.example .env
   # Edit .env if needed
   ```

3. **Fetch Initial Data**
   ```bash
   python main.py update
   ```

4. **Run Demo**
   ```bash
   python demo_full_pipeline.py
   ```

---

## Basic Usage

### Command Line Interface

The main CLI provides several commands:

```bash
python main.py [COMMAND] [OPTIONS]
```

#### Available Commands

| Command | Description |
|---------|-------------|
| `predict` | Generate predictions for next draw |
| `backtest` | Run backtest on historical data |
| `update` | Update data from API |
| `train` | Train ML models |
| `info` | Show system information |

---

### 1. Generating Predictions

**Basic prediction:**
```bash
python main.py predict
```

**With options:**
```bash
# Generate 5 grids using LSTM model
python main.py predict --grids 5 --model lstm

# Verbose output with detailed statistics
python main.py predict -g 3 --verbose

# Use Random Forest model
python main.py predict --model random_forest
```

**Output Example:**
```
=======================================================
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE
=======================================================

╭─────────── Grid 1 ────────────╮
│                                │
│  Numbers:  05 12 23 34 45      │
│  Stars:    ⭐ 03 08            │
│                                │
│  Confidence: ████████░░ 75.2%  │
│  Method: top_probabilities     │
│                                │
╰────────────────────────────────╯
```

#### Options

- `--grids, -g`: Number of grids to generate (default: 2)
- `--model, -m`: Model to use: `auto`, `lstm`, `random_forest` (default: auto)
- `--verbose`: Show detailed statistics and feature information

---

### 2. Running Backtests

**Basic backtest:**
```bash
python main.py backtest
```

**With options:**
```bash
# Backtest last 12 months
python main.py backtest --window 12

# Backtest with specific model and export results
python main.py backtest --model lstm --export results.csv

# Verbose backtest with detailed metrics
python main.py backtest -w 6 --verbose
```

**Output Example:**
```
╭─────── Backtest Summary ───────╮
│ Total Draws: 156               │
│ Avg Numbers Accuracy: 21.4%    │
│ Avg Stars Accuracy: 17.8%      │
│ Avg Confidence: 72.3%          │
╰────────────────────────────────╯

📈 Hits Distribution:
  3+1             ████░░░░░░  7.1% (11 draws)
  3+0             ██████░░░░  12.8% (20 draws)
  2+1             ████████░░  15.4% (24 draws)
  ...
```

#### Options

- `--window, -w`: Number of months to backtest (default: 6)
- `--model, -m`: Model to use (default: auto)
- `--export, -e`: Export results to CSV file
- `--verbose`: Show detailed metrics

---

### 3. Updating Data

**Basic update:**
```bash
python main.py update
```

**Force update (clear cache):**
```bash
python main.py update --force
```

**Verbose update:**
```bash
python main.py update --verbose
```

This command:
- Fetches latest draws from the API
- Updates local cache
- Shows latest draw information
- Displays cache statistics (with `--verbose`)

---

### 4. Training Models

**Train all models:**
```bash
python main.py train
```

**Train specific model:**
```bash
# Train only LSTM
python main.py train --model lstm --epochs 200

# Train only Random Forest
python main.py train --model random_forest
```

**Training script (more detailed):**
```bash
# Use the dedicated training script for full control
python train_models.py
```

#### Training Options

- `--model, -m`: Model to train: `all`, `lstm`, `random_forest` (default: all)
- `--epochs, -e`: Number of training epochs for LSTM (default: 100)
- `--save/--no-save`: Whether to save trained models (default: save)
- `--verbose`: Show detailed training progress

---

## Advanced Features

### Custom Configuration

Edit `config.yaml` to customize behavior:

```yaml
api:
  base_url: "https://euromillions.api.pedromealha.dev"
  timeout: 30
  rate_limit: 2.0
  retry_attempts: 4

data:
  cache_dir: "./data/cache"
  cache_ttl_historical: 0  # Never expire
  cache_ttl_current: 86400  # 24 hours

lottery:
  numbers_range: [1, 50]
  stars_range: [1, 12]
  numbers_count: 5
  stars_count: 2
```

### Environment Variables

Override settings with environment variables:

```bash
export EUROMILLIONS_API_TIMEOUT=60
export EUROMILLIONS_DATA_CACHE_DIR="/custom/path"
```

### Programmatic Usage

Use the library in your Python code:

```python
from config.settings import Settings
from data.loader import DataLoader
from euromillions_ml.prediction.predictor import Predictor

# Load data
settings = Settings.load_from_yaml()
loader = DataLoader(settings)
draws = loader.load_all_historical()

# Generate predictions
# (requires trained model and feature engineering setup)
# ... see demo_full_pipeline.py for complete example
```

---

## Common Workflows

### Workflow 1: First-Time Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Fetch historical data
python main.py update

# 3. Train models
python train_models.py

# 4. Generate predictions
python main.py predict --grids 3

# 5. Evaluate with backtest
python main.py backtest --window 6
```

### Workflow 2: Weekly Prediction Routine

```bash
# 1. Update data with latest draws
python main.py update

# 2. Quick info check
python main.py info

# 3. Generate predictions
python main.py predict --grids 2 --verbose
```

### Workflow 3: Model Evaluation

```bash
# 1. Train models
python train_models.py

# 2. Run comprehensive backtest
python main.py backtest --window 12 --export eval_results.csv

# 3. Analyze exported results
# Open eval_results.csv in spreadsheet software
```

### Workflow 4: Development & Testing

```bash
# 1. Run full pipeline demo
python demo_full_pipeline.py

# 2. Run Sprint 1 demo (data layer only)
python demo_sprint1.py

# 3. Run tests
pytest tests/ -v

# 4. Check logs
tail -f logs/demo.log
```

---

## Troubleshooting

### Problem: "No data available"

**Solution:**
```bash
# Update data from API
python main.py update --force
```

### Problem: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Problem: "API timeout" or connection errors

**Solutions:**
1. Check internet connection
2. Increase timeout in config.yaml:
   ```yaml
   api:
     timeout: 60  # Increase from 30
   ```
3. Use cached data:
   ```bash
   # Don't force API fetch
   python main.py predict  # Uses cache
   ```

### Problem: Models not found

**Solution:**
```bash
# Train models first
python train_models.py
```

### Problem: Prediction accuracy is low

**Expected behavior:** Lottery outcomes are fundamentally random. Typical accuracy:
- Numbers: 15-25% match rate
- Stars: 10-20% match rate

This is normal and cannot be significantly improved due to the random nature of lottery draws.

### Problem: Cache growing too large

**Solution:**
```bash
# Clear cache directory
rm -rf data/cache/*

# Re-fetch data
python main.py update
```

---

## Tips & Best Practices

### Data Management

1. **Update regularly:** Run `python main.py update` weekly to fetch latest draws
2. **Backup cache:** Periodically backup `data/cache/` directory
3. **Monitor size:** Check cache size with `python main.py info`

### Model Training

1. **Minimum data:** Wait until you have 100+ draws before training
2. **Optimal data:** 300+ draws recommended for best LSTM performance
3. **Retrain periodically:** Retrain models monthly with updated data
4. **Compare models:** Run backtests to compare LSTM vs Random Forest

### Predictions

1. **Multiple grids:** Generate 3-5 grids for variety
2. **Check confidence:** Higher confidence (>70%) indicates more "certain" predictions
3. **Use verbose mode:** `--verbose` shows feature importance and stats
4. **Don't over-rely:** Remember this is for entertainment/education only

### Performance

1. **First run is slow:** Initial data fetch takes 5-10 minutes
2. **Cache helps:** Subsequent runs use cached data (much faster)
3. **LSTM is slower:** LSTM training/prediction slower than Random Forest
4. **Backtest takes time:** Large backtests (12+ months) can take several minutes

### Logging

1. **Check logs:** Review `logs/*.log` for debugging
2. **Log levels:** Edit logging level in code for more/less detail
3. **Structured logs:** Logs use structured format for easy parsing

---

## File Structure

```
Jsprjaibon/
├── main.py                    # Main CLI entry point
├── train_models.py            # Training script
├── demo_full_pipeline.py      # Full pipeline demo
├── demo_sprint1.py           # Data layer demo
│
├── config.yaml               # Configuration file
├── .env                      # Environment variables
│
├── config/                   # Configuration module
├── data/                     # Data loading & caching
├── euromillions_ml/         # Core ML package
│   ├── features/            # Feature engineering
│   ├── models/              # ML models
│   ├── prediction/          # Prediction engine
│   └── utils/               # Utilities & display
│
├── tests/                   # Test suite
├── logs/                    # Log files
├── models/                  # Saved model files
└── data/cache/             # Data cache
```

---

## Getting Help

- **Documentation:** See `README.md` and other docs in repository root
- **Logs:** Check `logs/` directory for error details
- **Issues:** Check GitHub issues for known problems
- **Verbose mode:** Use `--verbose` flag for detailed output

---

## Important Disclaimer

**This tool is for entertainment and educational purposes only.**

- Lottery outcomes are fundamentally random
- No prediction system can reliably forecast lottery results
- Past patterns do not predict future outcomes
- Please gamble responsibly and within your means

The ML models in this system are designed to demonstrate machine learning techniques, not to provide actionable lottery predictions.

---

## Version History

- **v0.1.0** (November 2025)
  - Initial release
  - Sprint 1: Data foundation
  - Basic prediction and backtest functionality
  - CLI interface

---

For more information, see:
- `README.md` - Project overview
- `ARCHITECTURE.md` - System architecture
- `PROJECT_PLAN.md` - Development roadmap
- `FINAL_REPORT.md` - Complete project report
