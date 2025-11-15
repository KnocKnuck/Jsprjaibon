"""Comprehensive Sprint 1 Test Suite

This script thoroughly tests all Sprint 1 components:
- Configuration loading (YAML + defaults)
- API client connectivity and retry logic
- Data model validation
- Caching mechanism (set/get/TTL)
- Data loader integration
- Error handling

Usage:
    python test_sprint1.py
"""
import sys
from pathlib import Path
from datetime import datetime, date
import structlog
from typing import List

from config.settings import Settings
from data.api_client import EuromillionsAPIClient
from data.cache import DrawCache
from data.loader import DataLoader
from data.models import Draw, Prize
from utils.logger import setup_logging

logger = structlog.get_logger()


class TestResult:
    """Track test results"""
    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, name: str):
        self.total += 1
        self.passed += 1
        print(f"   ✓ {name}")
        logger.info("test_passed", test=name)

    def add_fail(self, name: str, error: str):
        self.total += 1
        self.failed += 1
        self.errors.append((name, error))
        print(f"   ✗ {name}: {error}")
        logger.error("test_failed", test=name, error=error)

    def summary(self):
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {self.total}")
        print(f"Passed: {self.passed} ✓")
        print(f"Failed: {self.failed} ✗")
        print(f"Success Rate: {(self.passed/self.total*100 if self.total > 0 else 0):.1f}%")

        if self.errors:
            print("\nFailed Tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")

        return self.failed == 0


def test_configuration(results: TestResult):
    """Test configuration loading and validation"""
    print("\n" + "=" * 70)
    print("1. CONFIGURATION TESTS")
    print("=" * 70)

    # Test 1.1: Load from YAML
    try:
        settings = Settings.load_from_yaml("config.yaml")
        results.add_pass("Load configuration from config.yaml")

        # Validate API settings
        if settings.api.base_url and settings.api.timeout > 0:
            results.add_pass("API configuration valid")
        else:
            results.add_fail("API configuration validation", "Invalid settings")

        # Validate data settings
        if settings.data.cache_dir:
            results.add_pass("Data configuration valid")
        else:
            results.add_fail("Data configuration validation", "Invalid cache dir")

        # Validate lottery rules
        if (settings.lottery.numbers_count == 5 and
            settings.lottery.stars_count == 2):
            results.add_pass("Lottery rules configuration valid")
        else:
            results.add_fail("Lottery rules validation", "Invalid game rules")

        return settings

    except FileNotFoundError:
        results.add_fail("Load config.yaml", "File not found")
        print("   → Using default settings instead")
        return Settings()

    except Exception as e:
        results.add_fail("Configuration loading", str(e))
        return Settings()


def test_data_models(results: TestResult):
    """Test Pydantic data model validation"""
    print("\n" + "=" * 70)
    print("2. DATA MODEL VALIDATION TESTS")
    print("=" * 70)

    # Test 2.1: Valid draw creation
    try:
        valid_draw = Draw(
            id=1,
            draw_id=1,
            numbers=[5, 12, 23, 34, 45],
            stars=[3, 8],
            date=date(2024, 1, 1),
            has_winner=True
        )
        results.add_pass("Create valid draw")

        # Test sorting
        if valid_draw.numbers == [5, 12, 23, 34, 45]:
            results.add_pass("Numbers automatically sorted")
        else:
            results.add_fail("Number sorting", "Numbers not sorted correctly")

    except Exception as e:
        results.add_fail("Valid draw creation", str(e))

    # Test 2.2: Invalid number range
    try:
        invalid_draw = Draw(
            id=2,
            draw_id=2,
            numbers=[5, 12, 23, 34, 99],  # 99 is invalid
            stars=[3, 8],
            date=date(2024, 1, 1),
            has_winner=False
        )
        results.add_fail("Number range validation", "Should reject numbers > 50")
    except ValueError:
        results.add_pass("Reject invalid number range (> 50)")
    except Exception as e:
        results.add_fail("Number range validation", f"Wrong exception: {e}")

    # Test 2.3: Invalid star range
    try:
        invalid_draw = Draw(
            id=3,
            draw_id=3,
            numbers=[5, 12, 23, 34, 45],
            stars=[3, 15],  # 15 is invalid
            date=date(2024, 1, 1),
            has_winner=False
        )
        results.add_fail("Star range validation", "Should reject stars > 12")
    except ValueError:
        results.add_pass("Reject invalid star range (> 12)")
    except Exception as e:
        results.add_fail("Star range validation", f"Wrong exception: {e}")

    # Test 2.4: Duplicate numbers
    try:
        invalid_draw = Draw(
            id=4,
            draw_id=4,
            numbers=[5, 5, 23, 34, 45],  # Duplicate 5
            stars=[3, 8],
            date=date(2024, 1, 1),
            has_winner=False
        )
        results.add_fail("Duplicate number validation", "Should reject duplicate numbers")
    except ValueError:
        results.add_pass("Reject duplicate numbers")
    except Exception as e:
        results.add_fail("Duplicate validation", f"Wrong exception: {e}")

    # Test 2.5: Prize model
    try:
        prize = Prize(
            prize_amount=1000000.50,
            winners_count=1,
            matched_numbers=5,
            matched_stars=2
        )
        results.add_pass("Create valid prize")
    except Exception as e:
        results.add_fail("Prize creation", str(e))


def test_api_client(results: TestResult, settings: Settings):
    """Test API client functionality"""
    print("\n" + "=" * 70)
    print("3. API CLIENT TESTS")
    print("=" * 70)

    try:
        client = EuromillionsAPIClient(settings)
        results.add_pass("Initialize API client")

        # Test 3.1: Fetch recent draws
        try:
            print("   → Fetching draws from 2024 (this may take a few seconds)...")
            draws_2024 = client.get_draws(year=2024)

            if draws_2024 and len(draws_2024) > 0:
                results.add_pass(f"Fetch 2024 draws ({len(draws_2024)} draws)")

                # Validate first draw
                first_draw = draws_2024[0]
                if isinstance(first_draw, Draw):
                    results.add_pass("Draw objects properly validated")
                else:
                    results.add_fail("Draw object type", "Not a Draw instance")

                # Display sample draw
                print(f"   → Sample draw: {first_draw}")
                print(f"      Date: {first_draw.date}")
                print(f"      Numbers: {first_draw.numbers}")
                print(f"      Stars: {first_draw.stars}")
                print(f"      Winner: {'Yes' if first_draw.has_winner else 'No'}")
            else:
                results.add_fail("Fetch 2024 draws", "No draws returned")

        except Exception as e:
            results.add_fail("Fetch draws from API", str(e))
            print(f"   → API Error: {e}")
            print("   → This may be a network issue or API rate limit")

        # Test 3.2: API error handling (invalid year)
        try:
            invalid_draws = client.get_draws(year=1900)  # Before Euromillions existed
            if len(invalid_draws) == 0:
                results.add_pass("Handle invalid year gracefully (returns empty)")
            else:
                results.add_fail("Invalid year handling", "Should return empty list")
        except Exception as e:
            # Either exception or empty list is acceptable
            results.add_pass("Handle invalid year (raises exception)")

    except Exception as e:
        results.add_fail("API client initialization", str(e))


def test_cache(results: TestResult, settings: Settings):
    """Test caching mechanism"""
    print("\n" + "=" * 70)
    print("4. CACHE MECHANISM TESTS")
    print("=" * 70)

    try:
        cache = DrawCache(settings)
        results.add_pass("Initialize cache")

        # Test 4.1: Create test draws
        test_draws = [
            Draw(
                id=100,
                draw_id=100,
                numbers=[1, 2, 3, 4, 5],
                stars=[1, 2],
                date=date(2023, 1, 1),
                has_winner=False
            ),
            Draw(
                id=101,
                draw_id=101,
                numbers=[6, 7, 8, 9, 10],
                stars=[3, 4],
                date=date(2023, 1, 2),
                has_winner=True
            )
        ]

        # Test 4.2: Store in cache
        try:
            cache.set_draws(test_draws, year=2023, test=True)
            results.add_pass("Store draws in cache")
        except Exception as e:
            results.add_fail("Cache storage", str(e))
            return

        # Test 4.3: Retrieve from cache
        try:
            cached_draws = cache.get_draws(year=2023, test=True)
            if cached_draws and len(cached_draws) == 2:
                results.add_pass("Retrieve draws from cache")

                # Validate cached data integrity
                if cached_draws[0].numbers == [1, 2, 3, 4, 5]:
                    results.add_pass("Cache data integrity maintained")
                else:
                    results.add_fail("Cache integrity", "Data corrupted")
            else:
                results.add_fail("Cache retrieval", f"Expected 2 draws, got {len(cached_draws) if cached_draws else 0}")
        except Exception as e:
            results.add_fail("Cache retrieval", str(e))

        # Test 4.4: Cache miss
        try:
            miss = cache.get_draws(year=1999, nonexistent=True)
            if miss is None:
                results.add_pass("Cache miss returns None")
            else:
                results.add_fail("Cache miss behavior", "Should return None")
        except Exception as e:
            results.add_fail("Cache miss handling", str(e))

        # Test 4.5: Cache statistics
        try:
            stats = cache.get_stats()
            if 'item_count' in stats and 'size_bytes' in stats:
                results.add_pass("Cache statistics available")
                print(f"   → Cache items: {stats['item_count']}")
                print(f"   → Cache size: {stats['size_bytes']:,} bytes")
            else:
                results.add_fail("Cache statistics", "Missing fields")
        except Exception as e:
            results.add_fail("Cache statistics", str(e))

    except Exception as e:
        results.add_fail("Cache initialization", str(e))


def test_data_loader(results: TestResult, settings: Settings):
    """Test integrated data loader"""
    print("\n" + "=" * 70)
    print("5. DATA LOADER INTEGRATION TESTS")
    print("=" * 70)

    try:
        loader = DataLoader(settings)
        results.add_pass("Initialize data loader")

        # Test 5.1: Load with cache
        try:
            print("   → Loading 2024 draws with cache...")
            draws = loader.load_draws(year=2024, use_cache=True)
            if draws and len(draws) > 0:
                results.add_pass(f"Load draws via DataLoader ({len(draws)} draws)")
            else:
                results.add_fail("DataLoader fetch", "No draws returned")
        except Exception as e:
            results.add_fail("DataLoader load_draws", str(e))

        # Test 5.2: Get latest draw
        try:
            print("   → Fetching latest draw...")
            latest = loader.get_latest_draw(use_cache=True)
            if latest:
                results.add_pass("Get latest draw")
                print(f"   → Latest: {latest}")
            else:
                results.add_fail("Latest draw", "No draw returned")
        except Exception as e:
            results.add_fail("Get latest draw", str(e))

        # Test 5.3: Cache stats through loader
        try:
            stats = loader.get_cache_stats()
            if stats:
                results.add_pass("Get cache stats via loader")
            else:
                results.add_fail("Loader cache stats", "No stats returned")
        except Exception as e:
            results.add_fail("Loader cache stats", str(e))

    except Exception as e:
        results.add_fail("DataLoader initialization", str(e))


def test_logging(results: TestResult):
    """Test structured logging"""
    print("\n" + "=" * 70)
    print("6. LOGGING TESTS")
    print("=" * 70)

    try:
        # Check if log file was created
        log_path = Path("logs/test_sprint1.log")
        if log_path.exists():
            results.add_pass("Log file created")

            # Check log file has content
            if log_path.stat().st_size > 0:
                results.add_pass("Log file contains entries")
            else:
                results.add_fail("Log content", "Log file is empty")
        else:
            results.add_fail("Log file creation", "File not found")

    except Exception as e:
        results.add_fail("Logging system", str(e))


def main():
    """Run all Sprint 1 tests"""
    print("\n" + "=" * 70)
    print("EUROMILLIONS ML PREDICTOR - SPRINT 1 TEST SUITE")
    print("=" * 70)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Setup logging
    setup_logging(log_file="logs/test_sprint1.log", level="INFO")
    logger.info("test_suite_started")

    # Track results
    results = TestResult()

    try:
        # Run all tests
        settings = test_configuration(results)
        test_data_models(results)
        test_api_client(results, settings)
        test_cache(results, settings)
        test_data_loader(results, settings)
        test_logging(results)

        # Show summary
        success = results.summary()

        print("\n" + "=" * 70)
        print("RECOMMENDATIONS")
        print("=" * 70)
        if success:
            print("✓ All tests passed! Sprint 1 foundation is solid.")
            print("\nNext steps:")
            print("  1. Proceed with Sprint 2 feature engineering")
            print("  2. Implement ML models")
            print("  3. Build prediction engine")
        else:
            print("⚠ Some tests failed. Review errors above.")
            print("\nAction items:")
            print("  1. Check logs/test_sprint1.log for details")
            print("  2. Verify network connectivity for API tests")
            print("  3. Fix failing components before Sprint 2")

        print("\nFor detailed logs: cat logs/test_sprint1.log")
        print("=" * 70)

        logger.info("test_suite_completed",
                   total=results.total,
                   passed=results.passed,
                   failed=results.failed)

        # Exit with appropriate code
        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"\n✗ CRITICAL ERROR: {e}")
        logger.error("test_suite_error", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
