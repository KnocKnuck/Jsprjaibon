#!/usr/bin/env python3
"""System validation script - runs all checks"""
import sys
from pathlib import Path


def check_dependencies():
    """Check all dependencies installed"""
    required = {
        'pydantic': 'pydantic',
        'tenacity': 'tenacity',
        'diskcache': 'diskcache',
        'typer': 'typer',
        'structlog': 'structlog',
        'sklearn': 'scikit-learn',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'requests': 'requests',
        'yaml': 'PyYAML',
        'ratelimit': 'ratelimit',
        'responses': 'responses (dev)',
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"  ✗ {package} - MISSING")

    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print("  pip install -r requirements.txt")
        print("  pip install -r requirements-dev.txt")
        return False

    print("\n✓ All dependencies installed")
    return True


def check_structure():
    """Check project structure"""
    required_dirs = [
        'data',
        'config',
        'utils',
        'tests',
        'tests/test_data',
        'tests/test_features',
        'tests/test_models',
        'tests/test_prediction',
        'euromillions_ml',
        'euromillions_ml/data',
        'euromillions_ml/features',
        'euromillions_ml/models',
        'euromillions_ml/prediction',
    ]

    missing_dirs = []
    for dir_path in required_dirs:
        full_path = Path(dir_path)
        if not full_path.exists():
            missing_dirs.append(dir_path)
            print(f"  ✗ {dir_path} - MISSING")
        else:
            print(f"  ✓ {dir_path}")

    if missing_dirs:
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        return False

    print("\n✓ Project structure valid")
    return True


def check_config():
    """Check configuration files"""
    required_files = [
        'config.yaml',
        'requirements.txt',
        'requirements-dev.txt',
        'pytest.ini',
        'README.md',
    ]

    missing_files = []
    for file_path in required_files:
        full_path = Path(file_path)
        if not full_path.exists():
            missing_files.append(file_path)
            print(f"  ✗ {file_path} - MISSING")
        else:
            print(f"  ✓ {file_path}")

    if missing_files:
        print(f"\n❌ Missing config files: {', '.join(missing_files)}")
        return False

    print("\n✓ Configuration files present")
    return True


def check_core_modules():
    """Check that core modules can be imported"""
    modules = [
        ('config.settings', 'Settings'),
        ('data.models', 'Draw'),
        ('data.api_client', 'EuromillionsAPIClient'),
        ('data.cache', 'DrawCache'),
    ]

    failed_imports = []
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"  ✓ {module_name}.{class_name}")
        except Exception as e:
            failed_imports.append(f"{module_name}.{class_name}: {e}")
            print(f"  ✗ {module_name}.{class_name} - ERROR: {e}")

    if failed_imports:
        print(f"\n❌ Failed to import core modules")
        return False

    print("\n✓ Core modules importable")
    return True


def run_quick_tests():
    """Run quick smoke tests"""
    try:
        # Test 1: Configuration loads
        print("\n  Testing configuration loading...")
        from config.settings import Settings

        settings = Settings.load_from_yaml('config.yaml')
        print(f"  ✓ Configuration loads successfully")
        print(f"    - API URL: {settings.api.base_url}")
        print(f"    - Cache dir: {settings.data.cache_dir}")

        # Test 2: API client initializes
        print("\n  Testing API client initialization...")
        from data.api_client import EuromillionsAPIClient

        client = EuromillionsAPIClient(settings)
        print(f"  ✓ API client initializes")
        print(f"    - Base URL: {client.base_url}")
        print(f"    - Timeout: {client.timeout}s")

        # Test 3: Cache initializes
        print("\n  Testing cache initialization...")
        from data.cache import DrawCache

        cache = DrawCache(settings)
        stats = cache.get_stats()
        print(f"  ✓ Cache initializes")
        print(f"    - Cache dir: {stats['cache_dir']}")
        print(f"    - Items: {stats['item_count']}")
        cache.cache.close()

        # Test 4: Model validation works
        print("\n  Testing data models...")
        from data.models import Draw
        from datetime import date

        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[1, 2, 3, 4, 5],
            stars=[1, 2],
            date=date(2024, 1, 1),
            has_winner=False,
            prizes=[]
        )
        print(f"  ✓ Data models validate correctly")
        print(f"    - Sample draw: {draw}")

        print("\n✓ Quick tests passed")
        return True

    except Exception as e:
        print(f"\n❌ Quick tests failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_test_files():
    """Check that test files exist"""
    required_tests = [
        'tests/conftest.py',
        'tests/test_data/test_api_client.py',
        'tests/test_data/test_cache.py',
        'tests/test_data/test_models.py',
        'tests/test_features/test_engineering.py',
        'tests/test_features/test_normalizer.py',
        'tests/test_models/test_random_forest.py',
        'tests/test_models/test_lstm.py',
        'tests/test_models/test_registry.py',
        'tests/test_prediction/test_predictor.py',
        'tests/test_prediction/test_backtest.py',
        'tests/test_integration.py',
        'tests/test_performance.py',
    ]

    missing_tests = []
    for test_file in required_tests:
        if not Path(test_file).exists():
            missing_tests.append(test_file)
            print(f"  ✗ {test_file} - MISSING")
        else:
            print(f"  ✓ {test_file}")

    if missing_tests:
        print(f"\n❌ Missing test files: {len(missing_tests)}")
        return False

    print(f"\n✓ All {len(required_tests)} test files present")
    return True


def run_pytest_dry_run():
    """Run pytest in dry-run mode to check test discovery"""
    import subprocess

    print("\n  Running pytest --collect-only...")
    try:
        result = subprocess.run(
            ['pytest', '--collect-only', '-q'],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout
        if result.returncode == 0:
            # Count tests
            import re
            match = re.search(r'(\d+) tests? collected', output)
            if match:
                test_count = int(match.group(1))
                print(f"  ✓ Pytest can discover {test_count} tests")
                return True
            else:
                print(f"  ✓ Pytest collection successful")
                return True
        else:
            print(f"  ✗ Pytest collection failed")
            print(f"    Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"  ⚠ Pytest collection timed out")
        return False
    except FileNotFoundError:
        print(f"  ⚠ Pytest not found in PATH")
        return False
    except Exception as e:
        print(f"  ✗ Error running pytest: {e}")
        return False


def main():
    """Run all validation checks"""
    print("=" * 70)
    print("EUROMILLIONS ML PREDICTOR - SYSTEM VALIDATION")
    print("=" * 70)

    checks = []

    # 1. Dependencies
    print("\n[1/7] Checking dependencies...")
    print("-" * 70)
    checks.append(check_dependencies())

    # 2. Project structure
    print("\n[2/7] Checking project structure...")
    print("-" * 70)
    checks.append(check_structure())

    # 3. Configuration files
    print("\n[3/7] Checking configuration files...")
    print("-" * 70)
    checks.append(check_config())

    # 4. Core modules
    print("\n[4/7] Checking core modules...")
    print("-" * 70)
    checks.append(check_core_modules())

    # 5. Quick tests
    print("\n[5/7] Running quick tests...")
    print("-" * 70)
    checks.append(run_quick_tests())

    # 6. Test files
    print("\n[6/7] Checking test files...")
    print("-" * 70)
    checks.append(check_test_files())

    # 7. Pytest discovery
    print("\n[7/7] Checking pytest test discovery...")
    print("-" * 70)
    checks.append(run_pytest_dry_run())

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    passed = sum(checks)
    total = len(checks)

    if all(checks):
        print(f"\n✓ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🎉 System is ready for testing!")
        print("\nNext steps:")
        print("  1. Run tests:           pytest")
        print("  2. Run with coverage:   pytest --cov=euromillions_ml")
        print("  3. Run integration:     pytest -m integration")
        print("  4. Run performance:     pytest -m performance")
        return 0
    else:
        print(f"\n❌ SOME CHECKS FAILED ({passed}/{total})")
        print("\n⚠ Please fix the issues above before running tests")
        return 1


if __name__ == "__main__":
    sys.exit(main())
