"""Tests for caching layer"""
import pytest
import time
from datetime import datetime, date
from pathlib import Path

from data.cache import DrawCache
from data.models import Draw


@pytest.mark.unit
class TestCacheInitialization:
    """Test cache initialization"""

    def test_cache_initialization(self, test_settings):
        """Test that cache initializes correctly"""
        cache = DrawCache(test_settings)

        assert cache.cache is not None
        assert cache.ttl_historical == test_settings.data.cache_ttl_historical
        assert cache.ttl_current == test_settings.data.cache_ttl_current
        assert Path(test_settings.data.cache_dir).exists()

    def test_cache_directory_creation(self, test_settings, temp_dir):
        """Test that cache creates directory if it doesn't exist"""
        cache_dir = temp_dir / "new_cache"
        test_settings.data.cache_dir = str(cache_dir)

        cache = DrawCache(test_settings)

        assert cache_dir.exists()

    def test_cache_context_manager(self, test_settings):
        """Test cache works as context manager"""
        with DrawCache(test_settings) as cache:
            assert cache is not None
            assert cache.cache is not None


@pytest.mark.unit
class TestCacheKeyGeneration:
    """Test cache key generation"""

    def test_make_key_consistency(self, test_settings):
        """Test that same params generate same key"""
        cache = DrawCache(test_settings)

        key1 = cache._make_key(year=2024, limit=10)
        key2 = cache._make_key(year=2024, limit=10)

        assert key1 == key2

    def test_make_key_different_params(self, test_settings):
        """Test that different params generate different keys"""
        cache = DrawCache(test_settings)

        key1 = cache._make_key(year=2024, limit=10)
        key2 = cache._make_key(year=2023, limit=10)
        key3 = cache._make_key(year=2024, limit=20)

        assert key1 != key2
        assert key1 != key3
        assert key2 != key3

    def test_make_key_param_order_independence(self, test_settings):
        """Test that parameter order doesn't affect key"""
        cache = DrawCache(test_settings)

        key1 = cache._make_key(year=2024, limit=10)
        key2 = cache._make_key(limit=10, year=2024)

        assert key1 == key2

    def test_make_key_format(self, test_settings):
        """Test that keys have correct format"""
        cache = DrawCache(test_settings)

        key = cache._make_key(year=2024)

        assert key.startswith('draws:')
        assert len(key) > 10  # Should be hash


@pytest.mark.unit
class TestCacheTTL:
    """Test TTL determination logic"""

    def test_ttl_historical_data(self, test_settings):
        """Test that historical data gets 0 TTL (never expire)"""
        cache = DrawCache(test_settings)
        historical_date = datetime(2020, 1, 1)

        ttl = cache._get_ttl(historical_date)

        assert ttl == 0

    def test_ttl_current_year(self, test_settings):
        """Test that current year data gets proper TTL"""
        cache = DrawCache(test_settings)
        current_date = datetime.now()

        ttl = cache._get_ttl(current_date)

        assert ttl == test_settings.data.cache_ttl_current
        assert ttl == 86400  # 24 hours

    def test_ttl_boundary(self, test_settings):
        """Test TTL at year boundary"""
        cache = DrawCache(test_settings)
        current_year = datetime.now().year

        # Last day of previous year
        last_year = datetime(current_year - 1, 12, 31)
        ttl_last_year = cache._get_ttl(last_year)

        # First day of current year
        this_year = datetime(current_year, 1, 1)
        ttl_this_year = cache._get_ttl(this_year)

        assert ttl_last_year == 0  # Historical
        assert ttl_this_year == 86400  # Current


@pytest.mark.unit
class TestCacheOperations:
    """Test cache get/set operations"""

    def test_cache_miss(self, test_settings):
        """Test cache miss returns None"""
        cache = DrawCache(test_settings)

        result = cache.get_draws(year=2024)

        assert result is None

    def test_cache_set_and_get(self, test_settings, sample_draws):
        """Test setting and getting from cache"""
        cache = DrawCache(test_settings)

        # Set cache
        cache.set_draws(sample_draws, year=2024)

        # Get from cache
        cached_draws = cache.get_draws(year=2024)

        assert cached_draws is not None
        assert len(cached_draws) == len(sample_draws)
        assert all(isinstance(draw, Draw) for draw in cached_draws)
        assert cached_draws[0].draw_id == sample_draws[0].draw_id

    def test_cache_set_empty_list(self, test_settings):
        """Test caching empty draw list"""
        cache = DrawCache(test_settings)

        cache.set_draws([], year=2024)
        cached_draws = cache.get_draws(year=2024)

        assert cached_draws is not None
        assert len(cached_draws) == 0

    def test_cache_different_params(self, test_settings, sample_draws):
        """Test that different params create separate cache entries"""
        cache = DrawCache(test_settings)

        # Cache for different years
        cache.set_draws(sample_draws[:5], year=2024)
        cache.set_draws(sample_draws[5:], year=2023)

        # Get separately
        draws_2024 = cache.get_draws(year=2024)
        draws_2023 = cache.get_draws(year=2023)

        assert len(draws_2024) == 5
        assert len(draws_2023) == 5

    def test_cache_overwrite(self, test_settings, sample_draws):
        """Test that setting cache with same params overwrites"""
        cache = DrawCache(test_settings)

        # Set initial cache
        cache.set_draws(sample_draws[:3], year=2024)

        # Overwrite with different data
        cache.set_draws(sample_draws[5:8], year=2024)

        # Should get overwritten data
        cached_draws = cache.get_draws(year=2024)

        assert len(cached_draws) == 3
        assert cached_draws[0].draw_id == sample_draws[5].draw_id


@pytest.mark.unit
class TestCacheTTLExpiration:
    """Test cache expiration behavior"""

    def test_historical_data_no_expiration(self, test_settings):
        """Test that historical data doesn't expire"""
        cache = DrawCache(test_settings)

        # Create draws from 2020 (historical)
        old_draws = [
            Draw(
                id=1,
                draw_id=2020001,
                numbers=[1, 2, 3, 4, 5],
                stars=[1, 2],
                date=date(2020, 1, 1),
                has_winner=False,
                prizes=[]
            )
        ]

        cache.set_draws(old_draws, year=2020)

        # Should still be in cache
        cached = cache.get_draws(year=2020)
        assert cached is not None
        assert len(cached) == 1

    def test_current_data_expiration(self, test_settings):
        """Test that current year data expires"""
        # Set very short TTL for testing
        test_settings.data.cache_ttl_current = 1  # 1 second

        cache = DrawCache(test_settings)

        # Create current year draws
        current_draws = [
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[1, 2, 3, 4, 5],
                stars=[1, 2],
                date=date.today(),
                has_winner=False,
                prizes=[]
            )
        ]

        cache.set_draws(current_draws, year=2024)

        # Should be in cache immediately
        cached = cache.get_draws(year=2024)
        assert cached is not None

        # Wait for expiration
        time.sleep(2)

        # Should be expired
        cached = cache.get_draws(year=2024)
        assert cached is None


@pytest.mark.unit
class TestCacheClear:
    """Test cache clearing"""

    def test_clear_empty_cache(self, test_settings):
        """Test clearing empty cache"""
        cache = DrawCache(test_settings)

        cache.clear()

        # Should work without error
        assert True

    def test_clear_populated_cache(self, test_settings, sample_draws):
        """Test clearing populated cache"""
        cache = DrawCache(test_settings)

        # Populate cache
        cache.set_draws(sample_draws, year=2024)
        cache.set_draws(sample_draws, year=2023)

        # Verify data is cached
        assert cache.get_draws(year=2024) is not None
        assert cache.get_draws(year=2023) is not None

        # Clear cache
        cache.clear()

        # Verify data is gone
        assert cache.get_draws(year=2024) is None
        assert cache.get_draws(year=2023) is None


@pytest.mark.unit
class TestCacheStats:
    """Test cache statistics"""

    def test_stats_empty_cache(self, test_settings):
        """Test stats on empty cache"""
        cache = DrawCache(test_settings)

        stats = cache.get_stats()

        assert 'size_bytes' in stats
        assert 'item_count' in stats
        assert 'cache_dir' in stats
        assert stats['item_count'] == 0

    def test_stats_populated_cache(self, test_settings, sample_draws):
        """Test stats on populated cache"""
        cache = DrawCache(test_settings)

        # Add some data
        cache.set_draws(sample_draws, year=2024)
        cache.set_draws(sample_draws, year=2023)

        stats = cache.get_stats()

        assert stats['item_count'] == 2
        assert stats['size_bytes'] > 0
        assert str(test_settings.data.cache_dir) in stats['cache_dir']


@pytest.mark.unit
class TestCacheErrorHandling:
    """Test cache error handling"""

    def test_corrupted_cache_data(self, test_settings, sample_draws):
        """Test handling of corrupted cache data"""
        cache = DrawCache(test_settings)

        # Set valid data
        cache.set_draws(sample_draws, year=2024)

        # Manually corrupt the cache
        key = cache._make_key(year=2024)
        cache.cache.set(key, [{"invalid": "data"}])

        # Should handle gracefully and return None
        result = cache.get_draws(year=2024)

        assert result is None

    def test_invalid_draw_in_cache(self, test_settings):
        """Test handling of invalid Draw objects in cache"""
        cache = DrawCache(test_settings)

        # Manually insert invalid data
        key = cache._make_key(year=2024)
        invalid_data = [{
            "id": 1,
            "draw_id": 2024001,
            "numbers": [1, 2, 3, 4, 99],  # Invalid number
            "stars": [1, 2],
            "date": "2024-01-01",
            "has_winner": False,
            "prizes": []
        }]
        cache.cache.set(key, invalid_data)

        # Should handle gracefully
        result = cache.get_draws(year=2024)

        assert result is None


@pytest.mark.unit
class TestCacheThreadSafety:
    """Test cache thread safety"""

    def test_concurrent_access(self, test_settings, sample_draws):
        """Test that cache handles concurrent access"""
        import threading

        cache = DrawCache(test_settings)

        def write_cache(year):
            cache.set_draws(sample_draws, year=year)

        def read_cache(year):
            return cache.get_draws(year=year)

        # Create multiple threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=write_cache, args=(2020 + i,))
            threads.append(t)
            t.start()

        # Wait for all to complete
        for t in threads:
            t.join()

        # Verify all data was written
        for i in range(10):
            draws = read_cache(2020 + i)
            assert draws is not None
            assert len(draws) == len(sample_draws)


@pytest.mark.integration
class TestCacheIntegration:
    """Integration tests for cache with real scenarios"""

    def test_cache_full_workflow(self, test_settings, sample_draws):
        """Test complete cache workflow"""
        with DrawCache(test_settings) as cache:
            # Initial cache miss
            assert cache.get_draws(year=2024) is None

            # Store data
            cache.set_draws(sample_draws, year=2024)

            # Cache hit
            cached = cache.get_draws(year=2024)
            assert cached is not None
            assert len(cached) == len(sample_draws)

            # Get stats
            stats = cache.get_stats()
            assert stats['item_count'] == 1

            # Clear
            cache.clear()
            assert cache.get_draws(year=2024) is None
