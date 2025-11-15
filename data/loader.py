"""Data loader combining API and cache"""
from typing import List, Optional
from datetime import datetime
import structlog

from config.settings import Settings
from data.api_client import EuromillionsAPIClient
from data.cache import DrawCache
from data.models import Draw

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
        use_cache: bool = True,
        use_csv_fallback: bool = False
    ) -> List[Draw]:
        """Load draws with caching

        Args:
            year: Filter by specific year
            start_date: Filter draws from this date
            end_date: Filter draws until this date
            use_cache: Whether to use cached data
            use_csv_fallback: Whether to fall back to CSV if API fails

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

        # Try API
        try:
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

        except Exception as e:
            if use_csv_fallback:
                logger.warning("api_failed_using_csv", error=str(e))
                from data.csv_fallback import load_from_csv, create_sample_csv

                try:
                    all_draws = load_from_csv()
                    # Filter by year if specified
                    if year:
                        draws = [d for d in all_draws if d.date.year == year]
                    else:
                        draws = all_draws
                    logger.info("loaded_from_csv_fallback", count=len(draws))
                    return draws
                except FileNotFoundError:
                    logger.warning("csv_not_found_creating_sample")
                    create_sample_csv()
                    all_draws = load_from_csv()
                    if year:
                        draws = [d for d in all_draws if d.date.year == year]
                    else:
                        draws = all_draws
                    return draws
                except Exception as csv_error:
                    logger.error("csv_fallback_failed", error=str(csv_error))
                    raise Exception(f"Both API and CSV fallback failed. API: {e}, CSV: {csv_error}")
            raise

    def load_all_historical(self, use_cache: bool = True, use_csv_fallback: bool = True) -> List[Draw]:
        """Load all historical data from 2004 to present

        Args:
            use_cache: Whether to use cached data
            use_csv_fallback: Whether to fall back to CSV if API fails

        Returns:
            List of all historical draws

        Note:
            This is a convenience method that fetches all data.
            First call may take several minutes depending on API speed.
            If API fails and use_csv_fallback is True, will attempt to load from CSV.
        """
        params = {'all_historical': True}

        # Try cache first
        if use_cache:
            cached = self.cache.get_draws(**params)
            if cached:
                logger.info("loaded_all_historical_from_cache", count=len(cached))
                return cached

        # Try API
        try:
            logger.info("loading_all_historical_from_api")
            draws = self.api_client.get_all_historical()

            # Cache results
            if use_cache and draws:
                self.cache.set_draws(draws, **params)

            logger.info("loaded_all_historical", count=len(draws))
            return draws

        except Exception as e:
            logger.warning("api_load_failed", error=str(e))

            if use_csv_fallback:
                logger.info("attempting_csv_fallback")
                from data.csv_fallback import load_from_csv, create_sample_csv

                try:
                    draws = load_from_csv()
                    logger.info("loaded_from_csv_fallback", count=len(draws))
                    print(f"✓ Loaded {len(draws)} draws from CSV fallback")
                    return draws
                except FileNotFoundError:
                    logger.warning("csv_not_found_creating_sample")
                    print("⚠ CSV not found, creating sample data...")
                    create_sample_csv()
                    draws = load_from_csv()
                    logger.info("loaded_from_sample_csv", count=len(draws))
                    print(f"✓ Loaded {len(draws)} draws from sample CSV (MOCK DATA)")
                    return draws
                except Exception as csv_error:
                    logger.error("csv_fallback_failed", error=str(csv_error))
                    raise Exception(f"Both API and CSV fallback failed. API: {e}, CSV: {csv_error}")

            # No fallback, re-raise original error
            raise

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
