"""Backtest engine for EuroMillions predictions"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from ..data.models import Draw
from .predictor import Predictor, PredictionGrid


class BacktestResult:
    """Results from backtesting"""

    def __init__(self):
        self.predictions = []
        self.actuals = []
        self.metrics = {}
        self.hits_distribution = defaultdict(int)

    def add_result(self, prediction: PredictionGrid, actual: Draw):
        """Add a prediction result

        Args:
            prediction: Predicted grid
            actual: Actual draw result
        """
        self.predictions.append(prediction)
        self.actuals.append(actual)

        # Calculate hits
        numbers_hit = len(set(prediction.numbers) & set(actual.numbers))
        stars_hit = len(set(prediction.stars) & set(actual.stars))

        self.hits_distribution[f"{numbers_hit}+{stars_hit}"] += 1

    def calculate_metrics(self):
        """Calculate performance metrics"""
        total_draws = len(self.predictions)

        if total_draws == 0:
            self.metrics = {
                'total_draws': 0,
                'avg_numbers_accuracy': 0,
                'avg_stars_accuracy': 0,
                'avg_confidence': 0,
                'hits_distribution': {},
                'best_prediction': None
            }
            return

        # Accuracy metrics
        numbers_accuracy = []
        stars_accuracy = []

        for pred, actual in zip(self.predictions, self.actuals):
            numbers_hit = len(set(pred.numbers) & set(actual.numbers))
            stars_hit = len(set(pred.stars) & set(actual.stars))

            numbers_accuracy.append(numbers_hit / 5)
            stars_accuracy.append(stars_hit / 2)

        self.metrics = {
            'total_draws': total_draws,
            'avg_numbers_accuracy': float(np.mean(numbers_accuracy)),
            'avg_stars_accuracy': float(np.mean(stars_accuracy)),
            'avg_confidence': float(np.mean([p.confidence for p in self.predictions])),
            'hits_distribution': dict(self.hits_distribution),
            'best_prediction': self._find_best_prediction()
        }

    def _find_best_prediction(self) -> Optional[Dict]:
        """Find best prediction"""
        if not self.predictions:
            return None

        best_idx = 0
        best_score = 0

        for i, (pred, actual) in enumerate(zip(self.predictions, self.actuals)):
            numbers_hit = len(set(pred.numbers) & set(actual.numbers))
            stars_hit = len(set(pred.stars) & set(actual.stars))
            score = numbers_hit * 2 + stars_hit * 3

            if score > best_score:
                best_score = score
                best_idx = i

        return {
            'date': self.actuals[best_idx].date.isoformat(),
            'predicted_numbers': self.predictions[best_idx].numbers,
            'predicted_stars': self.predictions[best_idx].stars,
            'actual_numbers': self.actuals[best_idx].numbers,
            'actual_stars': self.actuals[best_idx].stars,
            'numbers_hit': len(set(self.predictions[best_idx].numbers) & set(self.actuals[best_idx].numbers)),
            'stars_hit': len(set(self.predictions[best_idx].stars) & set(self.actuals[best_idx].stars)),
            'score': best_score
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Convert results to DataFrame

        Returns:
            DataFrame with prediction results
        """
        data = []
        for pred, actual in zip(self.predictions, self.actuals):
            numbers_hit = len(set(pred.numbers) & set(actual.numbers))
            stars_hit = len(set(pred.stars) & set(actual.stars))

            data.append({
                'date': actual.date,
                'predicted_numbers': str(pred.numbers),
                'actual_numbers': str(actual.numbers),
                'predicted_stars': str(pred.stars),
                'actual_stars': str(actual.stars),
                'numbers_hit': numbers_hit,
                'stars_hit': stars_hit,
                'confidence': pred.confidence,
                'method': pred.method
            })

        return pd.DataFrame(data)

    def __repr__(self):
        return f"BacktestResult(draws={len(self.predictions)}, avg_accuracy={self.metrics.get('avg_numbers_accuracy', 0):.2%})"


class BacktestEngine:
    """Backtest model performance on historical data"""

    def __init__(self, predictor: Predictor):
        """Initialize backtest engine

        Args:
            predictor: Predictor instance to test
        """
        self.predictor = predictor

    def run_backtest(
        self,
        all_draws: List[Draw],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        window_months: Optional[int] = None,
        min_training_draws: int = 50
    ) -> BacktestResult:
        """Run backtest over specified period

        Args:
            all_draws: All available historical draws
            start_date: Start date for backtest (optional)
            end_date: End date for backtest (optional)
            window_months: Number of months to backtest (alternative to dates)
            min_training_draws: Minimum training draws required

        Returns:
            BacktestResult object
        """
        result = BacktestResult()

        # Sort draws by date
        all_draws = sorted(all_draws, key=lambda d: d.date)

        # Determine date range
        if window_months:
            end_date = max(draw.date for draw in all_draws)
            start_date = end_date - timedelta(days=window_months * 30)
        elif not start_date:
            start_date = min(draw.date for draw in all_draws)
        if not end_date:
            end_date = max(draw.date for draw in all_draws)

        # Get test draws
        test_draws = [d for d in all_draws if start_date <= d.date <= end_date]

        # Safe date conversion for display
        start_str = start_date.date() if hasattr(start_date, 'date') else start_date
        end_str = end_date.date() if hasattr(end_date, 'date') else end_date
        print(f"Backtesting on {len(test_draws)} draws ({start_str} to {end_str})...")

        for i, test_draw in enumerate(test_draws):
            # Train on data BEFORE this draw
            train_draws = [d for d in all_draws if d.date < test_draw.date]

            if len(train_draws) < min_training_draws:
                continue  # Need minimum training data

            # Make prediction
            try:
                grids = self.predictor.predict(train_draws, n_grids=1)
                result.add_result(grids[0], test_draw)

                if (i + 1) % 10 == 0:
                    print(f"  Processed {i + 1}/{len(test_draws)} draws...")
            except Exception as e:
                print(f"  Error on draw {test_draw.date}: {e}")
                continue

        result.calculate_metrics()
        print(f"Backtest complete: {len(result.predictions)} predictions made")
        return result

    def walk_forward_validation(
        self,
        all_draws: List[Draw],
        test_size: int = 50,
        step_size: int = 10
    ) -> List[BacktestResult]:
        """Perform walk-forward validation

        Args:
            all_draws: All available historical draws
            test_size: Number of draws in each test set
            step_size: Number of draws to step forward

        Returns:
            List of BacktestResult objects for each fold
        """
        all_draws = sorted(all_draws, key=lambda d: d.date)
        results = []

        print(f"Walk-forward validation: test_size={test_size}, step_size={step_size}")

        start_idx = 100  # Minimum training size
        while start_idx + test_size <= len(all_draws):
            train_draws = all_draws[:start_idx]
            test_draws = all_draws[start_idx:start_idx + test_size]

            print(f"\nFold: train={len(train_draws)}, test={len(test_draws)}")

            result = BacktestResult()
            for test_draw in test_draws:
                try:
                    grids = self.predictor.predict(train_draws, n_grids=1)
                    result.add_result(grids[0], test_draw)
                except Exception as e:
                    print(f"  Error: {e}")
                    continue

            result.calculate_metrics()
            results.append(result)

            start_idx += step_size

        print(f"\nCompleted {len(results)} folds")
        return results
