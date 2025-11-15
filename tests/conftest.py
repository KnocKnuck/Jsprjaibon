"""Pytest configuration and shared fixtures"""
import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import date, datetime
from typing import List
import responses

from config.settings import Settings, APISettings, DataSettings, LotterySettings
from data.models import Draw, Prize


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def test_settings(temp_dir):
    """Create test settings with temporary cache directory"""
    return Settings(
        api=APISettings(
            base_url="https://euromillions.api.pedromealha.dev",
            timeout=30,
            rate_limit=2.0,
            retry_attempts=4,
            retry_backoff=2.0
        ),
        data=DataSettings(
            cache_dir=str(temp_dir / "cache"),
            cache_ttl_historical=0,
            cache_ttl_current=86400
        ),
        lottery=LotterySettings(
            numbers_range=(1, 50),
            stars_range=(1, 12),
            numbers_count=5,
            stars_count=2
        )
    )


@pytest.fixture
def sample_prize():
    """Create a sample Prize object"""
    return Prize(
        prize_amount=1000000.0,
        winners_count=1,
        matched_numbers=5,
        matched_stars=2
    )


@pytest.fixture
def sample_draw(sample_prize):
    """Create a sample Draw object"""
    return Draw(
        id=1,
        draw_id=2024001,
        numbers=[3, 12, 23, 34, 45],
        stars=[5, 9],
        date=date(2024, 1, 5),
        has_winner=True,
        prizes=[sample_prize]
    )


@pytest.fixture
def sample_draws(sample_prize):
    """Create multiple sample draws for testing"""
    draws = []
    for i in range(10):
        draw = Draw(
            id=i + 1,
            draw_id=2024000 + i + 1,
            numbers=[(i * 5 + j) % 50 + 1 for j in range(5)],
            stars=[(i % 11) + 1, ((i + 1) % 11) + 1],
            date=date(2024, 1, i + 1),
            has_winner=i % 3 == 0,
            prizes=[sample_prize] if i % 3 == 0 else []
        )
        draws.append(draw)
    return draws


@pytest.fixture
def historical_draws():
    """Create a larger set of historical draws"""
    draws = []
    for year in [2022, 2023]:
        for month in range(1, 13):
            for day in [5, 15, 25]:
                try:
                    draw_date = date(year, month, day)
                    draw = Draw(
                        id=len(draws) + 1,
                        draw_id=(year * 1000) + (month * 10) + day,
                        numbers=[1 + (len(draws) * 3 + i) % 50 for i in range(5)],
                        stars=[1 + (len(draws) % 11), 1 + ((len(draws) + 1) % 11)],
                        date=draw_date,
                        has_winner=len(draws) % 5 == 0,
                        prizes=[]
                    )
                    draws.append(draw)
                except ValueError:
                    # Skip invalid dates
                    continue
    return draws


@pytest.fixture
def mock_api_response():
    """Mock API response data"""
    return [
        {
            "id": 1,
            "draw_id": 2024001,
            "numbers": [3, 12, 23, 34, 45],
            "stars": [5, 9],
            "date": "2024-01-05",
            "has_winner": True,
            "prizes": [
                {
                    "prize_amount": 1000000.0,
                    "winners_count": 1,
                    "matched_numbers": 5,
                    "matched_stars": 2
                }
            ]
        },
        {
            "id": 2,
            "draw_id": 2024002,
            "numbers": [7, 15, 22, 38, 49],
            "stars": [2, 11],
            "date": "2024-01-09",
            "has_winner": False,
            "prizes": []
        }
    ]


@pytest.fixture
def mock_responses_api():
    """Setup responses mock for API testing"""
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mock_successful_api(mock_responses_api, mock_api_response):
    """Mock successful API calls"""
    mock_responses_api.add(
        responses.GET,
        "https://euromillions.api.pedromealha.dev/v1/draws",
        json=mock_api_response,
        status=200
    )
    return mock_responses_api


@pytest.fixture
def mock_failed_api(mock_responses_api):
    """Mock failed API calls"""
    mock_responses_api.add(
        responses.GET,
        "https://euromillions.api.pedromealha.dev/v1/draws",
        json={"error": "Internal Server Error"},
        status=500
    )
    return mock_responses_api


@pytest.fixture
def mock_timeout_api(mock_responses_api):
    """Mock API timeout"""
    import requests
    mock_responses_api.add(
        responses.GET,
        "https://euromillions.api.pedromealha.dev/v1/draws",
        body=requests.Timeout("Connection timeout")
    )
    return mock_responses_api


@pytest.fixture
def sample_features():
    """Create sample feature data for ML models"""
    import numpy as np
    return {
        'number_frequency': np.random.rand(50),
        'star_frequency': np.random.rand(12),
        'hot_numbers': [1, 5, 12, 23, 45],
        'cold_numbers': [7, 14, 28, 39, 44],
        'gap_analysis': np.random.randint(1, 20, size=50),
        'consecutive_pairs': 3,
        'odd_even_ratio': 0.6,
        'high_low_ratio': 0.4,
        'sum_total': 135
    }


@pytest.fixture
def sample_feature_matrix():
    """Create a sample feature matrix for ML training"""
    import numpy as np
    # 100 samples, 200+ features
    return np.random.rand(100, 250)


@pytest.fixture
def sample_target_numbers():
    """Create sample target numbers for training"""
    import numpy as np
    # 100 samples, 5 numbers each
    return np.random.randint(1, 51, size=(100, 5))


@pytest.fixture
def sample_target_stars():
    """Create sample target stars for training"""
    import numpy as np
    # 100 samples, 2 stars each
    return np.random.randint(1, 13, size=(100, 2))


@pytest.fixture
def trained_model_path(temp_dir):
    """Path for saving trained models during tests"""
    model_dir = temp_dir / "models"
    model_dir.mkdir(exist_ok=True)
    return model_dir


@pytest.fixture
def config_yaml_path(temp_dir):
    """Create a temporary config.yaml for testing"""
    config_content = """
api:
  base_url: https://euromillions.api.pedromealha.dev
  timeout: 30
  rate_limit: 2.0
  retry_attempts: 4
  retry_backoff: 2.0

data:
  cache_dir: {cache_dir}
  cache_ttl_historical: 0
  cache_ttl_current: 86400

lottery:
  numbers_range: [1, 50]
  stars_range: [1, 12]
  numbers_count: 5
  stars_count: 2
"""
    config_file = temp_dir / "test_config.yaml"
    config_file.write_text(config_content.format(cache_dir=str(temp_dir / "cache")))
    return config_file


# Markers for test categorization
def pytest_configure(config):
    """Configure custom markers"""
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "slow: slow running tests")
    config.addinivalue_line("markers", "api: tests requiring API access")
    config.addinivalue_line("markers", "model: tests involving ML models")


# Test data cleanup
@pytest.fixture(autouse=True)
def cleanup_test_artifacts():
    """Automatically cleanup test artifacts after each test"""
    yield
    # Cleanup is handled by temp_dir fixture
