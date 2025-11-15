"""Dummy model for testing and fallback"""
import numpy as np
from typing import Tuple

from .base import BaseModel


class DummyModel(BaseModel):
    """Dummy model for testing and fallback

    This model generates random probabilities and can be used
    for testing the prediction pipeline without training.
    """

    def __init__(self):
        super().__init__("dummy")
        self.trained = True  # Always ready

    def train(self, X: np.ndarray, y_numbers: np.ndarray, y_stars: np.ndarray) -> dict:
        """Dummy training - does nothing

        Args:
            X: Training features
            y_numbers: Target numbers
            y_stars: Target stars

        Returns:
            Empty metrics dict
        """
        return {
            'loss': 0.0,
            'accuracy': 0.0,
            'epochs': 0
        }

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Generate random probabilities

        Returns uniform random probabilities for all numbers and stars.

        Args:
            X: Input features (ignored)

        Returns:
            Tuple of (numbers_probabilities, stars_probabilities)
        """
        # Uniform probabilities with some noise
        numbers_proba = np.random.uniform(0.5, 1.5, 50)
        stars_proba = np.random.uniform(0.5, 1.5, 12)

        # Normalize to sum to 1
        numbers_proba = numbers_proba / numbers_proba.sum()
        stars_proba = stars_proba / stars_proba.sum()

        return numbers_proba, stars_proba

    def save(self, path: str):
        """Dummy save - does nothing"""
        pass

    def load(self, path: str):
        """Dummy load - does nothing"""
        pass
