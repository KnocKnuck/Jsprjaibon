# 🎰 Euromillions ML Predictor

**AI-powered lottery prediction system using machine learning and statistical analysis**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## ⚠️ Disclaimer

**This is an educational project for learning ML and data analysis.**
- Lottery games are games of chance with independent random draws
- Past results DO NOT predict future outcomes
- This tool is for entertainment and educational purposes only
- Never gamble more than you can afford to lose
- Gambling can be addictive - please play responsibly

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Architecture](#-architecture)
- [Configuration](#-configuration)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Capabilities
- 🎯 **Dual-Mode Prediction**: LSTM neural networks + Random Forest ensemble
- 📊 **Historical Analysis**: 20+ years of Euromillions data (2004-2025)
- 🔄 **Auto-Updates**: Automated data fetching from REST API
- 📈 **Backtesting**: Validate model performance on historical draws
- 🎨 **Beautiful Terminal UI**: Rich formatting with progress bars and charts
- 🔐 **Production-Ready**: Robust error handling, caching, logging, retry logic

### ML Features
- **Feature Engineering**: 200+ statistical features (frequencies, patterns, delays)
- **Model Selection**: Auto-selects LSTM (300+ draws) or Random Forest
- **Confidence Scoring**: Probability-based predictions with confidence metrics
- **Progressive Disclosure**: Quick view (numbers only) or detailed analysis

### UX Features
- **First-Run Wizard**: Interactive setup for new users
- **Multiple Output Modes**: Quiet, normal, verbose
- **Data Freshness Warnings**: Alerts when data is stale
- **Export Options**: JSON, CSV, Markdown reports

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- 4GB RAM minimum (8GB recommended for LSTM)
- Internet connection (for API access)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/euromillions-ml.git
cd euromillions-ml

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run setup wizard
python main.py setup
```

### First Prediction

```bash
# Generate 2 predictions for next draw
python main.py predict

# With verbose output
python main.py predict --verbose

# Quick mode (numbers only)
python main.py predict --quiet
```

---

## 📦 Installation

### Standard Installation

```bash
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pre-commit install
```

### Optional: GPU Support (for LSTM)

```bash
pip install tensorflow[and-cuda]>=2.13.0
```

---

## 📖 Usage

### Commands

#### Predict Mode
Generate predictions for the next draw:

```bash
# Basic prediction (2 grids)
python main.py predict

# Specify number of grids
python main.py predict --grids 5

# Choose model
python main.py predict --model lstm
python main.py predict --model random_forest
python main.py predict --model auto  # (default)

# Output options
python main.py predict --quiet       # Numbers only
python main.py predict --verbose     # Detailed analysis
python main.py predict --output predictions.json
```

#### Backtest Mode
Validate model performance:

```bash
# Backtest last 6 months
python main.py backtest --window 6

# Backtest specific date range
python main.py backtest --start 2024-01-01 --end 2024-12-31

# Generate detailed report
python main.py backtest --window 12 --export backtest_report.csv
```

#### Data Management

```bash
# Update data from API
python main.py update

# Validate cached data
python main.py validate

# Show data statistics
python main.py stats
```

#### Utilities

```bash
# First-time setup wizard
python main.py setup

# System health check
python main.py health

# View configuration
python main.py config --show

# Clean cache
python main.py cache --clear
```

---

## 🏗️ Architecture

### Project Structure

```
euromillions_ml/
├── data/           # Data acquisition (API client, caching, validation)
├── features/       # Feature engineering and normalization
├── models/         # ML models (LSTM, Random Forest, registry)
├── prediction/     # Prediction engine and backtesting
├── utils/          # Utilities (display, metrics, logging)
└── config/         # Configuration and settings
```

### Data Flow

```
API Client → Cache → Validator → Feature Engineering → Model → Predictor → Terminal Display
```

### Tech Stack

- **ML**: TensorFlow/Keras (LSTM), Scikit-learn (Random Forest)
- **Data**: NumPy, Pandas, Diskcache
- **CLI**: Typer, Rich
- **Config**: Pydantic, PyYAML
- **Testing**: Pytest, Coverage
- **Quality**: Black, Flake8, MyPy

---

## ⚙️ Configuration

### config.yaml

```yaml
api:
  base_url: "https://euromillions.api.pedromealha.dev"
  rate_limit: 2  # seconds between requests

models:
  default_model: "auto"  # auto, lstm, random_forest
  lstm_threshold: 300    # minimum draws for LSTM

output:
  verbosity: "normal"    # quiet, normal, verbose
  color_theme: "dark"    # dark, light, high-contrast
```

### Environment Variables

Create `.env` file:

```env
EUROMILLIONS_API_URL=https://euromillions.api.pedromealha.dev
LOG_LEVEL=INFO
DEBUG=false
```

---

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=euromillions_ml --cov-report=html

# Specific test file
pytest tests/test_data/test_api_client.py
```

### Code Quality

```bash
# Format code
black euromillions_ml/

# Sort imports
isort euromillions_ml/

# Lint
flake8 euromillions_ml/

# Type check
mypy euromillions_ml/
```

### Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

---

## 📊 Example Output

### Prediction Mode

```
═══════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE
═══════════════════════════════════════════════════════

📊 Training Data: 287 draws | 🤖 Model: LSTM
📈 Accuracy: 82.4% | Period: 2024-01-01 → 2024-11-15

───────────────────────────────────────────────────────
  GRILLE 1 (High Confidence)
───────────────────────────────────────────────────────

  ┏━━━┓ ┏━━━┓ ┏━━━┓ ┏━━━┓ ┏━━━┓     ┏━━━┓ ┏━━━┓
  ┃ 7 ┃ ┃14 ┃ ┃23 ┃ ┃38 ┃ ┃49 ┃  ⭐ ┃ 5 ┃ ┃ 9 ┃
  ┗━━━┛ ┗━━━┛ ┗━━━┛ ┗━━━┛ ┗━━━┛     ┗━━━┛ ┗━━━┛

  Confidence: ████████░░ 82%
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Run pre-commit hooks

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 🙏 Acknowledgments

- **Data Source**: [pedro-mealha/euromillions-api](https://github.com/pedro-mealha/euromillions-api)
- **Inspiration**: Statistical analysis and machine learning communities

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/euromillions-ml/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/euromillions-ml/discussions)

---

**Remember: This is for educational purposes only. Gamble responsibly! 🎲**
