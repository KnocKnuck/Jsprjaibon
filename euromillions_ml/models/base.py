"""
Base model interface for EuroMillions ML models.

This module defines the abstract base class that all prediction models
must implement, ensuring consistent interfaces across different model types.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Tuple, Optional
import joblib


class BaseModel(ABC):
    """
    Abstract base class for all EuroMillions prediction models.

    All models (LSTM, RandomForest, etc.) must inherit from this class
    and implement the required abstract methods.

    Attributes:
        name (str): Name identifier for the model
        trained (bool): Whether the model has been trained
        metadata (Dict): Model metadata including hyperparameters and training info
    """

    def __init__(self, name: str):
        """
        Initialize the base model.

        Args:
            name: Identifier name for the model
        """
        self.name = name
        self.trained = False
        self.metadata = {}

    @abstractmethod
    def train(self, X: np.ndarray, y_numbers: np.ndarray, y_stars: np.ndarray):
        """
        Train the model on provided data.

        Args:
            X: Input features array of shape (n_samples, n_features)
            y_numbers: Target array for main numbers
            y_stars: Target array for star numbers
        """
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate predictions for numbers and stars.

        Args:
            X: Input features array

        Returns:
            Tuple of (numbers_probabilities, stars_probabilities)
        """
        pass

    @abstractmethod
    def save(self, path: str):
        """
        Save the trained model to disk.

        Args:
            path: File path where model should be saved
        """
        pass

    @abstractmethod
    def load(self, path: str):
        """
        Load a trained model from disk.

        Args:
            path: File path from which to load the model
        """
        pass

    def get_metadata(self) -> Dict:
        """
        Get model metadata and configuration.

        Returns:
            Dictionary containing model metadata
        """
        return self.metadata

    def is_trained(self) -> bool:
        """
        Check if the model has been trained.

        Returns:
            True if model is trained, False otherwise
        """
        return self.trained
