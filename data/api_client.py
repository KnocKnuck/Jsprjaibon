"""API client for pedro-mealha/euromillions-api"""
import requests
from typing import List, Optional
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
try:
    from ratelimit import limits, sleep_and_retry
except ImportError:
    # Fallback to shim if ratelimit not available
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from ratelimit_shim import limits, sleep_and_retry
import structlog

from config.settings import Settings
from data.models import Draw

logger = structlog.get_logger()


class EuromillionsAPIClient:
    """Client for Euromillions API with retry and rate limiting

    Features:
    - Automatic retry on network failures (up to 4 attempts)
    - Exponential backoff between retries
    - Rate limiting (1 request per 2 seconds)
    - Structured logging for all API calls
    """

    def __init__(self, settings: Settings):
        """Initialize API client

        Args:
            settings: Application settings with API configuration
        """
        self.settings = settings
        self.base_url = str(settings.api.base_url)
        self.timeout = settings.api.timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'EuromillionsMLPredictor/1.0',
            'Accept': 'application/json'
        })
        logger.info("api_client_initialized", base_url=self.base_url)

    @sleep_and_retry
    @limits(calls=1, period=2)  # 1 call per 2 seconds
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=2, max=16),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout)),
        reraise=True
    )
    def _get(self, endpoint: str, params: Optional[dict] = None) -> dict:
        """Make GET request with retry logic

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            requests.HTTPError: If request fails after all retries
            requests.Timeout: If request times out
        """
        url = f"{self.base_url}/{endpoint}"
        logger.info("api_request", url=url, params=params)

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            logger.info("api_response_success", url=url, status=response.status_code)
            return data
        except requests.HTTPError as e:
            logger.error("api_http_error", url=url, status=e.response.status_code, error=str(e))
            raise
        except requests.Timeout as e:
            logger.error("api_timeout", url=url, timeout=self.timeout, error=str(e))
            raise
        except Exception as e:
            logger.error("api_error", url=url, error=str(e))
            raise

    def get_draws(
        self,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Draw]:
        """Fetch draws from API

        Args:
            year: Filter by specific year
            start_date: Filter draws from this date
            end_date: Filter draws until this date
            limit: Maximum number of draws to return

        Returns:
            List of validated Draw objects

        Raises:
            requests.HTTPError: If API request fails
            ValueError: If draw data fails validation
        """
        params = {}
        if year:
            params['year'] = year
        if start_date:
            params['start_date'] = start_date.strftime('%Y-%m-%d')
        if end_date:
            params['end_date'] = end_date.strftime('%Y-%m-%d')
        if limit:
            params['limit'] = limit

        data = self._get('v1/draws', params)

        # Validate and convert to Draw objects
        try:
            draws = [Draw(**draw_data) for draw_data in data]
            logger.info("draws_fetched", count=len(draws), params=params)
            return draws
        except Exception as e:
            logger.error("draw_validation_error", error=str(e), data=data)
            raise ValueError(f"Failed to validate draw data: {e}")

    def get_draw_by_id(self, draw_id: int) -> Draw:
        """Fetch specific draw by ID

        Args:
            draw_id: Unique draw identifier

        Returns:
            Validated Draw object

        Raises:
            requests.HTTPError: If draw not found or API error
            ValueError: If draw data fails validation
        """
        data = self._get(f'v1/draws/{draw_id}')
        try:
            draw = Draw(**data)
            logger.info("draw_fetched", draw_id=draw_id)
            return draw
        except Exception as e:
            logger.error("draw_validation_error", draw_id=draw_id, error=str(e))
            raise ValueError(f"Failed to validate draw {draw_id}: {e}")

    def get_all_historical(self, start_year: int = 2004) -> List[Draw]:
        """Fetch all historical data from start_year to present

        Args:
            start_year: First year to fetch (default: 2004, first Euromillions draw)

        Returns:
            List of all historical draws

        Note:
            This method makes multiple API calls (one per year) and may take time.
            Consider using caching for subsequent calls.
        """
        current_year = datetime.now().year
        all_draws = []

        for year in range(start_year, current_year + 1):
            logger.info("fetching_year", year=year)
            try:
                draws = self.get_draws(year=year)
                all_draws.extend(draws)
                logger.info("year_fetched", year=year, count=len(draws))
            except Exception as e:
                logger.error("year_fetch_failed", year=year, error=str(e))
                # Continue with other years even if one fails
                continue

        logger.info("historical_fetch_complete", total_draws=len(all_draws))
        return all_draws

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up session on exit"""
        self.session.close()
