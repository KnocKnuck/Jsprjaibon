"""Tests for Euromillions API client"""
import pytest
import requests
import responses
from datetime import datetime, date
from unittest.mock import patch, Mock

from data.api_client import EuromillionsAPIClient
from data.models import Draw


@pytest.mark.unit
class TestAPIClientInitialization:
    """Test API client initialization"""

    def test_client_initialization(self, test_settings):
        """Test that client initializes correctly"""
        client = EuromillionsAPIClient(test_settings)

        assert client.base_url == str(test_settings.api.base_url)
        assert client.timeout == test_settings.api.timeout
        assert client.session is not None
        assert 'User-Agent' in client.session.headers
        assert client.session.headers['User-Agent'] == 'EuromillionsMLPredictor/1.0'
        assert client.session.headers['Accept'] == 'application/json'

    def test_client_context_manager(self, test_settings):
        """Test client works as context manager"""
        with EuromillionsAPIClient(test_settings) as client:
            assert client is not None
            assert client.session is not None


@pytest.mark.unit
class TestAPIClientRequests:
    """Test API client HTTP requests"""

    @responses.activate
    def test_successful_get_request(self, test_settings, mock_api_response):
        """Test successful GET request"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        result = client._get('v1/draws')

        assert result == mock_api_response
        assert len(responses.calls) == 1

    @responses.activate
    def test_get_request_with_params(self, test_settings, mock_api_response):
        """Test GET request with query parameters"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        params = {'year': 2024, 'limit': 10}
        result = client._get('v1/draws', params=params)

        assert result == mock_api_response
        assert len(responses.calls) == 1
        # Verify params were sent
        assert 'year=2024' in responses.calls[0].request.url
        assert 'limit=10' in responses.calls[0].request.url

    @responses.activate
    def test_http_error_handling(self, test_settings):
        """Test handling of HTTP errors"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json={"error": "Not Found"},
            status=404
        )

        client = EuromillionsAPIClient(test_settings)

        with pytest.raises(requests.HTTPError):
            client._get('v1/draws')

    @responses.activate
    def test_timeout_handling(self, test_settings):
        """Test handling of timeouts"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            body=requests.Timeout("Connection timeout")
        )

        client = EuromillionsAPIClient(test_settings)

        with pytest.raises(requests.Timeout):
            client._get('v1/draws')

    @responses.activate
    def test_retry_logic(self, test_settings):
        """Test that retry logic works on failures"""
        # First call fails, subsequent calls succeed
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json={"error": "Server Error"},
            status=500
        )
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json={"error": "Server Error"},
            status=500
        )
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=[{"id": 1, "draw_id": 2024001}],
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        result = client._get('v1/draws')

        # Should have retried and eventually succeeded
        assert result == [{"id": 1, "draw_id": 2024001}]
        assert len(responses.calls) == 3


@pytest.mark.unit
class TestGetDraws:
    """Test get_draws method"""

    @responses.activate
    def test_get_draws_no_params(self, test_settings, mock_api_response):
        """Test getting draws without parameters"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        draws = client.get_draws()

        assert len(draws) == 2
        assert all(isinstance(draw, Draw) for draw in draws)
        assert draws[0].draw_id == 2024001
        assert draws[1].draw_id == 2024002

    @responses.activate
    def test_get_draws_by_year(self, test_settings, mock_api_response):
        """Test getting draws filtered by year"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        draws = client.get_draws(year=2024)

        assert len(draws) == 2
        assert 'year=2024' in responses.calls[0].request.url

    @responses.activate
    def test_get_draws_by_date_range(self, test_settings, mock_api_response):
        """Test getting draws filtered by date range"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 1, 31)
        draws = client.get_draws(start_date=start_date, end_date=end_date)

        assert len(draws) == 2
        assert 'start_date=2024-01-01' in responses.calls[0].request.url
        assert 'end_date=2024-01-31' in responses.calls[0].request.url

    @responses.activate
    def test_get_draws_with_limit(self, test_settings, mock_api_response):
        """Test getting draws with limit"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        draws = client.get_draws(limit=10)

        assert len(draws) == 2
        assert 'limit=10' in responses.calls[0].request.url

    @responses.activate
    def test_get_draws_validation_error(self, test_settings):
        """Test handling of invalid draw data"""
        # Invalid data - numbers out of range
        invalid_response = [{
            "id": 1,
            "draw_id": 2024001,
            "numbers": [1, 2, 3, 4, 99],  # 99 is out of range
            "stars": [5, 9],
            "date": "2024-01-05",
            "has_winner": True,
            "prizes": []
        }]

        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=invalid_response,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)

        with pytest.raises(ValueError, match="Failed to validate draw data"):
            client.get_draws()


@pytest.mark.unit
class TestGetDrawById:
    """Test get_draw_by_id method"""

    @responses.activate
    def test_get_draw_by_id_success(self, test_settings, mock_api_response):
        """Test getting a specific draw by ID"""
        draw_data = mock_api_response[0]

        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws/1",
            json=draw_data,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)
        draw = client.get_draw_by_id(1)

        assert isinstance(draw, Draw)
        assert draw.draw_id == 2024001
        assert draw.numbers == [3, 12, 23, 34, 45]
        assert draw.stars == [5, 9]

    @responses.activate
    def test_get_draw_by_id_not_found(self, test_settings):
        """Test getting non-existent draw"""
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws/999999",
            json={"error": "Not Found"},
            status=404
        )

        client = EuromillionsAPIClient(test_settings)

        with pytest.raises(requests.HTTPError):
            client.get_draw_by_id(999999)

    @responses.activate
    def test_get_draw_by_id_validation_error(self, test_settings):
        """Test handling of invalid draw data by ID"""
        invalid_draw = {
            "id": 1,
            "draw_id": 2024001,
            "numbers": [1, 2, 3, 4, 99],  # Invalid
            "stars": [5, 9],
            "date": "2024-01-05",
            "has_winner": True,
            "prizes": []
        }

        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws/1",
            json=invalid_draw,
            status=200
        )

        client = EuromillionsAPIClient(test_settings)

        with pytest.raises(ValueError, match="Failed to validate draw 1"):
            client.get_draw_by_id(1)


@pytest.mark.unit
@pytest.mark.slow
class TestGetAllHistorical:
    """Test get_all_historical method"""

    @responses.activate
    def test_get_all_historical_success(self, test_settings, mock_api_response):
        """Test getting all historical data"""
        # Mock responses for multiple years
        current_year = datetime.now().year

        for year in range(current_year - 1, current_year + 1):
            responses.add(
                responses.GET,
                f"{test_settings.api.base_url}/v1/draws",
                json=mock_api_response,
                status=200
            )

        client = EuromillionsAPIClient(test_settings)
        draws = client.get_all_historical(start_year=current_year - 1)

        # Should have data from 2 years
        assert len(draws) == 4  # 2 draws per year
        assert all(isinstance(draw, Draw) for draw in draws)

    @responses.activate
    def test_get_all_historical_with_failures(self, test_settings, mock_api_response):
        """Test that get_all_historical continues even if some years fail"""
        current_year = datetime.now().year

        # First year succeeds
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_api_response,
            status=200
        )

        # Second year fails
        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json={"error": "Server Error"},
            status=500
        )

        client = EuromillionsAPIClient(test_settings)
        draws = client.get_all_historical(start_year=current_year - 1)

        # Should still have data from successful year
        assert len(draws) == 2
        assert all(isinstance(draw, Draw) for draw in draws)


@pytest.mark.unit
class TestRateLimiting:
    """Test rate limiting behavior"""

    @responses.activate
    def test_rate_limiting_delays_requests(self, test_settings, mock_api_response):
        """Test that rate limiting introduces delays"""
        import time

        # Add multiple successful responses
        for _ in range(3):
            responses.add(
                responses.GET,
                f"{test_settings.api.base_url}/v1/draws",
                json=mock_api_response,
                status=200
            )

        client = EuromillionsAPIClient(test_settings)

        start_time = time.time()

        # Make 3 requests - should be rate limited
        for _ in range(3):
            client._get('v1/draws')

        elapsed = time.time() - start_time

        # With 1 request per 2 seconds, 3 requests should take at least 4 seconds
        # (0s, 2s, 4s)
        assert elapsed >= 4.0, f"Rate limiting not working: {elapsed}s elapsed"


@pytest.mark.api
@pytest.mark.integration
class TestRealAPIConnection:
    """Integration tests with real API (skipped by default)"""

    @pytest.mark.skip(reason="Requires real API access")
    def test_real_api_connection(self, test_settings):
        """Test actual API connection (manual test)"""
        client = EuromillionsAPIClient(test_settings)
        draws = client.get_draws(limit=5)

        assert len(draws) <= 5
        assert all(isinstance(draw, Draw) for draw in draws)

    @pytest.mark.skip(reason="Requires real API access")
    def test_real_api_get_by_id(self, test_settings):
        """Test getting real draw by ID (manual test)"""
        client = EuromillionsAPIClient(test_settings)
        # Use a known draw ID
        draw = client.get_draw_by_id(1)

        assert isinstance(draw, Draw)
        assert draw.id == 1
