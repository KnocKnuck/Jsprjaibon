"""Tests for the prediction engine"""
import pytest
import numpy as np
from datetime import date

from euromillions_ml.prediction.predictor import Predictor, PredictionGrid
from euromillions_ml.models.dummy import DummyModel
from euromillions_ml.features.engineering import FeatureEngineer
from euromillions_ml.features.normalizer import FeatureNormalizer
from data.models import Draw


@pytest.fixture
def sample_draws():
    """Create sample draws for testing"""
    draws = []
    for i in range(100):
        draw = Draw(
            id=i,
            draw_id=i,
            numbers=[1 + (i % 10), 11 + (i % 10), 21 + (i % 10), 31 + (i % 10), 41 + (i % 9)],
            stars=[1 + (i % 2), 3 + (i % 2)],
            date=date(2024, 1, 1) + __import__('datetime').timedelta(days=i * 3),
            has_winner=i % 5 == 0
        )
        draws.append(draw)
    return draws


@pytest.fixture
def predictor(sample_draws):
    """Create predictor instance"""
    model = DummyModel()
    feature_engineer = FeatureEngineer()
    normalizer = FeatureNormalizer()

    # Fit normalizer
    features = feature_engineer.extract_all_features(sample_draws)
    normalizer.fit(features)

    return Predictor(model, feature_engineer, normalizer)


def test_prediction_grid_creation():
    """Test PredictionGrid creation"""
    grid = PredictionGrid([5, 10, 15, 20, 25], [3, 7], 0.75, "test_method")

    assert grid.numbers == [5, 10, 15, 20, 25]
    assert grid.stars == [3, 7]
    assert grid.confidence == 0.75
    assert grid.method == "test_method"


def test_prediction_grid_sorting():
    """Test that numbers and stars are sorted"""
    grid = PredictionGrid([25, 5, 20, 10, 15], [7, 3], 0.75, "test")

    assert grid.numbers == [5, 10, 15, 20, 25]
    assert grid.stars == [3, 7]


def test_predict_generates_grids(predictor, sample_draws):
    """Test that predictor generates correct number of grids"""
    grids = predictor.predict(sample_draws, n_grids=3)

    assert len(grids) == 3
    assert all(isinstance(g, PredictionGrid) for g in grids)


def test_predict_valid_ranges(predictor, sample_draws):
    """Test that predicted numbers are in valid ranges"""
    grids = predictor.predict(sample_draws, n_grids=5)

    for grid in grids:
        # Check numbers
        assert len(grid.numbers) == 5
        assert all(1 <= n <= 50 for n in grid.numbers)
        assert len(set(grid.numbers)) == 5  # No duplicates

        # Check stars
        assert len(grid.stars) == 2
        assert all(1 <= s <= 12 for s in grid.stars)
        assert len(set(grid.stars)) == 2  # No duplicates


def test_predict_confidence_scores(predictor, sample_draws):
    """Test that confidence scores are valid"""
    grids = predictor.predict(sample_draws, n_grids=5)

    for grid in grids:
        assert 0 <= grid.confidence <= 1


def test_predict_different_methods(predictor, sample_draws):
    """Test that different generation methods are used"""
    grids = predictor.predict(sample_draws, n_grids=3)

    # First grid should use top probabilities
    assert grids[0].method == "top_probabilities"

    # Other grids should use weighted sampling
    for grid in grids[1:]:
        assert grid.method == "weighted_sampling"


def test_predict_insufficient_data():
    """Test prediction with insufficient data"""
    model = DummyModel()
    feature_engineer = FeatureEngineer()
    normalizer = FeatureNormalizer()

    predictor = Predictor(model, feature_engineer, normalizer)

    # Very few draws
    draws = [
        Draw(
            id=1, draw_id=1, numbers=[1, 2, 3, 4, 5], stars=[1, 2],
            date=date(2024, 1, 1), has_winner=True
        )
    ]

    with pytest.raises(ValueError):
        predictor.predict(draws, n_grids=2)


def test_grid_to_dict():
    """Test PredictionGrid to_dict conversion"""
    grid = PredictionGrid([5, 10, 15, 20, 25], [3, 7], 0.75, "test_method")
    grid_dict = grid.to_dict()

    assert grid_dict['numbers'] == [5, 10, 15, 20, 25]
    assert grid_dict['stars'] == [3, 7]
    assert grid_dict['confidence'] == 0.75
    assert grid_dict['method'] == "test_method"
    assert 'generated_at' in grid_dict
