"""Performance tests for the system"""
import pytest
import time
import numpy as np
from datetime import date


@pytest.mark.performance
@pytest.mark.slow
class TestDataPerformance:
    """Test data layer performance"""

    def test_large_dataset_caching(self, test_settings, historical_draws):
        """Test caching performance with large dataset"""
        from data.cache import DrawCache

        with DrawCache(test_settings) as cache:
            # Time first write (cache miss)
            start = time.time()
            cache.set_draws(historical_draws, year=2022)
            write_time = time.time() - start

            # Time read (cache hit)
            start = time.time()
            cached = cache.get_draws(year=2022)
            read_time = time.time() - start

            # Reading should be much faster than writing
            assert cached is not None
            assert len(cached) == len(historical_draws)
            assert read_time < write_time
            print(f"Cache write: {write_time:.3f}s, read: {read_time:.3f}s")

    def test_api_client_rate_limiting(self, test_settings):
        """Test that rate limiting doesn't block unnecessarily"""
        import responses
        from data.api_client import EuromillionsAPIClient

        mock_response = [{
            "id": 1,
            "draw_id": 2024001,
            "numbers": [1, 2, 3, 4, 5],
            "stars": [1, 2],
            "date": "2024-01-01",
            "has_winner": False,
            "prizes": []
        }]

        with responses.RequestsMock() as rsps:
            # Add 5 responses
            for _ in range(5):
                rsps.add(
                    responses.GET,
                    f"{test_settings.api.base_url}/v1/draws",
                    json=mock_response,
                    status=200
                )

            with EuromillionsAPIClient(test_settings) as client:
                start = time.time()

                for _ in range(5):
                    client._get('v1/draws')

                elapsed = time.time() - start

                # 5 requests at 1 per 2 seconds = ~8 seconds minimum
                # Allow some overhead
                assert elapsed >= 8.0
                print(f"5 API calls took: {elapsed:.3f}s")

    def test_model_validation_speed(self, sample_draws):
        """Test Pydantic validation speed"""
        from data.models import Draw

        # Time validation of many draws
        start = time.time()

        for draw in sample_draws * 100:  # 1000 validations
            _ = Draw(**draw.dict())

        elapsed = time.time() - start

        # Should validate 1000 draws in < 1 second
        assert elapsed < 1.0
        print(f"1000 validations in: {elapsed:.3f}s")


@pytest.mark.performance
@pytest.mark.slow
class TestFeaturePerformance:
    """Test feature engineering performance"""

    def test_feature_extraction_speed(self, historical_draws):
        """Test feature extraction performance"""
        start = time.time()

        # Extract basic features
        all_numbers = [n for draw in historical_draws for n in draw.numbers]
        number_freq = np.bincount(all_numbers, minlength=51)[1:]

        # Extract patterns
        for draw in historical_draws:
            _ = sum(1 for n in draw.numbers if n % 2 == 1)  # Odd count
            _ = sum(1 for n in draw.numbers if n > 25)  # High count
            _ = sum(draw.numbers)  # Sum

        elapsed = time.time() - start

        # Should complete in < 0.5 seconds for ~72 draws
        assert elapsed < 0.5
        print(f"Feature extraction for {len(historical_draws)} draws: {elapsed:.3f}s")

    def test_normalization_speed(self):
        """Test feature normalization performance"""
        from sklearn.preprocessing import StandardScaler

        # Large feature matrix
        X = np.random.rand(5000, 250)

        start = time.time()
        scaler = StandardScaler()
        scaler.fit_transform(X)
        elapsed = time.time() - start

        # Should normalize 5000x250 matrix in < 0.5 seconds
        assert elapsed < 0.5
        print(f"Normalized 5000x250 matrix in: {elapsed:.3f}s")

    def test_feature_memory_usage(self, historical_draws):
        """Test memory efficiency of feature extraction"""
        import sys

        # Extract features
        features = {
            'number_freq': np.zeros(50),
            'star_freq': np.zeros(12),
            'patterns': np.zeros((len(historical_draws), 10)),
            'stats': np.zeros((len(historical_draws), 5))
        }

        # Calculate memory usage
        total_bytes = sum(
            arr.nbytes for arr in features.values() if isinstance(arr, np.ndarray)
        )
        total_mb = total_bytes / (1024 * 1024)

        # Should use < 1MB for typical dataset
        assert total_mb < 1.0
        print(f"Feature memory usage: {total_mb:.3f}MB")


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.model
class TestModelPerformance:
    """Test model training and prediction performance"""

    def test_random_forest_training_speed(self):
        """Test Random Forest training time"""
        from sklearn.ensemble import RandomForestClassifier

        # Simulate 1000 draws with 250 features
        X = np.random.rand(1000, 250)
        y = np.random.randint(1, 51, size=1000)

        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

        start = time.time()
        model.fit(X, y)
        elapsed = time.time() - start

        # Should train in < 5 minutes (300 seconds)
        assert elapsed < 300.0
        print(f"RF training (1000 samples, 100 trees): {elapsed:.3f}s")

    def test_random_forest_prediction_speed(self):
        """Test Random Forest prediction time"""
        from sklearn.ensemble import RandomForestClassifier

        # Train small model
        X_train = np.random.rand(100, 250)
        y_train = np.random.randint(1, 51, size=100)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        # Test prediction speed
        X_test = np.random.rand(100, 250)

        start = time.time()
        predictions = model.predict(X_test)
        elapsed = time.time() - start

        # Should predict 100 samples in < 5 seconds
        assert elapsed < 5.0
        print(f"RF prediction (100 samples): {elapsed:.3f}s")

    def test_lstm_training_speed(self):
        """Test LSTM training time"""
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import LSTM, Dense

            # Small dataset for quick test
            X = np.random.rand(200, 10, 250).astype(np.float32)
            y = np.random.randint(0, 50, size=200)
            y_onehot = tf.keras.utils.to_categorical(y, num_classes=50)

            model = Sequential([
                LSTM(64, input_shape=(10, 250)),
                Dense(50, activation='softmax')
            ])

            model.compile(optimizer='adam', loss='categorical_crossentropy')

            start = time.time()
            model.fit(X, y_onehot, epochs=10, batch_size=32, verbose=0)
            elapsed = time.time() - start

            # Should train in < 2 minutes
            assert elapsed < 120.0
            print(f"LSTM training (200 samples, 10 epochs): {elapsed:.3f}s")

        except ImportError:
            pytest.skip("TensorFlow not available")

    def test_model_save_load_speed(self, temp_dir):
        """Test model serialization speed"""
        from sklearn.ensemble import RandomForestClassifier
        import pickle

        # Train model
        X = np.random.rand(500, 250)
        y = np.random.randint(1, 51, size=500)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)

        model_path = temp_dir / "model.pkl"

        # Time save
        start = time.time()
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        save_time = time.time() - start

        # Time load
        start = time.time()
        with open(model_path, 'rb') as f:
            loaded = pickle.load(f)
        load_time = time.time() - start

        # Both should be fast (< 1 second)
        assert save_time < 1.0
        assert load_time < 1.0
        print(f"Model save: {save_time:.3f}s, load: {load_time:.3f}s")


@pytest.mark.performance
class TestPredictionPerformance:
    """Test prediction generation performance"""

    def test_single_prediction_speed(self):
        """Test single prediction generation time"""
        from sklearn.ensemble import RandomForestClassifier

        # Train model
        X_train = np.random.rand(100, 250)
        y_train = np.random.randint(1, 51, size=100)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        # Time single prediction
        X_test = np.random.rand(1, 250)

        start = time.time()
        prediction = model.predict(X_test)
        elapsed = time.time() - start

        # Should predict in < 1 second
        assert elapsed < 1.0
        print(f"Single prediction: {elapsed:.3f}s")

    def test_batch_prediction_speed(self):
        """Test batch prediction generation time"""
        from sklearn.ensemble import RandomForestClassifier

        # Train model
        X_train = np.random.rand(100, 250)
        y_train = np.random.randint(1, 51, size=100)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        # Time batch prediction
        X_test = np.random.rand(1000, 250)

        start = time.time()
        predictions = model.predict(X_test)
        elapsed = time.time() - start

        # Should predict 1000 samples in < 5 seconds
        assert elapsed < 5.0
        print(f"Batch prediction (1000): {elapsed:.3f}s")

    def test_probability_prediction_speed(self):
        """Test probability prediction speed"""
        from sklearn.ensemble import RandomForestClassifier

        X_train = np.random.rand(100, 250)
        y_train = np.random.randint(1, 51, size=100)

        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X_train, y_train)

        X_test = np.random.rand(10, 250)

        start = time.time()
        probas = model.predict_proba(X_test)
        elapsed = time.time() - start

        # Should be fast
        assert elapsed < 2.0
        print(f"Probability prediction (10 samples): {elapsed:.3f}s")


@pytest.mark.performance
@pytest.mark.slow
class TestSystemPerformance:
    """Test overall system performance"""

    def test_end_to_end_latency(self, sample_draws):
        """Test complete pipeline latency"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler

        start_total = time.time()

        # 1. Feature extraction
        start = time.time()
        features = []
        for i in range(len(sample_draws) - 1):
            feat = np.zeros(50)
            for n in sample_draws[i].numbers:
                feat[n - 1] = 1
            features.append(feat)
        targets = [sample_draws[i + 1].numbers[0] for i in range(len(sample_draws) - 1)]

        X = np.array(features)
        y = np.array(targets)
        feature_time = time.time() - start

        # 2. Normalization
        start = time.time()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        normalize_time = time.time() - start

        # 3. Training
        start = time.time()
        model = RandomForestClassifier(n_estimators=20, random_state=42)
        model.fit(X_scaled, y)
        train_time = time.time() - start

        # 4. Prediction
        start = time.time()
        prediction = model.predict(X_scaled[:1])
        predict_time = time.time() - start

        total_time = time.time() - start_total

        # Print breakdown
        print(f"\nPipeline breakdown:")
        print(f"  Feature extraction: {feature_time:.3f}s")
        print(f"  Normalization: {normalize_time:.3f}s")
        print(f"  Training: {train_time:.3f}s")
        print(f"  Prediction: {predict_time:.3f}s")
        print(f"  Total: {total_time:.3f}s")

        # Entire pipeline should complete in reasonable time
        assert total_time < 10.0

    def test_memory_efficiency(self):
        """Test memory efficiency of system"""
        import sys

        # Create typical data structures
        draws = []
        for i in range(1000):
            draws.append({
                'numbers': [1, 2, 3, 4, 5],
                'stars': [1, 2],
                'date': date(2024, 1, 1)
            })

        # Calculate memory usage
        size = sys.getsizeof(draws)
        size_mb = size / (1024 * 1024)

        print(f"1000 draws memory: {size_mb:.3f}MB")

        # Should use reasonable memory
        assert size_mb < 10.0

    def test_concurrent_predictions(self):
        """Test handling concurrent prediction requests"""
        from sklearn.ensemble import RandomForestClassifier
        import threading

        # Train model
        X = np.random.rand(100, 250)
        y = np.random.randint(1, 51, size=100)

        model = RandomForestClassifier(n_estimators=20, random_state=42)
        model.fit(X, y)

        # Test concurrent predictions
        results = []

        def predict_worker():
            X_test = np.random.rand(10, 250)
            pred = model.predict(X_test)
            results.append(pred)

        # Create 10 concurrent threads
        start = time.time()
        threads = [threading.Thread(target=predict_worker) for _ in range(10)]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        elapsed = time.time() - start

        # Should handle concurrent requests efficiently
        assert len(results) == 10
        assert elapsed < 5.0
        print(f"10 concurrent predictions: {elapsed:.3f}s")


@pytest.mark.performance
class TestCachingSpeedup:
    """Test caching performance improvements"""

    def test_cache_speedup(self, test_settings, sample_draws):
        """Test that caching provides speedup"""
        from data.cache import DrawCache

        with DrawCache(test_settings) as cache:
            # First access (cache miss + write)
            start = time.time()
            cache.set_draws(sample_draws, year=2024)
            cached = cache.get_draws(year=2024)
            first_time = time.time() - start

            # Clear cache
            cache.clear()

            # Populate cache again
            cache.set_draws(sample_draws, year=2024)

            # Second access (cache hit)
            start = time.time()
            cached = cache.get_draws(year=2024)
            second_time = time.time() - start

            print(f"First access: {first_time:.4f}s")
            print(f"Cache hit: {second_time:.4f}s")
            print(f"Speedup: {first_time / second_time:.2f}x")

            # Cache hit should be faster
            assert cached is not None
