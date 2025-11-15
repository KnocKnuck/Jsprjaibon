"""
Unit tests for RandomForest model implementation.
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import shutil

from euromillions_ml.models.random_forest import RandomForestModel


class TestRandomForestModel:
    """Test cases for RandomForest model."""

    @pytest.fixture
    def sample_data(self):
        """Generate sample training data."""
        np.random.seed(42)
        n_samples = 100
        n_features = 20

        X = np.random.randn(n_samples, n_features)
        y_numbers = np.random.randint(0, 50, size=(n_samples, 5))
        y_stars = np.random.randint(0, 12, size=(n_samples, 2))

        return X, y_numbers, y_stars

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        model = RandomForestModel()

        assert model.name == "RandomForest"
        assert model.n_estimators == 200
        assert model.max_depth == 15
        assert model.random_state == 42
        assert model.trained is False

    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        model = RandomForestModel(n_estimators=100, max_depth=10, random_state=123)

        assert model.n_estimators == 100
        assert model.max_depth == 10
        assert model.random_state == 123

    def test_model_training(self, sample_data):
        """Test model training."""
        X, y_numbers, y_stars = sample_data
        model = RandomForestModel(n_estimators=10)  # Small for faster testing

        model.train(X, y_numbers, y_stars)

        assert model.trained is True
        assert 'n_samples' in model.metadata
        assert 'n_features' in model.metadata
        assert model.metadata['n_samples'] == 100
        assert model.metadata['n_features'] == 20

    def test_model_prediction_untrained(self, sample_data):
        """Test that prediction fails on untrained model."""
        X, _, _ = sample_data
        model = RandomForestModel()

        with pytest.raises(ValueError, match="Model not trained"):
            model.predict(X[:1])

    def test_model_prediction(self, sample_data):
        """Test model prediction after training."""
        X, y_numbers, y_stars = sample_data
        model = RandomForestModel(n_estimators=10)
        model.train(X, y_numbers, y_stars)

        numbers_pred, stars_pred = model.predict(X[:1])

        assert numbers_pred.shape == (50,)
        assert stars_pred.shape == (12,)
        assert np.all(numbers_pred >= 0)
        assert np.all(stars_pred >= 0)

    def test_feature_importance(self, sample_data):
        """Test feature importance extraction."""
        X, y_numbers, y_stars = sample_data
        model = RandomForestModel(n_estimators=10)
        model.train(X, y_numbers, y_stars)

        importance = model.get_feature_importance()

        assert 'numbers' in importance
        assert 'stars' in importance
        assert importance['numbers'].shape == (20,)
        assert importance['stars'].shape == (20,)

    def test_save_and_load(self, sample_data, temp_dir):
        """Test model saving and loading."""
        X, y_numbers, y_stars = sample_data
        model = RandomForestModel(n_estimators=10)
        model.train(X, y_numbers, y_stars)

        # Save model
        save_path = Path(temp_dir) / "test_rf_model.pkl"
        model.save(str(save_path))

        assert save_path.exists()

        # Load model
        new_model = RandomForestModel()
        new_model.load(str(save_path))

        assert new_model.trained is True
        assert new_model.metadata == model.metadata

        # Test prediction matches
        numbers_pred1, stars_pred1 = model.predict(X[:1])
        numbers_pred2, stars_pred2 = new_model.predict(X[:1])

        np.testing.assert_array_almost_equal(numbers_pred1, numbers_pred2)
        np.testing.assert_array_almost_equal(stars_pred1, stars_pred2)

    def test_get_metadata(self, sample_data):
        """Test metadata retrieval."""
        X, y_numbers, y_stars = sample_data
        model = RandomForestModel(n_estimators=10)
        model.train(X, y_numbers, y_stars)

        metadata = model.get_metadata()

        assert isinstance(metadata, dict)
        assert 'model_type' in metadata
        assert metadata['model_type'] == 'RandomForest'
