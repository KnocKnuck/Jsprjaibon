# 🚀 Quick Start Guide - Euromillions ML Predictor

**Get up and running in 5 minutes!**

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- **Git** installed ([Download](https://git-scm.com/downloads))
- **4GB RAM minimum** (8GB recommended for LSTM training)
- **Internet connection** (for API access)

### Check Your Python Version

```bash
python --version
# Should show: Python 3.9.x or higher
```

---

## 🛠️ Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the project
git clone https://github.com/KnocKnuck/Jsprjaibon.git

# Navigate to the project directory
cd Jsprjaibon

# Switch to the feature branch
git checkout claude/euromillions-ml-predictor-01FnZh38PtsYFTs3KDnLeFf3
```

### Step 2: Create Virtual Environment

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**Verify activation:**
You should see `(venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements-dev.txt
```

**Installation time:** ~2-5 minutes (depending on internet speed)

### Step 4: Create Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (optional - defaults work fine)
# nano .env  # or use your favorite editor
```

### Step 5: Verify Installation

```bash
# Test the CLI
python main.py --version

# Should output: Euromillions ML Predictor v0.1.0
```

---

## 🎯 First Steps - What Works Now

### Current Status (Sprint 1 Complete)

✅ **Working:**
- API client with retry logic
- Data caching system
- Configuration management
- Data validation
- Logging system

⏳ **Coming in Sprint 2-5:**
- ML models (LSTM, Random Forest)
- Prediction mode
- Backtest mode
- Feature engineering

### Test the Data Loader

```bash
# Run the Sprint 1 demo
python demo_sprint1.py
```

**What this does:**
1. Loads configuration from `config.yaml`
2. Connects to the Euromillions API
3. Fetches recent draws with caching
4. Validates all data
5. Displays results in terminal

**Expected output:**
```
✓ Configuration loaded
✓ API client initialized
✓ Fetching draws from API...
✓ Successfully loaded 52 draws
✓ Data cached for future use

Latest Draw:
  Date: 2024-11-12
  Numbers: [7, 14, 23, 38, 49]
  Stars: [5, 9]
```

**Check logs:**
```bash
cat logs/demo.log
```

---

## 📚 Understanding the Project Structure

```
Jsprjaibon/
├── 📁 euromillions_ml/        # Main application package
│   ├── 📁 data/               # ✅ IMPLEMENTED - API client, caching
│   ├── 📁 features/           # ⏳ Sprint 2 - Feature engineering
│   ├── 📁 models/             # ⏳ Sprint 2 - ML models
│   ├── 📁 prediction/         # ⏳ Sprint 3 - Prediction engine
│   ├── 📁 utils/              # ✅ IMPLEMENTED - Logging, display
│   └── 📁 config/             # ✅ IMPLEMENTED - Settings
├── 📁 data/                   # Data storage
│   ├── cache/                 # Cached API responses
│   ├── raw/                   # Raw downloaded data
│   └── processed/             # Processed datasets
├── 📁 models/                 # Saved trained models (empty for now)
├── 📁 logs/                   # Application logs
├── 📁 tests/                  # Test suite
├── 📄 config.yaml             # Configuration file
├── 📄 main.py                 # CLI entry point
└── 📄 requirements.txt        # Dependencies
```

---

## 🔧 Configuration

### Default Configuration (`config.yaml`)

The default configuration works out of the box. Key settings:

```yaml
api:
  base_url: "https://euromillions.api.pedromealha.dev"
  rate_limit: 2              # Seconds between requests
  retry_attempts: 4          # Retry on network errors

data:
  cache_dir: "./data/cache"  # Where to cache API data

output:
  verbosity: "normal"        # quiet | normal | verbose
  color_theme: "dark"        # dark | light | high-contrast
```

### Customization

**Change verbosity:**
```yaml
output:
  verbosity: "verbose"  # Show detailed information
```

**Adjust cache settings:**
```yaml
data:
  cache_ttl_current_year: 3600  # 1 hour instead of 24 hours
```

**Environment variables override:**
Create `.env` file:
```env
EUROMILLIONS_API_URL=https://euromillions.api.pedromealha.dev
LOG_LEVEL=DEBUG
```

---

## 🎮 Available Commands (Current Sprint)

### CLI Commands

```bash
# Show version
python main.py --version

# Show help
python main.py --help

# Update data from API
python main.py update

# Show system information
python main.py info
```

### Coming Soon (Sprint 2-5)

```bash
# Generate predictions (Sprint 3)
python main.py predict --grids 2

# Run backtest (Sprint 4)
python main.py backtest --window 6

# Train models (Sprint 2)
python main.py train --model lstm
```

---

## 🧪 Testing the Installation

### Run Basic Tests

```bash
# Test the data loader
python demo_sprint1.py

# Expected: Successfully loads draws and displays latest
```

### Check Logs

```bash
# View application logs
cat logs/demo.log

# Monitor logs in real-time (macOS/Linux)
tail -f logs/euromillions.log
```

### Verify Cache

```bash
# Check cache directory
ls -la data/cache/

# You should see cache files after running demo_sprint1.py
```

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError`

**Problem:** Dependencies not installed

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `403 Forbidden` from API

**Problem:** API endpoint blocked

**Solution:**
The pedro-mealha API may have rate limiting. The client has automatic retry built-in. If persistent:

1. Check your internet connection
2. Wait 5 minutes and try again
3. Check API status: https://github.com/pedro-mealha/euromillions-api

**Alternative:** Self-host the API (see DATA_SOURCES.md)

### Issue: `FileNotFoundError: config.yaml`

**Problem:** Running from wrong directory

**Solution:**
```bash
# Always run from project root
cd /path/to/Jsprjaibon
python demo_sprint1.py
```

### Issue: Python version error

**Problem:** Python version < 3.9

**Solution:**
```bash
# Install Python 3.9+ from python.org
# Or use pyenv to manage versions
pyenv install 3.9.0
pyenv local 3.9.0
```

### Issue: Permission denied on logs/

**Solution:**
```bash
# Create logs directory if missing
mkdir -p logs

# Fix permissions (macOS/Linux)
chmod 755 logs
```

---

## 📖 Next Steps

### 1. Explore the Documentation

- **README.md** - Full project overview
- **ARCHITECTURE.md** - Technical architecture
- **DATA_SOURCES.md** - Data source details
- **AUDIT_SUMMARY.md** - Quality audit findings

### 2. Review the Sprint Plan

- **Sprint 1** ✅ Complete - Data foundation
- **Sprint 2** ⏳ Next - ML models (LSTM, Random Forest)
- **Sprint 3** ⏳ Prediction mode
- **Sprint 4** ⏳ Backtest mode
- **Sprint 5** ⏳ Polish & documentation

### 3. Stay Updated

```bash
# Pull latest changes
git pull origin claude/euromillions-ml-predictor-01FnZh38PtsYFTs3KDnLeFf3

# Reinstall dependencies if updated
pip install -r requirements.txt --upgrade
```

### 4. Development Mode (Optional)

If you want to contribute or develop:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests (when available)
pytest

# Format code
black euromillions_ml/
isort euromillions_ml/
```

---

## 🔮 What's Coming Next

### Sprint 2: ML Models (Weeks 3-4)

We'll implement:
- Feature engineering (200+ statistical features)
- LSTM neural network model
- Random Forest ensemble model
- Model versioning and registry

**Timeline:** 2-3 weeks

### Sprint 3: Prediction Mode (Weeks 5-6)

You'll be able to:
```bash
python main.py predict --grids 2
```

Output:
```
🎰 PREDICTED GRIDS

Grid 1: [7, 14, 23, 38, 49] ⭐ [5, 9]
Confidence: 82%

Grid 2: [3, 19, 27, 41, 50] ⭐ [2, 11]
Confidence: 74%
```

### Sprint 4: Backtest Mode (Weeks 7-8)

Validate model accuracy:
```bash
python main.py backtest --window 6
```

### Sprint 5: Polish (Weeks 9-10)

- Enhanced terminal UI
- Export to CSV/JSON
- Statistics dashboard
- Performance optimization

---

## 💬 Getting Help

### Resources

- **GitHub Issues:** [Report bugs](https://github.com/KnocKnuck/Jsprjaibon/issues)
- **Documentation:** Check the `docs/` folder
- **Logs:** Always check `logs/euromillions.log` first

### Common Questions

**Q: How much historical data is available?**
A: 2004-2025 (21+ years, ~2,200 draws)

**Q: Can I use this for other lotteries?**
A: Not yet, but it's planned for v2.0

**Q: Is the API free?**
A: Yes, pedro-mealha's API is MIT licensed and free

**Q: How accurate are the predictions?**
A: ML models not yet implemented. Accuracy will be measured in Sprint 4 backtest.

**Q: Can I run this offline?**
A: After initial data download, cached data works offline. Models will work offline once trained.

---

## ⚠️ Important Reminders

1. **Educational Purpose Only:** This is a learning project for ML and data analysis
2. **Gambling Warning:** Lottery is random - past results don't predict future
3. **Responsible Gaming:** Never gamble more than you can afford to lose
4. **Data Source:** Thanks to pedro-mealha for the excellent API
5. **Work in Progress:** Only Sprint 1 complete, more features coming!

---

## 📊 Installation Checklist

Use this to verify your setup:

- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Correct branch checked out (`claude/euromillions-ml-predictor-01FnZh38PtsYFTs3KDnLeFf3`)
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed (`requirements.txt`)
- [ ] `.env` file created (from `.env.example`)
- [ ] `python main.py --version` works
- [ ] `python demo_sprint1.py` runs successfully
- [ ] Logs created in `logs/` directory
- [ ] Cache created in `data/cache/` directory

**All checked?** 🎉 You're ready to go!

---

## 🎯 Quick Reference

```bash
# Clone
git clone https://github.com/KnocKnuck/Jsprjaibon.git
cd Jsprjaibon
git checkout claude/euromillions-ml-predictor-01FnZh38PtsYFTs3KDnLeFf3

# Setup
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Test
python demo_sprint1.py

# Run
python main.py --help
```

**Total setup time:** ~5-10 minutes

---

**Need help?** Check the troubleshooting section above or open an issue on GitHub!

**Ready for more?** Review the full README.md and ARCHITECTURE.md for deeper understanding.

---

*Last Updated: 2025-11-15*
*Sprint 1 Complete - Data Foundation ✅*
*Next: Sprint 2 - ML Models ⏳*
