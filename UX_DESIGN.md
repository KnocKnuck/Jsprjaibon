# UX Design Document
## Euromillions ML Predictor - Terminal Interface

---

## 1. UX Principles

### 1.1 Clarity
- **Clear Information Hierarchy**: Use visual separators and spacing to distinguish sections
- **Concise Text**: Display essential information without overwhelming the user
- **Meaningful Labels**: Use descriptive labels for all data points
- **Progressive Disclosure**: Show summary first, details on demand

### 1.2 Feedback
- **Immediate Response**: Acknowledge every user action instantly
- **Progress Indicators**: Show loading states for long-running operations
- **Clear Error Messages**: Provide actionable error information
- **Success Confirmation**: Clearly indicate successful operations

### 1.3 Consistency
- **Uniform Formatting**: Maintain consistent spacing, alignment, and typography
- **Predictable Structure**: Keep layout consistent across different modes
- **Standard Color Coding**: Use consistent colors for status types
- **Repeatable Patterns**: Use the same design patterns throughout

---

## 2. Design System

### 2.1 Character Palette

```python
CHARS = {
    # Separators
    'separator_heavy': '═',
    'separator_light': '─',
    'separator_dotted': '·',

    # Boxes
    'box_top_left': '╔',
    'box_top_right': '╗',
    'box_bottom_left': '╚',
    'box_bottom_right': '╝',
    'box_vertical': '║',
    'box_horizontal': '═',

    # Bullets & Icons
    'bullet': '•',
    'arrow_right': '→',
    'arrow_up': '↑',
    'arrow_down': '↓',
    'check': '✓',
    'cross': '✗',

    # Progress Bars
    'bar_full': '█',
    'bar_three_quarters': '▓',
    'bar_half': '▒',
    'bar_quarter': '░',
    'bar_empty': '░',

    # Charts
    'chart_bar': '█',
    'chart_dot': '●',
    'chart_line': '─',
    'chart_vertical': '│',
}
```

### 2.2 Color Codes (ANSI)

```python
COLORS = {
    # Status Colors
    'success': '\033[92m',      # Bright Green
    'error': '\033[91m',        # Bright Red
    'warning': '\033[93m',      # Bright Yellow
    'info': '\033[94m',         # Bright Blue

    # Emphasis
    'bold': '\033[1m',
    'dim': '\033[2m',
    'underline': '\033[4m',

    # Data Colors
    'primary': '\033[96m',      # Cyan (for main numbers)
    'secondary': '\033[95m',    # Magenta (for stars)
    'neutral': '\033[37m',      # White

    # Reset
    'reset': '\033[0m',
}
```

### 2.3 Emoji Usage

```python
EMOJIS = {
    # Headers
    'lottery': '🎰',
    'ml': '🤖',
    'chart': '📊',
    'calendar': '📅',
    'clock': '⏱️',

    # Status
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',

    # Numbers & Data
    'numbers': '🔢',
    'star': '⭐',
    'target': '🎯',
    'trophy': '🏆',

    # Actions
    'rocket': '🚀',
    'gear': '⚙️',
    'magnifying_glass': '🔍',
    'sparkles': '✨',
}
```

### 2.4 Typography Hierarchy

```
LEVEL 1 (Main Title):
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - [MODE NAME]
═══════════════════════════════════════════════════════════════════════

LEVEL 2 (Section Header):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SECTION TITLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEVEL 3 (Subsection):
─────────────────────────────────────────────────────────────────────
▸ Subsection Title
─────────────────────────────────────────────────────────────────────

LEVEL 4 (Label):
• Label: Value
```

---

## 3. Terminal UI Mockups

### 3.1 Prediction Mode - Complete Output

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE
═══════════════════════════════════════════════════════════════════════

📊 Model Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Training Data:    287 historical draws
  • Model Type:       LSTM Neural Network
  • Training Period:  2024-01-01 → 2024-11-15
  • Last Updated:     2024-11-15 14:32:18
  • Model Accuracy:   67.3% (last 100 draws)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Predicted Numbers for Next Draw
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Main Numbers (5):
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │            07    14    23    38    42                           │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Stars (2):
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │                ⭐ 03      ⭐ 09                                  │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Confidence Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Overall Confidence:  ████████████████░░░░ 82%

  Individual Number Confidence:
  ┌─────────────────────────────────────────────────────────────────┐
  │  07  →  ████████████████████░ 95%   (Very High)                │
  │  14  →  █████████████████░░░░ 87%   (High)                     │
  │  23  →  ███████████████░░░░░░ 76%   (Medium-High)              │
  │  38  →  ████████████░░░░░░░░░ 68%   (Medium)                   │
  │  42  →  ███████████░░░░░░░░░░ 61%   (Medium)                   │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Star Confidence:
  ┌─────────────────────────────────────────────────────────────────┐
  │  03  →  ██████████████████░░░ 89%   (High)                     │
  │  09  →  ██████████████░░░░░░░ 73%   (Medium-High)              │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Pattern Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Number Distribution:  Balanced (2 low, 3 high)
  • Odd/Even Ratio:       3:2 (60% odd)
  • Sum of Numbers:       124 (within optimal range: 95-165)
  • Consecutive Numbers:  None
  • Hot Numbers Used:     3/5 (07, 14, 23)
  • Cold Numbers Used:    1/5 (42)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Execution Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Data Loading:     0.34s
  • Model Training:   2.17s
  • Prediction:       0.12s
  • Total:            2.63s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Disclaimer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  This prediction is generated by a machine learning model based on
  historical data. Lottery draws are random events. This tool is for
  entertainment purposes only. Please gamble responsibly.

═══════════════════════════════════════════════════════════════════════
```

### 3.2 Backtest Mode - Complete Output

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - BACKTEST MODE
═══════════════════════════════════════════════════════════════════════

🔍 Backtest Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Test Period:      2024-05-01 → 2024-11-15 (6 months)
  • Total Draws:      52 draws
  • Model Type:       LSTM Neural Network
  • Training Window:  180 days rolling
  • Started:          2024-11-15 14:35:42
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ Running Backtest... [████████████████████] 100% (52/52 draws)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Overall Performance Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Jackpot Matches (5+2):         0  (0.0%)   ████████████████████░
  Match 5+1:                     0  (0.0%)
  Match 5+0:                     1  (1.9%)   ✅
  Match 4+2:                     2  (3.8%)   ✅✅
  Match 4+1:                     8  (15.4%)  ████░░░░░░░░░░░░░░░░
  Match 4+0:                    12  (23.1%)  ██████░░░░░░░░░░░░░░
  Match 3+2:                     5  (9.6%)   ███░░░░░░░░░░░░░░░░░
  Match 3+1:                    14  (26.9%)  ███████░░░░░░░░░░░░░
  Match 3+0:                    10  (19.2%)  █████░░░░░░░░░░░░░░░
  ───────────────────────────────────────────────────────────────────
  Total Matches:                52  (100%)
  Average Match Rate:           3.2 numbers + 1.1 stars per draw

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Detailed Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Main Numbers Performance:
  ┌─────────────────────────────────────────────────────────────────┐
  │  5 matches:   1  draws  (1.9%)   █░░░░░░░░░░░░░░░░░░░          │
  │  4 matches:  22  draws  (42.3%)  █████████░░░░░░░░░░░          │
  │  3 matches:  29  draws  (55.8%)  ████████████░░░░░░░░          │
  │  2 matches:  0   draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  │  1 match:    0   draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  │  0 matches:  0   draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Stars Performance:
  ┌─────────────────────────────────────────────────────────────────┐
  │  2 matches:   7  draws  (13.5%)  ████░░░░░░░░░░░░░░░░          │
  │  1 match:    29  draws  (55.8%)  ████████████░░░░░░░░          │
  │  0 matches:  16  draws  (30.8%)  ███████░░░░░░░░░░░░░          │
  └─────────────────────────────────────────────────────────────────┘

  Accuracy Trends:
  ┌─────────────────────────────────────────────────────────────────┐
  │  Main Numbers:    ████████████████░░░░  64.2%                  │
  │  Lucky Stars:     █████████████░░░░░░░  58.7%                  │
  │  Combined:        ███████████████░░░░░  61.8%                  │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Performance Over Time (Weekly Aggregation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Hit Rate Evolution:

  100% ┤
       │
   75% ┤     ●       ●
       │       ●   ●   ●
   50% ┤ ●       ●       ●   ●
       │                       ●
   25% ┤
       │
    0% ┤
       └───────────────────────────────────────────────────────────
        May   Jun   Jul   Aug   Sep   Oct   Nov

  Average Confidence by Month:
  ┌─────────────────────────────────────────────────────────────────┐
  │  May 2024:  ██████████████████░░  78%  ▲                       │
  │  Jun 2024:  ███████████████░░░░░  72%  ▼                       │
  │  Jul 2024:  ████████████████████  81%  ▲                       │
  │  Aug 2024:  ███████████████░░░░░  69%  ▼                       │
  │  Sep 2024:  ██████████████████░░  76%  ▲                       │
  │  Oct 2024:  ████████████████░░░░  73%  ▼                       │
  │  Nov 2024:  ███████████████████░  79%  ▲                       │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Best Predictions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───────────┬─────────────────────────┬────────────┬──────────┐
  │   Date    │      Predicted          │   Actual   │  Result  │
  ├───────────┼─────────────────────────┼────────────┼──────────┤
  │ 2024-07-12│ 04 11 17 29 45 | ⭐ 2 8  │ 5+0 Match  │ ✅ Best  │
  │ 2024-09-20│ 09 18 23 31 47 | ⭐ 1 11 │ 4+2 Match  │ ✅ Good  │
  │ 2024-10-08│ 07 14 26 38 42 | ⭐ 5 9  │ 4+2 Match  │ ✅ Good  │
  └───────────┴─────────────────────────┴────────────┴──────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Hypothetical ROI Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Total Investment:      €130.00  (€2.50 × 52 draws)
  Total Winnings:        €87.50
  Net Profit/Loss:       -€42.50  (ROI: -32.7%)

  ┌─────────────────────────────────────────────────────────────────┐
  │  Note: Average lottery ROI is approximately -50%                │
  │  Model performance is 17.3% better than random play             │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Execution Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Data Loading:     0.89s
  • Backtest Runs:    47.23s
  • Analysis:         1.45s
  • Total:            49.57s

═══════════════════════════════════════════════════════════════════════
```

### 3.3 Loading States

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR
═══════════════════════════════════════════════════════════════════════

⏳ Initializing...

  [▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░] 50% - Loading historical data...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Data loaded successfully (287 draws)
⏳ Training model...

  [▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░] 75% - Epoch 15/20...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Alternative Spinner Styles:**

```
⏳ Loading data... ⠋
⏳ Loading data... ⠙
⏳ Loading data... ⠹
⏳ Loading data... ⠸
⏳ Loading data... ⠼
⏳ Loading data... ⠴
⏳ Loading data... ⠦
⏳ Loading data... ⠧
⏳ Loading data... ⠇
⏳ Loading data... ⠏
```

**Multi-Stage Progress:**

```
═══════════════════════════════════════════════════════════════════════

🚀 Starting Prediction Pipeline

  Stage 1: Data Collection       [████████████████████] ✅ Complete
  Stage 2: Data Preprocessing    [████████████████████] ✅ Complete
  Stage 3: Model Training        [███████████░░░░░░░░░] ⏳ 57%
  Stage 4: Prediction            [░░░░░░░░░░░░░░░░░░░░] ⏱️  Pending
  Stage 5: Analysis              [░░░░░░░░░░░░░░░░░░░░] ⏱️  Pending

  Overall Progress: [████████░░░░░░░░░░░░] 42%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3.4 Error Messages

**Error Template:**

```
═══════════════════════════════════════════════════════════════════════

❌ ERROR: [Error Type]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What happened:
  • [Clear description of the error]

  Why this occurred:
  • [Explanation of the root cause]

  How to fix it:
  1. [Step-by-step solution]
  2. [Additional steps if needed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Need help? Check the documentation or run: python predictor.py --help

═══════════════════════════════════════════════════════════════════════
```

**Example 1: Network Error**

```
═══════════════════════════════════════════════════════════════════════

❌ ERROR: Data Scraping Failed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What happened:
  • Failed to fetch historical data from Euromillions website
  • Connection timeout after 30 seconds

  Why this occurred:
  • Network connectivity issue
  • Website may be temporarily unavailable
  • Firewall/proxy blocking the request

  How to fix it:
  1. Check your internet connection
  2. Try again in a few minutes
  3. If using VPN/proxy, try disabling it
  4. Check if euromillions.com is accessible in your browser

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Need help? Check the documentation or run: python predictor.py --help

═══════════════════════════════════════════════════════════════════════
```

**Example 2: Insufficient Data**

```
═══════════════════════════════════════════════════════════════════════

❌ ERROR: Insufficient Training Data

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What happened:
  • Only 42 historical draws found
  • Minimum required: 100 draws

  Why this occurred:
  • Not enough data to train a reliable ML model
  • Data file may be corrupted or incomplete

  How to fix it:
  1. Re-run the scraper to fetch complete historical data:
     python scraper.py --full-history

  2. Or specify a longer date range:
     python scraper.py --start-date 2020-01-01

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Need help? Check the documentation or run: python predictor.py --help

═══════════════════════════════════════════════════════════════════════
```

**Example 3: Invalid Arguments**

```
═══════════════════════════════════════════════════════════════════════

❌ ERROR: Invalid Command Arguments

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What happened:
  • Invalid mode specified: 'predictt'
  • Did you mean: 'predict'?

  Available modes:
  • predict   - Generate predictions for next draw
  • backtest  - Run historical performance test
  • analyze   - Analyze historical patterns

  Usage:
  python predictor.py <mode> [options]

  Examples:
  python predictor.py predict
  python predictor.py backtest --months 6
  python predictor.py analyze --number 7

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Need help? Run: python predictor.py --help

═══════════════════════════════════════════════════════════════════════
```

---

## 4. User Flow Diagram

```
                    START
                      │
                      ▼
        ┌─────────────────────────┐
        │   Launch Application    │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Display Welcome       │
        │   & Available Modes     │
        └─────────────────────────┘
                      │
          ┌───────────┴───────────┬───────────┐
          ▼                       ▼           ▼
    ┌──────────┐           ┌──────────┐  ┌──────────┐
    │ PREDICT  │           │ BACKTEST │  │ ANALYZE  │
    └──────────┘           └──────────┘  └──────────┘
          │                       │           │
          ▼                       ▼           ▼
    ┌──────────┐           ┌──────────┐  ┌──────────┐
    │ Load     │           │ Config   │  │ Select   │
    │ Latest   │           │ Backtest │  │ Analysis │
    │ Data     │           │ Period   │  │ Type     │
    └──────────┘           └──────────┘  └──────────┘
          │                       │           │
          ▼                       ▼           ▼
    ┌──────────┐           ┌──────────┐  ┌──────────┐
    │ Train    │           │ Run      │  │ Generate │
    │ Model    │           │ Multiple │  │ Stats    │
    │          │           │ Tests    │  │ Charts   │
    └──────────┘           └──────────┘  └──────────┘
          │                       │           │
          ▼                       ▼           ▼
    ┌──────────┐           ┌──────────┐  ┌──────────┐
    │ Generate │           │ Aggregate│  │ Display  │
    │ Predict  │           │ Results  │  │ Insights │
    └──────────┘           └──────────┘  └──────────┘
          │                       │           │
          └───────────┬───────────┴───────────┘
                      ▼
        ┌─────────────────────────┐
        │   Display Results       │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Save to History?      │
        │   (Optional)            │
        └─────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   Exit or New Query?    │
        └─────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
        [EXIT]              [RESTART]
```

### 4.1 Command Structure

```
python predictor.py <mode> [options]

MODES:
  predict               Generate prediction for next draw
  backtest              Test model performance on historical data
  analyze               Analyze patterns and statistics

PREDICT OPTIONS:
  --model <type>        Model type: lstm|random_forest|ensemble (default: lstm)
  --confidence          Show detailed confidence metrics
  --explain             Show pattern analysis and reasoning

BACKTEST OPTIONS:
  --months <n>          Number of months to test (default: 6)
  --start <date>        Start date (YYYY-MM-DD)
  --end <date>          End date (YYYY-MM-DD)
  --model <type>        Model type to test

ANALYZE OPTIONS:
  --number <n>          Analyze frequency of specific number
  --pattern <type>      Pattern type: hot|cold|pairs|distribution
  --period <months>     Time period to analyze

GLOBAL OPTIONS:
  --help, -h            Show help message
  --version, -v         Show version
  --verbose             Enable verbose output
  --quiet               Minimal output
  --output <file>       Save output to file
```

---

## 5. Data Visualization

### 5.1 ASCII Charts - Bar Chart

```
Number Frequency Distribution (Last 100 Draws)

50 │              █
   │              █
40 │     █        █
   │     █        █
30 │     █  █     █     █
   │  █  █  █  █  █  █  █
20 │  █  █  █  █  █  █  █     █
   │  █  █  █  █  █  █  █  █  █
10 │  █  █  █  █  █  █  █  █  █  █
   │  █  █  █  █  █  █  █  █  █  █
 0 └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴───
    1  5  10 15 20 25 30 35 40 45 50
```

### 5.2 ASCII Charts - Line Chart

```
Model Accuracy Trend (12 Months)

100% ┤
     │
 90% ┤
     │                               ●
 80% ┤           ●         ●       ●   ●
     │         ●   ●     ●   ●   ●
 70% ┤       ●       ● ●       ●
     │     ●
 60% ┤   ●
     │ ●
 50% ┤
     └─────────────────────────────────────
      J F M A M J J A S O N D
```

### 5.3 Confidence Bars

```
Detailed Confidence Visualization:

  ████████████████████  100%  Perfect
  ███████████████████░   95%  Excellent
  ██████████████████░░   90%  Very High
  ████████████████░░░░   80%  High
  ██████████████░░░░░░   70%  Medium-High
  ████████████░░░░░░░░   60%  Medium
  ██████████░░░░░░░░░░   50%  Medium-Low
  ████████░░░░░░░░░░░░   40%  Low
  ██████░░░░░░░░░░░░░░   30%  Very Low
  ████░░░░░░░░░░░░░░░░   20%  Minimal
  ░░░░░░░░░░░░░░░░░░░░    0%  None
```

### 5.4 Histogram - Number Distribution

```
Number Range Distribution (Predicted vs Actual)

  1-10  │ ████████████ (12%)  Predicted
        │ ██████████   (10%)  Actual
        │
 11-20  │ ████████████████ (16%)  Predicted
        │ ██████████████   (14%)  Actual
        │
 21-30  │ ████████████████████ (20%)  Predicted
        │ ██████████████████   (18%)  Actual
        │
 31-40  │ ████████████████████████ (24%)  Predicted
        │ ██████████████████████   (22%)  Actual
        │
 41-50  │ ███████████████████████████ (28%)  Predicted
        │ ████████████████████████████ (36%)  Actual
```

### 5.5 Heatmap - Number Pair Frequency

```
Number Pair Correlation (Top 10 Pairs)

  High  ███  Medium  ▓▓▓  Low  ░░░

       1   5  10  15  20  25  30  35  40  45  50
   1 │ ─   ░   ░   ▓   ░   ░   ░   ░   ░   ░   ░
   5 │     ─   ░   ░   ░   ░   ▓   ░   ░   ░   ░
  10 │         ─   ░   ░   ░   ░   ░   ░   █   ░
  15 │             ─   ░   ░   ░   ░   ░   ░   ░
  20 │                 ─   ░   ░   ░   ░   ░   ░
  25 │                     ─   ░   ░   ░   ░   ░
  30 │                         ─   ░   ░   ░   ░
  35 │                             ─   ░   ░   ░
  40 │                                 ─   ░   ░
  45 │                                     ─   ░
  50 │                                         ─
```

---

## 6. Accessibility Guidelines

### 6.1 Readability Standards

**Line Length:**
- Maximum: 73 characters per line (fits 80-column terminals with margin)
- Optimal: 60-70 characters for body text
- Tables: Can extend to 75 characters

**Spacing:**
```
# Good spacing example:

Section Header
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Subsection Title

  • Bullet point with proper indentation
  • Another bullet point

  Paragraph text with breathing room above and below.
  Sentences flow naturally without crowding.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 6.2 Color Contrast

**High Contrast Pairs:**
- ✅ Green on Black (success messages)
- ❌ Red on Black (error messages)
- ⚠️  Yellow on Black (warnings)
- ℹ️  Cyan on Black (info)
- Bold White on Black (emphasis)

**Avoid:**
- ❌ Yellow on White
- ❌ Light Gray on White
- ❌ Cyan on White

### 6.3 Alternative Text for Symbols

Always provide textual context:

```
# Good:
✅ Success: Model trained successfully

# Bad:
✅ Model trained

# Good:
❌ Error: Unable to load data file

# Bad:
❌ Unable to load data
```

### 6.4 Screen Reader Considerations

```
# Structure with clear hierarchy:

LEVEL 1: Main Title (all caps, emoji + text)
  LEVEL 2: Section (emoji + text, separator line)
    LEVEL 3: Subsection (bullet + text)
      LEVEL 4: Details (indented text)
```

### 6.5 Keyboard Navigation

**Interactive Elements:**
```
Select mode:
  [1] Predict      - Generate next draw prediction
  [2] Backtest     - Test model performance
  [3] Analyze      - View statistics
  [q] Quit

Enter choice (1-3 or q): _
```

---

## 7. Complete Output Examples

### 7.1 Example 1: Successful Prediction

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR v1.0.0
═══════════════════════════════════════════════════════════════════════

🚀 Initializing Prediction System...

  [████████████████████] 100% - Loading complete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ System Ready

  • Historical Data:   287 draws loaded
  • Date Range:        2023-01-03 → 2024-11-15
  • Model Type:        LSTM Neural Network
  • Status:            Ready for prediction

═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE
═══════════════════════════════════════════════════════════════════════

📊 Model Information
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Training Data:    287 historical draws
  • Model Type:       LSTM Neural Network
  • Training Period:  2024-01-01 → 2024-11-15
  • Last Updated:     2024-11-15 14:32:18
  • Model Accuracy:   67.3% (last 100 draws)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Predicted Numbers for Next Draw
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Main Numbers (5):
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │            07    14    23    38    42                           │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Stars (2):
  ┌─────────────────────────────────────────────────────────────────┐
  │                                                                 │
  │                ⭐ 03      ⭐ 09                                  │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Confidence Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Overall Confidence:  ████████████████░░░░ 82%

  Individual Number Confidence:
  ┌─────────────────────────────────────────────────────────────────┐
  │  07  →  ████████████████████░ 95%   (Very High)                │
  │  14  →  █████████████████░░░░ 87%   (High)                     │
  │  23  →  ███████████████░░░░░░ 76%   (Medium-High)              │
  │  38  →  ████████████░░░░░░░░░ 68%   (Medium)                   │
  │  42  →  ███████████░░░░░░░░░░ 61%   (Medium)                   │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Star Confidence:
  ┌─────────────────────────────────────────────────────────────────┐
  │  03  →  ██████████████████░░░ 89%   (High)                     │
  │  09  →  ██████████████░░░░░░░ 73%   (Medium-High)              │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Pattern Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Number Distribution:  Balanced (2 low, 3 high)
  • Odd/Even Ratio:       3:2 (60% odd)
  • Sum of Numbers:       124 (within optimal range: 95-165)
  • Consecutive Numbers:  None
  • Hot Numbers Used:     3/5 (07, 14, 23)
  • Cold Numbers Used:    1/5 (42)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Historical Context
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Recent Frequency (Last 50 Draws):
  ┌─────────────────────────────────────────────────────────────────┐
  │  07 → Appeared 8 times   (16%)  ████░░░░░░░░░░░░░░░░           │
  │  14 → Appeared 7 times   (14%)  ███░░░░░░░░░░░░░░░░░           │
  │  23 → Appeared 6 times   (12%)  ███░░░░░░░░░░░░░░░░░           │
  │  38 → Appeared 5 times   (10%)  ██░░░░░░░░░░░░░░░░░░           │
  │  42 → Appeared 3 times   (6%)   █░░░░░░░░░░░░░░░░░░░           │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Execution Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Data Loading:     0.34s
  • Model Training:   2.17s
  • Prediction:       0.12s
  • Total:            2.63s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Results Saved
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ Prediction saved to: predictions/2024-11-15_14-32-18.json
  ✅ CSV export: predictions/2024-11-15_14-32-18.csv

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Disclaimer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  This prediction is generated by a machine learning model based on
  historical data. Lottery draws are random events. This tool is for
  entertainment purposes only. Please gamble responsibly.

═══════════════════════════════════════════════════════════════════════

  Next Steps:
  • Run backtest to see historical performance
  • Analyze number patterns with analyze mode
  • Check results after the draw

  Commands:
  python predictor.py backtest --months 6
  python predictor.py analyze --number 7

═══════════════════════════════════════════════════════════════════════
```

### 7.2 Example 2: 6-Month Backtest Results

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - BACKTEST MODE
═══════════════════════════════════════════════════════════════════════

🔍 Backtest Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Test Period:      2024-05-01 → 2024-11-15 (6 months)
  • Total Draws:      52 draws
  • Model Type:       LSTM Neural Network
  • Training Window:  180 days rolling
  • Started:          2024-11-15 14:35:42
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏳ Running Backtest...

  Draw 1/52   [█░░░░░░░░░░░░░░░░░░░]  2% - 2024-05-03
  Draw 10/52  [████░░░░░░░░░░░░░░░░] 19% - 2024-06-14
  Draw 20/52  [████████░░░░░░░░░░░░] 38% - 2024-07-26
  Draw 30/52  [████████████░░░░░░░░] 58% - 2024-09-06
  Draw 40/52  [████████████████░░░░] 77% - 2024-10-18
  Draw 52/52  [████████████████████] 100% - 2024-11-15

✅ Backtest Complete (49.57s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏆 Overall Performance Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Match Results Distribution:
  ┌─────────────────────────────────────────────────────────────────┐
  │  5+2 (Jackpot)     0  (0.0%)   ░░░░░░░░░░░░░░░░░░░░            │
  │  5+1               0  (0.0%)   ░░░░░░░░░░░░░░░░░░░░            │
  │  5+0               1  (1.9%)   █░░░░░░░░░░░░░░░░░░░  ✅        │
  │  4+2               2  (3.8%)   ██░░░░░░░░░░░░░░░░░░  ✅✅      │
  │  4+1               8  (15.4%)  ████░░░░░░░░░░░░░░░░            │
  │  4+0              12  (23.1%)  ██████░░░░░░░░░░░░░░            │
  │  3+2               5  (9.6%)   ███░░░░░░░░░░░░░░░░░            │
  │  3+1              14  (26.9%)  ███████░░░░░░░░░░░░░            │
  │  3+0              10  (19.2%)  █████░░░░░░░░░░░░░░░            │
  ├─────────────────────────────────────────────────────────────────┤
  │  Total Matches    52  (100%)                                   │
  │  Avg Per Draw     3.2 main numbers + 1.1 stars                 │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Detailed Performance Metrics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Main Numbers Accuracy:
  ┌─────────────────────────────────────────────────────────────────┐
  │  5 matches:   1  draws  (1.9%)   █░░░░░░░░░░░░░░░░░░░          │
  │  4 matches:  22  draws  (42.3%)  █████████░░░░░░░░░░░          │
  │  3 matches:  29  draws  (55.8%)  ████████████░░░░░░░░          │
  │  2 matches:   0  draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  │  1 match:     0  draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  │  0 matches:   0  draws  (0.0%)   ░░░░░░░░░░░░░░░░░░░░          │
  └─────────────────────────────────────────────────────────────────┘

  Lucky Stars Accuracy:
  ┌─────────────────────────────────────────────────────────────────┐
  │  2 matches:   7  draws  (13.5%)  ████░░░░░░░░░░░░░░░░          │
  │  1 match:    29  draws  (55.8%)  ████████████░░░░░░░░          │
  │  0 matches:  16  draws  (30.8%)  ███████░░░░░░░░░░░░░          │
  └─────────────────────────────────────────────────────────────────┘

  Combined Accuracy:
  ┌─────────────────────────────────────────────────────────────────┐
  │  Main Numbers:    ████████████████░░░░  64.2%                  │
  │  Lucky Stars:     █████████████░░░░░░░  58.7%                  │
  │  Overall:         ███████████████░░░░░  61.8%                  │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Performance Trends
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Weekly Hit Rate Evolution:

  100% ┤
       │
   75% ┤     ●       ●
       │       ●   ●   ●
   50% ┤ ●       ●       ●   ●
       │                       ●
   25% ┤
       │
    0% ┤
       └───────────────────────────────────────────────────────────
        Week 1    Week 8   Week 16  Week 24
        May       Jun-Jul  Aug-Sep  Oct-Nov

  Monthly Confidence Progression:
  ┌─────────────────────────────────────────────────────────────────┐
  │  May 2024:  ██████████████████░░  78%  ▲ +12% vs previous     │
  │  Jun 2024:  ███████████████░░░░░  72%  ▼ -6%  vs previous     │
  │  Jul 2024:  ████████████████████  81%  ▲ +9%  vs previous     │
  │  Aug 2024:  ███████████████░░░░░  69%  ▼ -12% vs previous     │
  │  Sep 2024:  ██████████████████░░  76%  ▲ +7%  vs previous     │
  │  Oct 2024:  ████████████████░░░░  73%  ▼ -3%  vs previous     │
  │  Nov 2024:  ███████████████████░  79%  ▲ +6%  vs previous     │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Top 5 Best Predictions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌───────────┬──────────────────────────┬───────────┬──────────┐
  │   Date    │      Predicted           │  Result   │  Rating  │
  ├───────────┼──────────────────────────┼───────────┼──────────┤
  │ 2024-07-12│ 04 11 17 29 45 │⭐ 2  8  │ 5+0 Match │ ✅ Best  │
  │ 2024-09-20│ 09 18 23 31 47 │⭐ 1 11  │ 4+2 Match │ ✅ Exc   │
  │ 2024-10-08│ 07 14 26 38 42 │⭐ 5  9  │ 4+2 Match │ ✅ Exc   │
  │ 2024-06-15│ 03 12 19 35 48 │⭐ 3  7  │ 4+1 Match │ ✅ Good  │
  │ 2024-08-23│ 06 15 22 33 44 │⭐ 4 10  │ 4+1 Match │ ✅ Good  │
  └───────────┴──────────────────────────┴───────────┴──────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Hypothetical Financial Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Investment Summary:
  ┌─────────────────────────────────────────────────────────────────┐
  │  Total Invested:    €130.00  (52 draws × €2.50)                │
  │  Total Winnings:    €87.50                                      │
  │  Net Profit/Loss:   -€42.50                                     │
  │  ROI:               -32.7%                                      │
  └─────────────────────────────────────────────────────────────────┘

  Prize Breakdown:
  ┌─────────────────────────────────────────────────────────────────┐
  │  5+0 (1×):      €25.00                                          │
  │  4+2 (2×):      €40.00  (€20.00 each)                           │
  │  4+1 (8×):      €22.50  (€2.80 each)                            │
  └─────────────────────────────────────────────────────────────────┘

  Comparison to Random Play:
  ┌─────────────────────────────────────────────────────────────────┐
  │  Expected Random ROI:    -50%                                   │
  │  Model Performance:      +17.3% better than random              │
  │                                                                 │
  │  ℹ️  Note: While not profitable, the model significantly        │
  │     outperforms random number selection.                        │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔢 Number-Level Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Most Accurately Predicted Numbers:
  ┌─────────────────────────────────────────────────────────────────┐
  │  #07  →  Hit 14/18 times (78%)  ████████████████░░░░           │
  │  #14  →  Hit 12/16 times (75%)  ███████████████░░░░░           │
  │  #23  →  Hit 11/15 times (73%)  ███████████████░░░░░           │
  │  #03⭐ →  Hit 9/12 times  (75%)  ███████████████░░░░░           │
  │  #09⭐ →  Hit 8/11 times  (73%)  ███████████████░░░░░           │
  └─────────────────────────────────────────────────────────────────┘

  Least Accurately Predicted Numbers:
  ┌─────────────────────────────────────────────────────────────────┐
  │  #42  →  Hit 3/12 times  (25%)  ██████░░░░░░░░░░░░░░           │
  │  #50  →  Hit 4/14 times  (29%)  ███████░░░░░░░░░░░░░           │
  │  #11⭐ →  Hit 2/8 times   (25%)  ██████░░░░░░░░░░░░░░           │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⏱️  Execution Time
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Data Loading:        0.89s
  • Backtest Execution:  47.23s (avg 0.91s per draw)
  • Results Analysis:    1.45s
  • Total Time:          49.57s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Results Saved
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ Detailed report: backtest/2024-11-15_6month_report.json
  ✅ CSV export:      backtest/2024-11-15_6month_results.csv
  ✅ Charts saved:    backtest/2024-11-15_6month_charts/

═══════════════════════════════════════════════════════════════════════

  Insights:
  • Model shows consistent 60%+ accuracy on main numbers
  • Performance peaks in months with stable patterns
  • Numbers 7, 14, 23 are most reliably predicted
  • Consider retraining when accuracy drops below 55%

  Next Steps:
  python predictor.py analyze --pattern hot
  python predictor.py predict --confidence

═══════════════════════════════════════════════════════════════════════
```

### 7.3 Example 3: Error - Scraping Failed

```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR v1.0.0
═══════════════════════════════════════════════════════════════════════

🚀 Initializing Prediction System...

  [████░░░░░░░░░░░░░░░░] 20% - Fetching historical data...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

═══════════════════════════════════════════════════════════════════════

❌ ERROR: Data Scraping Failed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  What happened:
  • Failed to fetch historical draw data from Euromillions website
  • Connection timeout after 30 seconds
  • URL: https://www.euro-millions.com/results/history

  Technical Details:
  • Error Type:    requests.exceptions.ConnectTimeout
  • Error Code:    ETIMEDOUT
  • Timestamp:     2024-11-15 14:38:42
  • Retry Count:   3 attempts failed

  Why this occurred:
  Possible causes (in order of likelihood):
  1. Network connectivity issue on your end
  2. Euromillions website is temporarily down
  3. Firewall or proxy blocking the request
  4. Website structure has changed (rare)

  How to fix it:

  Step 1: Check Your Connection
  ┌─────────────────────────────────────────────────────────────────┐
  │  • Verify internet connection is active                         │
  │  • Try opening https://www.euro-millions.com in browser         │
  │  • Check if other websites load normally                        │
  └─────────────────────────────────────────────────────────────────┘

  Step 2: Retry Operation
  ┌─────────────────────────────────────────────────────────────────┐
  │  Wait 2-3 minutes and run the command again:                    │
  │                                                                 │
  │    python predictor.py predict                                  │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Step 3: Check Network Settings
  ┌─────────────────────────────────────────────────────────────────┐
  │  If using VPN/Proxy:                                            │
  │    • Try disabling VPN temporarily                              │
  │    • Check proxy settings                                       │
  │                                                                 │
  │  If behind firewall:                                            │
  │    • Ensure HTTPS (port 443) is allowed                         │
  │    • Whitelist euro-millions.com domain                         │
  └─────────────────────────────────────────────────────────────────┘

  Step 4: Use Cached Data (if available)
  ┌─────────────────────────────────────────────────────────────────┐
  │  Run with offline mode:                                         │
  │                                                                 │
  │    python predictor.py predict --offline                        │
  │                                                                 │
  │  Note: Uses last successfully downloaded data                   │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Additional Troubleshooting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Check System Status:
  ┌─────────────────────────────────────────────────────────────────┐
  │  • Last successful data fetch: 2024-11-14 09:23:15              │
  │  • Cached data available:      Yes (286 draws)                  │
  │  • Cache age:                  29 hours (still valid)           │
  └─────────────────────────────────────────────────────────────────┘

  Advanced Options:
  • View logs:         python predictor.py --show-logs
  • Test connection:   python predictor.py --test-connection
  • Manual data load:  python predictor.py --load-csv <file>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Need More Help?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Read the docs:      docs/TROUBLESHOOTING.md
  • Check FAQ:          docs/FAQ.md
  • Report an issue:    github.com/yourrepo/issues
  • Get help:           python predictor.py --help

═══════════════════════════════════════════════════════════════════════

  Quick Actions:
  [1] Retry now
  [2] Use offline mode (cached data)
  [3] View detailed logs
  [4] Test connection
  [q] Quit

  Enter choice (1-4 or q): _

═══════════════════════════════════════════════════════════════════════
```

---

## 8. Responsive Design

### 8.1 Terminal Width Adaptation

**Narrow Terminal (60 columns):**
```
══════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR
══════════════════════════════════════════════════════

📊 Model Info
──────────────────────────────────────────────────────
  Training Data:  287 draws
  Model:          LSTM
  Accuracy:       67.3%
──────────────────────────────────────────────────────

🎯 Prediction
──────────────────────────────────────────────────────
  Main: 07 14 23 38 42
  Stars: ⭐ 03 ⭐ 09

  Confidence: ████████████████░░░░ 82%
──────────────────────────────────────────────────────
```

**Standard Terminal (80 columns):**
```
═══════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE
═══════════════════════════════════════════════════════════════════════
[Full output as shown in examples above]
```

**Wide Terminal (120+ columns):**
```
════════════════════════════════════════════════════════════════════════════════════════════════════════════════
   🎰 EUROMILLIONS ML PREDICTOR - PREDICTION MODE                                    Runtime: 2.63s | v1.0.0
════════════════════════════════════════════════════════════════════════════════════════════════════════════════

📊 Model Information                          │  🎯 Predicted Numbers for Next Draw
──────────────────────────────────────────────┼───────────────────────────────────────────────────────────────
  • Training Data:    287 draws               │    Main Numbers (5):    07   14   23   38   42
  • Model Type:       LSTM Neural Network     │    Lucky Stars (2):     ⭐ 03      ⭐ 09
  • Training Period:  2024-01-01 → 2024-11-15 │
  • Model Accuracy:   67.3% (last 100 draws)  │    Overall Confidence:  ████████████████░░░░ 82%
                                              │
[Side-by-side layout for wide terminals]
```

---

## 9. Animation & Interactivity

### 9.1 Progress Animation Sequences

**Dots Animation:**
```
Loading.
Loading..
Loading...
Loading
```

**Spinner Animation:**
```
Processing  |
Processing  /
Processing  ─
Processing  \
Processing  |
```

**Block Animation:**
```
[▓          ] 10%
[▓▓         ] 20%
[▓▓▓        ] 30%
...
[▓▓▓▓▓▓▓▓▓▓] 100%
```

### 9.2 Interactive Menu Example

```
═══════════════════════════════════════════════════════════════════════

  🎰 EUROMILLIONS ML PREDICTOR - Main Menu

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Select Mode:

  ┌─────────────────────────────────────────────────────────────────┐
  │  [1] 🎯 Predict                                                 │
  │      Generate predictions for the next Euromillions draw        │
  │                                                                 │
  │  [2] 🔍 Backtest                                                │
  │      Test model accuracy on historical draws                    │
  │                                                                 │
  │  [3] 📊 Analyze                                                 │
  │      View statistical patterns and insights                     │
  │                                                                 │
  │  [4] ⚙️  Settings                                               │
  │      Configure model and display preferences                    │
  │                                                                 │
  │  [h] ℹ️  Help                                                   │
  │  [q] ❌ Quit                                                    │
  └─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Enter your choice (1-4, h, or q): _

═══════════════════════════════════════════════════════════════════════
```

---

## 10. Implementation Guidelines

### 10.1 Python Implementation Example

```python
# colors.py - Color and styling utilities

class Colors:
    """ANSI color codes for terminal output"""

    # Status colors
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    WARNING = '\033[93m'
    INFO = '\033[94m'

    # Emphasis
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'

    # Data colors
    PRIMARY = '\033[96m'
    SECONDARY = '\033[95m'
    NEUTRAL = '\033[37m'

    # Reset
    RESET = '\033[0m'

    @staticmethod
    def success(text):
        return f"{Colors.SUCCESS}{text}{Colors.RESET}"

    @staticmethod
    def error(text):
        return f"{Colors.ERROR}{text}{Colors.RESET}"

    @staticmethod
    def warning(text):
        return f"{Colors.WARNING}{text}{Colors.RESET}"

    @staticmethod
    def info(text):
        return f"{Colors.INFO}{text}{Colors.RESET}"

    @staticmethod
    def bold(text):
        return f"{Colors.BOLD}{text}{Colors.RESET}"


class UI:
    """Terminal UI components"""

    # Separators
    SEPARATOR_HEAVY = '═' * 71
    SEPARATOR_LIGHT = '─' * 71
    SEPARATOR_SECTION = '━' * 71

    # Box characters
    BOX_TOP_LEFT = '┌'
    BOX_TOP_RIGHT = '┐'
    BOX_BOTTOM_LEFT = '└'
    BOX_BOTTOM_RIGHT = '┘'
    BOX_VERTICAL = '│'
    BOX_HORIZONTAL = '─'

    @staticmethod
    def header(title, emoji='🎰'):
        """Create a formatted header"""
        print(UI.SEPARATOR_HEAVY)
        print(f"   {emoji} {title}")
        print(UI.SEPARATOR_HEAVY)

    @staticmethod
    def section(title, emoji='📊'):
        """Create a section header"""
        print()
        print(f"{emoji} {title}")
        print(UI.SEPARATOR_SECTION)

    @staticmethod
    def progress_bar(percentage, width=20, filled='█', empty='░'):
        """Generate a progress bar"""
        filled_width = int(width * percentage / 100)
        empty_width = width - filled_width
        bar = filled * filled_width + empty * empty_width
        return f"[{bar}] {percentage}%"

    @staticmethod
    def box(content, width=67):
        """Create a box around content"""
        print(f"{UI.BOX_TOP_LEFT}{UI.BOX_HORIZONTAL * width}{UI.BOX_TOP_RIGHT}")
        for line in content:
            padding = width - len(line)
            print(f"{UI.BOX_VERTICAL} {line}{' ' * padding}{UI.BOX_VERTICAL}")
        print(f"{UI.BOX_BOTTOM_LEFT}{UI.BOX_HORIZONTAL * width}{UI.BOX_BOTTOM_RIGHT}")


# Usage example
if __name__ == "__main__":
    UI.header("EUROMILLIONS ML PREDICTOR - PREDICTION MODE")
    UI.section("Predicted Numbers", "🎯")

    print(f"\n  Main Numbers: {Colors.bold('07 14 23 38 42')}")
    print(f"  Lucky Stars:  {Colors.bold('⭐ 03  ⭐ 09')}\n")

    print(f"  Overall Confidence: {UI.progress_bar(82)}\n")

    print(Colors.success("✅ Prediction generated successfully"))
    print(Colors.error("❌ Error: Connection failed"))
    print(Colors.warning("⚠️  Warning: Using cached data"))
```

### 10.2 Display Functions

```python
# display.py - Display formatting functions

def display_prediction_result(prediction, confidence, metadata):
    """
    Display prediction results in formatted terminal output

    Args:
        prediction: Dict with 'main_numbers' and 'stars'
        confidence: Dict with confidence scores
        metadata: Dict with model information
    """

    # Header
    UI.header("EUROMILLIONS ML PREDICTOR - PREDICTION MODE")

    # Model information section
    UI.section("Model Information")
    print(f"  • Training Data:    {metadata['total_draws']} historical draws")
    print(f"  • Model Type:       {metadata['model_type']}")
    print(f"  • Training Period:  {metadata['start_date']} → {metadata['end_date']}")
    print(f"  • Last Updated:     {metadata['updated_at']}")
    print(f"  • Model Accuracy:   {metadata['accuracy']}% (last 100 draws)")
    print(UI.SEPARATOR_SECTION)

    # Predicted numbers section
    UI.section("Predicted Numbers for Next Draw", "🎯")
    print("\n  Main Numbers (5):")
    main_nums = '    '.join([f"{n:02d}" for n in prediction['main_numbers']])
    UI.box([f"          {main_nums}"], width=63)

    print("\n  Lucky Stars (2):")
    stars = f"⭐ {prediction['stars'][0]:02d}      ⭐ {prediction['stars'][1]:02d}"
    UI.box([f"              {stars}"], width=63)

    # Confidence section
    UI.section("Confidence Metrics", "📈")
    overall_conf = int(confidence['overall'] * 100)
    print(f"\n  Overall Confidence:  {UI.progress_bar(overall_conf)}\n")

    print("  Individual Number Confidence:")
    UI.box([
        f"  {num:02d}  →  {UI.progress_bar(int(conf * 100))}   ({rating})"
        for num, conf, rating in zip(
            prediction['main_numbers'],
            confidence['main_numbers'],
            get_confidence_ratings(confidence['main_numbers'])
        )
    ])

    print(UI.SEPARATOR_HEAVY)


def get_confidence_rating(confidence):
    """Convert confidence percentage to text rating"""
    if confidence >= 0.90:
        return "Very High"
    elif confidence >= 0.80:
        return "High"
    elif confidence >= 0.70:
        return "Medium-High"
    elif confidence >= 0.60:
        return "Medium"
    elif confidence >= 0.50:
        return "Medium-Low"
    else:
        return "Low"
```

---

## 11. Summary & Best Practices

### 11.1 Key Design Principles

1. **Clarity First**: Always prioritize clear information over decoration
2. **Consistent Structure**: Maintain predictable layouts across all modes
3. **Progressive Disclosure**: Show summaries first, details on demand
4. **Visual Hierarchy**: Use separators and spacing to guide the eye
5. **Meaningful Colors**: Use color to convey meaning, not just aesthetics
6. **Accessible Design**: Ensure readability for all users
7. **Responsive Layout**: Adapt to different terminal widths
8. **Error-Friendly**: Make errors clear, actionable, and helpful

### 11.2 Do's and Don'ts

**DO:**
- ✅ Use emoji sparingly and meaningfully
- ✅ Provide clear error messages with solutions
- ✅ Show progress for long-running operations
- ✅ Use consistent spacing and alignment
- ✅ Include execution time information
- ✅ Offer next steps after completing actions

**DON'T:**
- ❌ Overcrowd the interface with too much information
- ❌ Use colors that clash or have poor contrast
- ❌ Show technical errors without context
- ❌ Mix different design patterns inconsistently
- ❌ Forget to include help/documentation references
- ❌ Use ambiguous icons or symbols

### 11.3 Testing Checklist

- [ ] Test in 60, 80, and 120 column terminals
- [ ] Verify color output on different terminal emulators
- [ ] Test with screen readers (accessibility)
- [ ] Validate all progress indicators work correctly
- [ ] Ensure error messages are clear and actionable
- [ ] Check alignment and spacing across all outputs
- [ ] Test with various data scenarios (edge cases)
- [ ] Verify emoji rendering on different systems

---

**Document Version:** 1.0.0
**Last Updated:** 2024-11-15
**Author:** UX Design Team
**Status:** Ready for Implementation
