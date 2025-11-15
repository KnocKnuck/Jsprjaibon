"""
Random Forest model implementation for EuroMillions prediction.

This module implements a Random Forest classifier using scikit-learn's
ensemble methods, with separate models for numbers and stars.
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
import numpy as np
from typing import Tuple, Dict
import joblib
from pathlib import Path

from .base import BaseModel


class RandomForestModel(BaseModel):
    """
    Random Forest model for lottery number prediction.

    Uses ensemble learning with multiple decision trees to predict
    probabilities for both main numbers and star numbers.

    Attributes:
        n_estimators (int): Number of trees in the forest
        max_depth (int): Maximum depth of each tree
        random_state (int): Random seed for reproducibility
        numbers_model: Random Forest for main numbers
        stars_model: Random Forest for star numbers
    """

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: int = 15,
        random_state: int = 42
    ):
        """
        Initialize Random Forest model.

        Args:
            n_estimators: Number of trees in the forest (default: 200)
            max_depth: Maximum depth of trees (default: 15)
            random_state: Random seed for reproducibility (default: 42)
        """
        super().__init__("RandomForest")
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state

        # Separate models for numbers and stars
        self.numbers_model = MultiOutputClassifier(
            RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                n_jobs=-1,  # Use all CPU cores
                class_weight='balanced'  # Handle class imbalance
            )
        )
        self.stars_model = MultiOutputClassifier(
            RandomForestClassifier(
                n_estimators=n_estimators,
                max_depth=max_depth,
                random_state=random_state,
                n_jobs=-1,
                class_weight='balanced'
            )
        )

    def train(self, X: np.ndarray, y_numbers: np.ndarray, y_stars: np.ndarray):
        """
        Train Random Forest models on historical data.

        Args:
            X: Feature matrix of shape (n_samples, n_features)
            y_numbers: Target labels for main numbers (n_samples, 5)
            y_stars: Target labels for star numbers (n_samples, 2)
        """
        print(f"Training Random Forest on {X.shape[0]} samples...")
        print(f"Features shape: {X.shape}, Numbers: {y_numbers.shape}, Stars: {y_stars.shape}")

        # Train numbers model (5 main numbers)
        print("Training main numbers model...")
        self.numbers_model.fit(X, y_numbers)

        # Train stars model (2 star numbers)
        print("Training star numbers model...")
        self.stars_model.fit(X, y_stars)

        self.trained = True
        self.metadata = {
            'model_type': 'RandomForest',
            'n_estimators': self.n_estimators,
            'max_depth': self.max_depth,
            'n_samples': X.shape[0],
            'n_features': X.shape[1],
            'numbers_shape': y_numbers.shape,
            'stars_shape': y_stars.shape
        }
        print("✓ Random Forest training complete")

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict probabilities for numbers and stars.

        Args:
            X: Feature matrix for prediction

        Returns:
            Tuple of (numbers_probabilities, stars_probabilities)
            - numbers_probabilities: Array of shape (50,) with probability for each number 1-50
            - stars_probabilities: Array of shape (12,) with probability for each star 1-12

        Raises:
            ValueError: If model has not been trained
        """
        if not self.trained:
            raise ValueError("Model not trained. Call train() first.")

        # Get probabilities from each multi-output classifier
        numbers_proba = self.numbers_model.predict_proba(X)
        stars_proba = self.stars_model.predict_proba(X)

        # Convert to probability arrays
        numbers_pred = self._aggregate_probabilities(numbers_proba, n_classes=50)
        stars_pred = self._aggregate_probabilities(stars_proba, n_classes=12)

        return numbers_pred, stars_pred

    def _aggregate_probabilities(
        self,
        proba_list: list,
        n_classes: int
    ) -> np.ndarray:
        """
        Aggregate probabilities from multi-output classifier.

        Each output in the multi-output classifier provides probabilities.
        This method aggregates them into a single probability distribution.

        Args:
            proba_list: List of probability arrays from each output
            n_classes: Total number of classes (50 for numbers, 12 for stars)

        Returns:
            Aggregated probability array of shape (n_classes,)
        """
        # Initialize aggregated probabilities
        aggregated = np.zeros(n_classes)

        # Average probabilities across all outputs
        for proba in proba_list:
            if proba.shape[1] == 2:  # Binary classifier for each position
                # Take probability of positive class
                aggregated += proba[:, 1]

        # Normalize by number of outputs
        aggregated = aggregated / len(proba_list)

        return aggregated

    def get_feature_importance(self) -> Dict[str, np.ndarray]:
        """
        Get feature importance scores from the trained models.

        Returns:
            Dictionary with 'numbers' and 'stars' feature importance arrays
        """
        if not self.trained:
            raise ValueError("Model not trained. Call train() first.")

        # Average feature importance across all estimators
        numbers_importance = np.mean([
            est.feature_importances_
            for est in self.numbers_model.estimators_
        ], axis=0)

        stars_importance = np.mean([
            est.feature_importances_
            for est in self.stars_model.estimators_
        ], axis=0)

        return {
            'numbers': numbers_importance,
            'stars': stars_importance
        }

    def save(self, path: str):
        """
        Save the trained Random Forest model to disk.

        Args:
            path: File path where model should be saved
        """
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        model_data = {
            'numbers_model': self.numbers_model,
            'stars_model': self.stars_model,
            'metadata': self.metadata,
            'n_estimators': self.n_estimators,
            'max_depth': self.max_depth,
            'random_state': self.random_state
        }

        joblib.dump(model_data, path)
        print(f"✓ Model saved to {path}")

    def load(self, path: str):
        """
        Load a trained Random Forest model from disk.

        Args:
            path: File path from which to load the model
        """
        model_data = joblib.load(path)

        self.numbers_model = model_data['numbers_model']
        self.stars_model = model_data['stars_model']
        self.metadata = model_data['metadata']
        self.n_estimators = model_data.get('n_estimators', self.n_estimators)
        self.max_depth = model_data.get('max_depth', self.max_depth)
        self.random_state = model_data.get('random_state', self.random_state)

        self.trained = True
        print(f"✓ Model loaded from {path}")
