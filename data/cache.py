"""Safe caching layer using diskcache"""
from diskcache import Cache
from typing import Optional, List
import hashlib
import json
from datetime import datetime
from pathlib import Path
import structlog

from ..config.settings import Settings
from .models import Draw

logger = structlog.get_logger()


class DrawCache:
    """Safe caching for API draws using diskcache

    Features:
    - Secure disk-based caching (no pickle vulnerabilities)
    - TTL-based expiration (historical data never expires)
    - Automatic cache key generation
    - Thread-safe operations
    """

    def __init__(self, settings: Settings):
        """Initialize cache

        Args:
            settings: Application settings with cache configuration
        """
        cache_path = Path(settings.data.cache_dir)
        cache_path.mkdir(parents=True, exist_ok=True)

        self.cache = Cache(str(cache_path))
        self.ttl_historical = settings.data.cache_ttl_historical
        self.ttl_current = settings.data.cache_ttl_current

        logger.info("cache_initialized",
                   path=str(cache_path),
                   ttl_historical=self.ttl_historical,
                   ttl_current=self.ttl_current)

    def _make_key(self, **kwargs) -> str:
        """Generate cache key from parameters

        Args:
            **kwargs: Parameters to hash into cache key

        Returns:
            MD5 hash of sorted parameters
        """
        # Sort keys for consistent hashing
        key_str = json.dumps(kwargs, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_str.encode()).hexdigest()
        return f"draws:{key_hash}"

    def _get_ttl(self, draw_date: datetime) -> int:
        """Determine TTL based on draw date

        Args:
            draw_date: Date of the draw

        Returns:
            TTL in seconds (0 for historical data, 24h for current year)
        """
        current_year = datetime.now().year
        if draw_date.year < current_year:
            return self.ttl_historical  # Never expire (0)
        return self.ttl_current  # 24 hours

    def get_draws(self, **params) -> Optional[List[Draw]]:
        """Get draws from cache

        Args:
            **params: Parameters used to fetch draws (year, dates, etc.)

        Returns:
            List of cached Draw objects, or None if cache miss
        """
        key = self._make_key(**params)
        cached = self.cache.get(key)

        if cached is not None:
            logger.info("cache_hit", key=key, count=len(cached))
            try:
                # Reconstruct Draw objects from cached dicts
                return [Draw(**d) for d in cached]
            except Exception as e:
                logger.error("cache_deserialize_error", key=key, error=str(e))
                # Remove corrupted cache entry
                self.cache.delete(key)
                return None

        logger.info("cache_miss", key=key)
        return None

    def set_draws(self, draws: List[Draw], **params):
        """Store draws in cache

        Args:
            draws: List of Draw objects to cache
            **params: Parameters used to fetch these draws
        """
        key = self._make_key(**params)

        # Determine TTL from newest draw
        if draws:
            newest_date = max(draw.date for draw in draws)
            ttl = self._get_ttl(datetime.combine(newest_date, datetime.min.time()))
        else:
            ttl = self.ttl_current

        # Store as dicts (safer than pickle)
        try:
            draw_dicts = [d.dict() for d in draws]
            if ttl == 0:
                # Store without expiration
                self.cache.set(key, draw_dicts, expire=None)
            else:
                self.cache.set(key, draw_dicts, expire=ttl)

            logger.info("cache_set",
                       key=key,
                       count=len(draws),
                       ttl=ttl if ttl > 0 else "never")
        except Exception as e:
            logger.error("cache_serialize_error", key=key, error=str(e))
            raise

    def clear(self):
        """Clear all cached data"""
        count = len(self.cache)
        self.cache.clear()
        logger.info("cache_cleared", items_removed=count)

    def get_stats(self) -> dict:
        """Get cache statistics

        Returns:
            Dictionary with cache size, count, and hit/miss ratios
        """
        return {
            'size_bytes': self.cache.volume(),
            'item_count': len(self.cache),
            'cache_dir': str(self.cache.directory)
        }

    def __enter__(self):
        """Context manager support"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up on exit"""
        self.cache.close()
