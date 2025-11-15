"""Data loader combining API and cache"""
from typing import List, Optional
from datetime import datetime
import structlog

from ..config.settings import Settings
from .api_client import EuromillionsAPIClient
from .cache import DrawCache
from .models import Draw

logger = structlog.get_logger()


class DataLoader:
    """Load draws from API with caching

    This class orchestrates data loading by first checking the cache,
    then falling back to the API if needed. It handles all caching
    logic transparently.
    """

    def __init__(self, settings: Settings):
        """Initialize data loader

        Args:
            settings: Application settings
        """
        self.settings = settings
        self.api_client = EuromillionsAPIClient(settings)
        self.cache = DrawCache(settings)
        logger.info("data_loader_initialized")

    def load_draws(
        self,
        year: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        use_cache: bool = True
    ) -> List[Draw]:
        """Load draws with caching

        Args:
            year: Filter by specific year
            start_date: Filter draws from this date
            end_date: Filter draws until this date
            use_cache: Whether to use cached data

        Returns:
            List of Draw objects

        Raises:
            requests.HTTPError: If API request fails
            ValueError: If data validation fails
        """
        params = {
            'year': year,
            'start_date': start_date.isoformat() if start_date else None,
            'end_date': end_date.isoformat() if end_date else None
        }

        # Try cache first
        if use_cache:
            cached = self.cache.get_draws(**params)
            if cached:
                logger.info("loaded_from_cache", count=len(cached))
                return cached

        # Fetch from API
        logger.info("loading_from_api", params=params)
        draws = self.api_client.get_draws(
            year=year,
            start_date=start_date,
            end_date=end_date
        )

        # Cache results
        if use_cache and draws:
            self.cache.set_draws(draws, **params)

        logger.info("loaded_from_api", count=len(draws))
        return draws

    def load_all_historical(self, use_cache: bool = True) -> List[Draw]:
        """Load all historical data from 2004 to present

        Args:
            use_cache: Whether to use cached data

        Returns:
            List of all historical draws

        Note:
            This is a convenience method that fetches all data.
            First call may take several minutes depending on API speed.
        """
        params = {'all_historical': True}

        # Try cache first
        if use_cache:
            cached = self.cache.get_draws(**params)
            if cached:
                logger.info("loaded_all_historical_from_cache", count=len(cached))
                return cached

        # Fetch from API
        logger.info("loading_all_historical_from_api")
        draws = self.api_client.get_all_historical()

        # Cache results
        if use_cache and draws:
            self.cache.set_draws(draws, **params)

        logger.info("loaded_all_historical", count=len(draws))
        return draws

    def get_latest_draw(self, use_cache: bool = True) -> Optional[Draw]:
        """Get most recent draw

        Args:
            use_cache: Whether to use cached data

        Returns:
            Latest Draw object, or None if no draws found
        """
        current_year = datetime.now().year
        draws = self.load_draws(year=current_year, use_cache=use_cache)

        if not draws:
            # Try previous year if current year has no draws yet
            draws = self.load_draws(year=current_year - 1, use_cache=use_cache)

        if draws:
            latest = max(draws, key=lambda d: d.date)
            logger.info("latest_draw", draw_id=latest.draw_id, date=str(latest.date))
            return latest

        logger.warning("no_draws_found")
        return None

    def refresh_cache(self):
        """Force refresh all cached data

        This clears the cache and fetches fresh data from the API.
        Use sparingly to avoid unnecessary API load.
        """
        logger.info("refreshing_cache")
        self.cache.clear()

        # Reload all historical data
        draws = self.api_client.get_all_historical()
        self.cache.set_draws(draws, all_historical=True)

        logger.info("cache_refreshed", count=len(draws))

    def get_cache_stats(self) -> dict:
        """Get cache statistics

        Returns:
            Dictionary with cache information
        """
        return self.cache.get_stats()

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources"""
        self.api_client.__exit__(exc_type, exc_val, exc_tb)
        self.cache.__exit__(exc_type, exc_val, exc_tb)
