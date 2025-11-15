"""Tests for the backtest engine"""
import pytest
import pandas as pd
from datetime import date, timedelta

from euromillions_ml.prediction.backtest import BacktestEngine, BacktestResult
from euromillions_ml.prediction.predictor import Predictor, PredictionGrid
from euromillions_ml.models.dummy import DummyModel
from euromillions_ml.features.engineering import FeatureEngineer
from euromillions_ml.features.normalizer import FeatureNormalizer
from data.models import Draw


@pytest.fixture
def sample_draws():
    """Create sample draws for testing"""
    draws = []
    base_date = date(2024, 1, 1)

    for i in range(150):
        draw = Draw(
            id=i,
            draw_id=i,
            numbers=[1 + (i % 10), 11 + (i % 10), 21 + (i % 10), 31 + (i % 10), 41 + (i % 9)],
            stars=[1 + (i % 2), 3 + (i % 2)],
            date=base_date + timedelta(days=i * 3),
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


@pytest.fixture
def backtest_engine(predictor):
    """Create backtest engine instance"""
    return BacktestEngine(predictor)


def test_backtest_result_initialization():
    """Test BacktestResult initialization"""
    result = BacktestResult()

    assert result.predictions == []
    assert result.actuals == []
    assert result.metrics == {}
    assert len(result.hits_distribution) == 0


def test_backtest_result_add_result():
    """Test adding results to BacktestResult"""
    result = BacktestResult()

    grid = PredictionGrid([5, 10, 15, 20, 25], [3, 7], 0.75, "test")
    draw = Draw(
        id=1, draw_id=1, numbers=[5, 10, 12, 20, 30], stars=[3, 9],
        date=date(2024, 1, 1), has_winner=True
    )

    result.add_result(grid, draw)

    assert len(result.predictions) == 1
    assert len(result.actuals) == 1
    assert "3+1" in result.hits_distribution  # 3 numbers match, 1 star matches


def test_backtest_result_calculate_metrics():
    """Test metrics calculation"""
    result = BacktestResult()

    # Add some results
    for i in range(10):
        grid = PredictionGrid([1, 2, 3, 4, 5], [1, 2], 0.75, "test")
        draw = Draw(
            id=i, draw_id=i, numbers=[1, 2, 6, 7, 8], stars=[1, 3],
            date=date(2024, 1, 1), has_winner=False
        )
        result.add_result(grid, draw)

    result.calculate_metrics()

    assert result.metrics['total_draws'] == 10
    assert 'avg_numbers_accuracy' in result.metrics
    assert 'avg_stars_accuracy' in result.metrics
    assert 'avg_confidence' in result.metrics
    assert 'hits_distribution' in result.metrics
    assert 'best_prediction' in result.metrics


def test_backtest_result_to_dataframe():
    """Test conversion to DataFrame"""
    result = BacktestResult()

    grid = PredictionGrid([5, 10, 15, 20, 25], [3, 7], 0.75, "test")
    draw = Draw(
        id=1, draw_id=1, numbers=[5, 10, 12, 20, 30], stars=[3, 9],
        date=date(2024, 1, 1), has_winner=True
    )

    result.add_result(grid, draw)

    df = result.to_dataframe()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert 'date' in df.columns
    assert 'predicted_numbers' in df.columns
    assert 'actual_numbers' in df.columns
    assert 'numbers_hit' in df.columns
    assert 'stars_hit' in df.columns


def test_backtest_engine_run_backtest(backtest_engine, sample_draws):
    """Test running a backtest"""
    result = backtest_engine.run_backtest(sample_draws, window_months=3)

    assert isinstance(result, BacktestResult)
    assert result.metrics['total_draws'] > 0
    assert 'avg_numbers_accuracy' in result.metrics
    assert 'avg_stars_accuracy' in result.metrics


def test_backtest_engine_window_filtering(backtest_engine, sample_draws):
    """Test that backtest window filtering works"""
    # Test with small window
    result_small = backtest_engine.run_backtest(sample_draws, window_months=1)

    # Test with larger window
    result_large = backtest_engine.run_backtest(sample_draws, window_months=6)

    # Larger window should have more draws
    assert result_large.metrics['total_draws'] >= result_small.metrics['total_draws']


def test_backtest_engine_minimum_training_draws(backtest_engine, sample_draws):
    """Test minimum training draws requirement"""
    # Use only first 60 draws - many won't have enough training data
    small_sample = sample_draws[:60]

    result = backtest_engine.run_backtest(
        small_sample,
        window_months=12,
        min_training_draws=50
    )

    # Should have fewer results due to min training requirement
    assert result.metrics['total_draws'] < 10


def test_backtest_hits_distribution(backtest_engine, sample_draws):
    """Test that hits distribution is calculated correctly"""
    result = backtest_engine.run_backtest(sample_draws, window_months=3)

    hits_dist = result.metrics['hits_distribution']

    # Should have various hit patterns
    assert isinstance(hits_dist, dict)
    assert len(hits_dist) > 0

    # All values should be non-negative
    assert all(count >= 0 for count in hits_dist.values())


def test_backtest_best_prediction(backtest_engine, sample_draws):
    """Test that best prediction is identified"""
    result = backtest_engine.run_backtest(sample_draws, window_months=3)

    best = result.metrics['best_prediction']

    if best:
        assert 'date' in best
        assert 'predicted_numbers' in best
        assert 'actual_numbers' in best
        assert 'numbers_hit' in best
        assert 'stars_hit' in best
        assert 'score' in best


def test_backtest_empty_result():
    """Test backtest with no predictions"""
    result = BacktestResult()
    result.calculate_metrics()

    assert result.metrics['total_draws'] == 0
    assert result.metrics['avg_numbers_accuracy'] == 0
    assert result.metrics['best_prediction'] is None


def test_walk_forward_validation(backtest_engine, sample_draws):
    """Test walk-forward validation"""
    results = backtest_engine.walk_forward_validation(
        sample_draws,
        test_size=10,
        step_size=5
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(r, BacktestResult) for r in results)
