"""Feature Normalization for Euromillions ML Predictor

This module provides feature normalization/scaling for ML models.
Supports StandardScaler (z-score normalization) and MinMaxScaler (0-1 scaling).
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
from pathlib import Path
from typing import Literal, Optional


class FeatureNormalizer:
    """Normalize features for ML model input

    Supports two normalization methods:
    - 'standard': StandardScaler (z-score normalization, mean=0, std=1)
    - 'minmax': MinMaxScaler (scales to [0, 1] range)

    Features:
    - Preserves pandas DataFrame structure
    - Saves/loads with joblib (safer than pickle)
    - Supports inverse transformation
    - Method chaining API

    Example:
        >>> normalizer = FeatureNormalizer(method='standard')
        >>> X_normalized = normalizer.fit_transform(X_train)
        >>> normalizer.save('models/scaler.joblib')
    """

    def __init__(self, method: Literal['standard', 'minmax'] = 'standard'):
        """Initialize feature normalizer

        Args:
            method: Normalization method ('standard' or 'minmax')

        Raises:
            ValueError: If method is not 'standard' or 'minmax'
        """
        if method not in ['standard', 'minmax']:
            raise ValueError(f"method must be 'standard' or 'minmax', got '{method}'")

        self.method = method
        if method == 'standard':
            self.scaler = StandardScaler()
        else:
            self.scaler = MinMaxScaler()

        self.fitted = False
        self.feature_names: list = []

    def fit(self, features: pd.DataFrame) -> 'FeatureNormalizer':
        """Fit the normalizer on training data

        Args:
            features: Training features DataFrame

        Returns:
            self for method chaining
        """
        if features.empty:
            raise ValueError("Cannot fit on empty DataFrame")

        self.feature_names = features.columns.tolist()
        self.scaler.fit(features)
        self.fitted = True

        return self

    def transform(self, features: pd.DataFrame) -> pd.DataFrame:
        """Transform features using fitted scaler

        Args:
            features: Features DataFrame to transform

        Returns:
            Normalized features DataFrame with same structure

        Raises:
            ValueError: If normalizer not fitted or feature mismatch
        """
        if not self.fitted:
            raise ValueError("Normalizer must be fitted before transform. Call fit() first.")

        # Validate feature names match
        if list(features.columns) != self.feature_names:
            raise ValueError(
                f"Feature names mismatch. Expected {len(self.feature_names)} features, "
                f"got {len(features.columns)}. "
                f"Expected: {self.feature_names[:5]}... "
                f"Got: {list(features.columns)[:5]}..."
            )

        # Transform
        X_normalized = self.scaler.transform(features)

        # Return as DataFrame with same structure
        return pd.DataFrame(
            X_normalized,
            columns=self.feature_names,
            index=features.index
        )

    def fit_transform(self, features: pd.DataFrame) -> pd.DataFrame:
        """Fit normalizer and transform features in one step

        Args:
            features: Features DataFrame

        Returns:
            Normalized features DataFrame
        """
        return self.fit(features).transform(features)

    def inverse_transform(self, features: pd.DataFrame) -> pd.DataFrame:
        """Reverse normalization to original scale

        Args:
            features: Normalized features DataFrame

        Returns:
            Original scale features DataFrame

        Raises:
            ValueError: If normalizer not fitted
        """
        if not self.fitted:
            raise ValueError("Normalizer must be fitted before inverse_transform")

        X_original = self.scaler.inverse_transform(features)

        return pd.DataFrame(
            X_original,
            columns=self.feature_names,
            index=features.index
        )

    def save(self, path: str) -> None:
        """Save normalizer to disk using joblib

        Args:
            path: Path to save the normalizer

        Example:
            >>> normalizer.save('models/scaler.joblib')
        """
        if not self.fitted:
            raise ValueError("Cannot save unfitted normalizer")

        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save entire normalizer object
        joblib.dump(self, path_obj)

    @classmethod
    def load(cls, path: str) -> 'FeatureNormalizer':
        """Load normalizer from disk

        Args:
            path: Path to the saved normalizer

        Returns:
            Loaded normalizer instance

        Raises:
            FileNotFoundError: If file doesn't exist

        Example:
            >>> normalizer = FeatureNormalizer.load('models/scaler.joblib')
        """
        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Normalizer file not found: {path}")

        return joblib.load(path_obj)

    def get_params(self) -> dict:
        """Get normalizer parameters

        Returns:
            Dictionary with normalizer info
        """
        params = {
            'method': self.method,
            'fitted': self.fitted,
            'n_features': len(self.feature_names),
            'feature_names': self.feature_names[:10] if len(self.feature_names) > 10 else self.feature_names
        }

        if self.fitted and self.method == 'standard':
            params['mean'] = self.scaler.mean_[:5].tolist() if hasattr(self.scaler, 'mean_') else None
            params['scale'] = self.scaler.scale_[:5].tolist() if hasattr(self.scaler, 'scale_') else None
        elif self.fitted and self.method == 'minmax':
            params['min'] = self.scaler.min_[:5].tolist() if hasattr(self.scaler, 'min_') else None
            params['scale'] = self.scaler.scale_[:5].tolist() if hasattr(self.scaler, 'scale_') else None

        return params

    def __repr__(self) -> str:
        """String representation"""
        status = "fitted" if self.fitted else "not fitted"
        n_features = len(self.feature_names) if self.feature_names else 0
        return f"FeatureNormalizer(method='{self.method}', {status}, features={n_features})"

    def __str__(self) -> str:
        """User-friendly string"""
        if not self.fitted:
            return f"FeatureNormalizer(method='{self.method}', not fitted)"

        return (
            f"FeatureNormalizer\n"
            f"  Method: {self.method}\n"
            f"  Status: fitted\n"
            f"  Features: {len(self.feature_names)}\n"
            f"  Sample features: {', '.join(self.feature_names[:5])}..."
        )


# Example usage and testing
if __name__ == "__main__":
    print("Testing FeatureNormalizer...")

    # Create sample data
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'feature_1': np.random.normal(100, 15, 100),
        'feature_2': np.random.normal(50, 10, 100),
        'feature_3': np.random.exponential(20, 100),
        'feature_4': np.random.uniform(0, 100, 100)
    })

    print("\n1. Original Data Statistics:")
    print(sample_data.describe())

    # Test StandardScaler
    print("\n2. Testing StandardScaler (z-score normalization):")
    normalizer_std = FeatureNormalizer(method='standard')
    normalized_std = normalizer_std.fit_transform(sample_data)
    print(normalized_std.describe())
    print(f"\nNormalizer: {normalizer_std}")

    # Test MinMaxScaler
    print("\n3. Testing MinMaxScaler (0-1 scaling):")
    normalizer_mm = FeatureNormalizer(method='minmax')
    normalized_mm = normalizer_mm.fit_transform(sample_data)
    print(normalized_mm.describe())
    print(f"\nNormalizer: {normalizer_mm}")

    # Test save/load
    print("\n4. Testing save/load:")
    normalizer_std.save('/tmp/test_scaler.joblib')
    loaded_normalizer = FeatureNormalizer.load('/tmp/test_scaler.joblib')
    print(f"Loaded: {loaded_normalizer}")
    print(f"Parameters: {loaded_normalizer.get_params()}")

    # Test inverse transform
    print("\n5. Testing inverse transform:")
    reconstructed = loaded_normalizer.inverse_transform(normalized_std)
    print(f"Original mean: {sample_data.mean().values}")
    print(f"Reconstructed mean: {reconstructed.mean().values}")
    print(f"Difference: {np.abs(sample_data.mean().values - reconstructed.mean().values)}")

    print("\n✓ All tests passed!")
