"""
Unit tests for LSTM model implementation.
"""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import shutil

from euromillions_ml.models.lstm import LSTMModel


class TestLSTMModel:
    """Test cases for LSTM model."""

    @pytest.fixture
    def sample_data(self):
        """Generate sample sequential data."""
        np.random.seed(42)
        n_samples = 50
        sequence_length = 10
        n_features = 10

        X = np.random.randn(n_samples, sequence_length, n_features)
        # For LSTM, y should be single values or one-hot encoded
        y_numbers = np.random.randint(0, 50, size=(n_samples, 1))
        y_stars = np.random.randint(0, 12, size=(n_samples, 1))

        return X, y_numbers, y_stars

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    def test_model_initialization(self):
        """Test model initialization with default parameters."""
        model = LSTMModel()

        assert model.name == "LSTM"
        assert model.sequence_length == 10
        assert model.hidden_units == 128
        assert model.dropout == 0.3
        assert model.trained is False
        assert model.model is None

    def test_model_initialization_custom_params(self):
        """Test model initialization with custom parameters."""
        model = LSTMModel(sequence_length=5, hidden_units=64, dropout=0.2)

        assert model.sequence_length == 5
        assert model.hidden_units == 64
        assert model.dropout == 0.2

    def test_model_training(self, sample_data):
        """Test model training."""
        X, y_numbers, y_stars = sample_data
        model = LSTMModel(sequence_length=10, hidden_units=32)

        # Train with fewer epochs for testing
        model.train(X, y_numbers, y_stars, epochs=2, batch_size=16)

        assert model.trained is True
        assert model.model is not None
        assert 'model_type' in model.metadata
        assert model.metadata['model_type'] == 'LSTM'
        assert 'epochs_trained' in model.metadata

    def test_model_prediction_untrained(self, sample_data):
        """Test that prediction fails on untrained model."""
        X, _, _ = sample_data
        model = LSTMModel()

        with pytest.raises(ValueError, match="Model not trained"):
            model.predict(X[:1])

    def test_model_prediction(self, sample_data):
        """Test model prediction after training."""
        X, y_numbers, y_stars = sample_data
        model = LSTMModel(sequence_length=10, hidden_units=32)
        model.train(X, y_numbers, y_stars, epochs=2, batch_size=16)

        numbers_pred, stars_pred = model.predict(X[:1])

        assert numbers_pred.shape == (50,)
        assert stars_pred.shape == (12,)
        # Probabilities should sum to ~1 (softmax output)
        assert np.abs(numbers_pred.sum() - 1.0) < 0.01
        assert np.abs(stars_pred.sum() - 1.0) < 0.01

    def test_save_and_load(self, sample_data, temp_dir):
        """Test model saving and loading."""
        X, y_numbers, y_stars = sample_data
        model = LSTMModel(sequence_length=10, hidden_units=32)
        model.train(X, y_numbers, y_stars, epochs=2, batch_size=16)

        # Save model
        save_path = Path(temp_dir) / "test_lstm_model"
        model.save(str(save_path))

        assert Path(str(save_path) + '.h5').exists()
        assert Path(str(save_path) + '.json').exists()

        # Load model
        new_model = LSTMModel()
        new_model.load(str(save_path))

        assert new_model.trained is True
        assert new_model.model is not None

        # Test prediction matches (approximately, due to floating point)
        numbers_pred1, stars_pred1 = model.predict(X[:1])
        numbers_pred2, stars_pred2 = new_model.predict(X[:1])

        np.testing.assert_array_almost_equal(numbers_pred1, numbers_pred2, decimal=5)
        np.testing.assert_array_almost_equal(stars_pred1, stars_pred2, decimal=5)

    def test_get_metadata(self, sample_data):
        """Test metadata retrieval."""
        X, y_numbers, y_stars = sample_data
        model = LSTMModel(sequence_length=10, hidden_units=32)
        model.train(X, y_numbers, y_stars, epochs=2, batch_size=16)

        metadata = model.get_metadata()

        assert isinstance(metadata, dict)
        assert 'model_type' in metadata
        assert metadata['model_type'] == 'LSTM'
        assert 'sequence_length' in metadata
        assert 'hidden_units' in metadata

    def test_model_architecture(self, sample_data):
        """Test that model builds with correct architecture."""
        X, y_numbers, y_stars = sample_data
        model = LSTMModel(sequence_length=10, hidden_units=32)
        model.train(X, y_numbers, y_stars, epochs=1, batch_size=16)

        # Check model has expected outputs
        assert len(model.model.outputs) == 2
        assert model.model.outputs[0].shape[1] == 50  # numbers output
        assert model.model.outputs[1].shape[1] == 12  # stars output
