"""Demo script for Sprint 1 - API Client + Data Foundation

This script demonstrates the core Sprint 1 functionality:
- Configuration loading
- API client with retry logic
- Safe caching layer
- Data validation
- Structured logging

Usage:
    python demo_sprint1.py
"""
from config.settings import Settings
from data.loader import DataLoader
from utils.logger import setup_logging
import structlog

logger = structlog.get_logger()


def main():
    """Run Sprint 1 demo"""

    # Setup logging
    print("=" * 60)
    print("Sprint 1 Demo: API Client + Data Foundation")
    print("=" * 60)
    print()

    setup_logging(log_file="logs/demo.log", level="INFO")
    logger.info("demo_started")

    # Load configuration
    print("1. Loading configuration...")
    try:
        settings = Settings.load_from_yaml("config.yaml")
        logger.info("config_loaded",
                   api_url=str(settings.api.base_url),
                   cache_dir=settings.data.cache_dir)
        print(f"   ✓ API URL: {settings.api.base_url}")
        print(f"   ✓ Cache directory: {settings.data.cache_dir}")
        print(f"   ✓ Rate limit: {settings.api.rate_limit}s between requests")
        print(f"   ✓ Retry attempts: {settings.api.retry_attempts}")
    except FileNotFoundError:
        print("   ✗ config.yaml not found, using defaults")
        settings = Settings()
    print()

    # Initialize data loader
    print("2. Initializing data loader...")
    loader = DataLoader(settings)
    print("   ✓ API client ready")
    print("   ✓ Cache initialized")
    print()

    # Test 1: Get latest draw
    print("3. Fetching latest draw...")
    try:
        latest_draw = loader.get_latest_draw(use_cache=True)
        if latest_draw:
            print(f"   ✓ {latest_draw}")
            print(f"   ✓ Date: {latest_draw.date}")
            print(f"   ✓ Numbers: {latest_draw.numbers}")
            print(f"   ✓ Stars: {latest_draw.stars}")
            print(f"   ✓ Jackpot winner: {'Yes' if latest_draw.has_winner else 'No'}")
        else:
            print("   ✗ No draws found")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        logger.error("latest_draw_failed", error=str(e))
    print()

    # Test 2: Get draws for a specific year
    print("4. Fetching draws from 2024...")
    try:
        draws_2024 = loader.load_draws(year=2024, use_cache=True)
        print(f"   ✓ Retrieved {len(draws_2024)} draws from 2024")

        if draws_2024:
            first_draw = draws_2024[0]
            last_draw = draws_2024[-1]
            print(f"   ✓ First draw: {first_draw.date}")
            print(f"   ✓ Last draw: {last_draw.date}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
        logger.error("year_fetch_failed", year=2024, error=str(e))
    print()

    # Test 3: Cache statistics
    print("5. Cache statistics...")
    try:
        stats = loader.get_cache_stats()
        print(f"   ✓ Cache directory: {stats['cache_dir']}")
        print(f"   ✓ Cached items: {stats['item_count']}")
        print(f"   ✓ Cache size: {stats['size_bytes']:,} bytes")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    print()

    # Test 4: Data validation
    print("6. Testing data validation...")
    from data.models import Draw
    from datetime import date

    try:
        # This should work
        valid_draw = Draw(
            id=1,
            draw_id=1,
            numbers=[5, 12, 23, 34, 45],
            stars=[3, 8],
            date=date(2024, 1, 1),
            has_winner=True
        )
        print(f"   ✓ Valid draw created: {valid_draw}")
    except Exception as e:
        print(f"   ✗ Validation error: {e}")

    try:
        # This should fail (invalid number range)
        invalid_draw = Draw(
            id=2,
            draw_id=2,
            numbers=[5, 12, 23, 34, 99],  # 99 is out of range
            stars=[3, 8],
            date=date(2024, 1, 1),
            has_winner=False
        )
        print("   ✗ Validation failed to catch invalid number!")
    except ValueError as e:
        print(f"   ✓ Correctly rejected invalid data: {e}")
    print()

    print("=" * 60)
    print("Sprint 1 Demo Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  - Check logs/demo.log for detailed logging")
    print("  - Run tests: pytest tests/")
    print("  - Install dependencies: pip install -r requirements.txt")

    logger.info("demo_completed")


if __name__ == "__main__":
    main()
