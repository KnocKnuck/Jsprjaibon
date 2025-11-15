"""Prediction engine for EuroMillions"""
import numpy as np
from typing import List, Tuple, Dict
from datetime import datetime
from collections import Counter

from ..models.base import BaseModel
from ..features.engineering import FeatureEngineer
from ..features.normalizer import FeatureNormalizer
from ..data.models import Draw


class PredictionGrid:
    """A single prediction grid"""

    def __init__(self, numbers: List[int], stars: List[int], confidence: float, method: str):
        """Initialize prediction grid

        Args:
            numbers: List of 5 predicted numbers (1-50)
            stars: List of 2 predicted stars (1-12)
            confidence: Confidence score (0-1)
            method: Generation method used
        """
        self.numbers = sorted(numbers)
        self.stars = sorted(stars)
        self.confidence = confidence
        self.method = method
        self.generated_at = datetime.now()

    def __repr__(self):
        return f"Grid(numbers={self.numbers}, stars={self.stars}, confidence={self.confidence:.1%})"

    def __str__(self):
        nums = ' '.join(f'{n:2d}' for n in self.numbers)
        stars = ' '.join(f'{s:2d}' for s in self.stars)
        return f"[{nums}] + [{stars}] (confidence: {self.confidence:.1%})"

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'numbers': self.numbers,
            'stars': self.stars,
            'confidence': self.confidence,
            'method': self.method,
            'generated_at': self.generated_at.isoformat()
        }


class Predictor:
    """Generate prediction grids using ML models"""

    def __init__(self, model: BaseModel, feature_engineer: FeatureEngineer, normalizer: FeatureNormalizer):
        """Initialize predictor

        Args:
            model: Trained ML model
            feature_engineer: Feature engineering instance
            normalizer: Feature normalizer instance
        """
        self.model = model
        self.feature_engineer = feature_engineer
        self.normalizer = normalizer

    def predict(self, historical_draws: List[Draw], n_grids: int = 2) -> List[PredictionGrid]:
        """Generate N prediction grids

        Args:
            historical_draws: List of historical Draw objects
            n_grids: Number of grids to generate

        Returns:
            List of PredictionGrid objects
        """
        # Extract features
        features = self.feature_engineer.extract_all_features(historical_draws)

        if len(features) == 0:
            raise ValueError("Not enough historical data to extract features")

        # Normalize features (use last row for prediction)
        features_norm = self.normalizer.transform(features.iloc[-1:])

        # Get model probabilities
        numbers_proba, stars_proba = self.model.predict(features_norm.values)

        # Get statistical probabilities
        stats_numbers_proba = self._calculate_frequency_proba(historical_draws, 'numbers')
        stats_stars_proba = self._calculate_frequency_proba(historical_draws, 'stars')

        # Fusion (50% ML, 50% stats)
        final_numbers_proba = 0.5 * numbers_proba + 0.5 * stats_numbers_proba
        final_stars_proba = 0.5 * stars_proba + 0.5 * stats_stars_proba

        # Generate grids
        grids = []
        for i in range(n_grids):
            if i == 0:
                # Grid 1: Top probabilities
                numbers, stars, conf = self._generate_top_proba(final_numbers_proba, final_stars_proba)
                grids.append(PredictionGrid(numbers, stars, conf, "top_probabilities"))
            else:
                # Other grids: Weighted sampling
                numbers, stars, conf = self._generate_weighted_sample(final_numbers_proba, final_stars_proba)
                grids.append(PredictionGrid(numbers, stars, conf, "weighted_sampling"))

        return grids

    def _generate_top_proba(self, numbers_proba: np.ndarray, stars_proba: np.ndarray) -> Tuple[List[int], List[int], float]:
        """Select top probabilities

        Args:
            numbers_proba: Probability array for numbers (50,)
            stars_proba: Probability array for stars (12,)

        Returns:
            Tuple of (numbers, stars, confidence)
        """
        # Top 5 numbers (add 1 because lottery is 1-indexed)
        top_numbers_idx = np.argsort(numbers_proba)[-5:]
        numbers = [int(idx + 1) for idx in top_numbers_idx]

        # Top 2 stars
        top_stars_idx = np.argsort(stars_proba)[-2:]
        stars = [int(idx + 1) for idx in top_stars_idx]

        # Calculate confidence
        confidence = float((np.mean(numbers_proba[top_numbers_idx]) + np.mean(stars_proba[top_stars_idx])) / 2)

        return sorted(numbers), sorted(stars), confidence

    def _generate_weighted_sample(self, numbers_proba: np.ndarray, stars_proba: np.ndarray) -> Tuple[List[int], List[int], float]:
        """Weighted random sampling

        Args:
            numbers_proba: Probability array for numbers (50,)
            stars_proba: Probability array for stars (12,)

        Returns:
            Tuple of (numbers, stars, confidence)
        """
        # Normalize probabilities
        numbers_proba_norm = numbers_proba / numbers_proba.sum()
        stars_proba_norm = stars_proba / stars_proba.sum()

        # Sample
        numbers_idx = np.random.choice(50, size=5, replace=False, p=numbers_proba_norm)
        stars_idx = np.random.choice(12, size=2, replace=False, p=stars_proba_norm)

        numbers = [int(idx + 1) for idx in numbers_idx]
        stars = [int(idx + 1) for idx in stars_idx]

        confidence = float((np.mean(numbers_proba[numbers_idx]) + np.mean(stars_proba[stars_idx])) / 2)

        return sorted(numbers), sorted(stars), confidence

    def _calculate_frequency_proba(self, draws: List[Draw], field: str) -> np.ndarray:
        """Calculate frequency-based probabilities

        Args:
            draws: Historical draws
            field: 'numbers' or 'stars'

        Returns:
            Probability array
        """
        if field == 'numbers':
            size = 50
            all_values = [num for draw in draws for num in draw.numbers]
        else:
            size = 12
            all_values = [star for draw in draws for star in draw.stars]

        counts = Counter(all_values)
        proba = np.zeros(size)
        for num, count in counts.items():
            proba[num - 1] = count

        # Normalize
        return proba / proba.sum() if proba.sum() > 0 else proba
