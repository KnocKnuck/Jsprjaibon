"""Integration tests for the complete system"""
import pytest
import numpy as np
from datetime import date
import responses


@pytest.mark.integration
class TestDataPipeline:
    """Test complete data pipeline"""

    def test_api_to_cache_integration(self, test_settings):
        """Test API client with caching"""
        from data.api_client import EuromillionsAPIClient
        from data.cache import DrawCache

        # Mock API response
        mock_response = [{
            "id": 1,
            "draw_id": 2024001,
            "numbers": [3, 12, 23, 34, 45],
            "stars": [5, 9],
            "date": "2024-01-05",
            "has_winner": True,
            "prizes": []
        }]

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{test_settings.api.base_url}/v1/draws",
                json=mock_response,
                status=200
            )

            # First call - hits API
            with EuromillionsAPIClient(test_settings) as client:
                with DrawCache(test_settings) as cache:
                    # Check cache miss
                    cached = cache.get_draws(year=2024)
                    assert cached is None

                    # Fetch from API
                    draws = client.get_draws(year=2024)
                    assert len(draws) == 1

                    # Store in cache
                    cache.set_draws(draws, year=2024)

                    # Verify cache hit
                    cached = cache.get_draws(year=2024)
                    assert cached is not None
                    assert len(cached) == 1
                    assert cached[0].draw_id == 2024001

    def test_data_validation_pipeline(self, test_settings):
        """Test data validation through the pipeline"""
        from data.models import Draw

        # Valid data should pass
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[3, 12, 23, 34, 45],
            stars=[5, 9],
            date=date(2024, 1, 5),
            has_winner=True,
            prizes=[]
        )

        assert draw.id == 1
        assert len(draw.numbers) == 5
        assert len(draw.stars) == 2

        # Invalid data should fail
        with pytest.raises(Exception):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 99],  # Invalid number
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )


@pytest.mark.integration
class TestFeaturePipeline:
    """Test feature engineering pipeline"""

    def test_draws_to_features(self, sample_draws):
        """Test converting draws to features"""
        # Extract basic features
        all_numbers = [draw.numbers for draw in sample_draws]
        all_stars = [draw.stars for draw in sample_draws]

        # Verify structure
        assert len(all_numbers) == len(sample_draws)
        assert all(len(nums) == 5 for nums in all_numbers)
        assert all(len(stars) == 2 for stars in all_stars)

        # Create frequency features
        flat_numbers = [n for nums in all_numbers for n in nums]
        number_freq = np.bincount(flat_numbers, minlength=51)[1:]

        assert len(number_freq) == 50
        assert sum(number_freq) == len(sample_draws) * 5

    def test_feature_normalization_pipeline(self, sample_feature_matrix):
        """Test feature extraction and normalization"""
        from sklearn.preprocessing import StandardScaler

        # Normalize
        scaler = StandardScaler()
        normalized = scaler.fit_transform(sample_feature_matrix)

        # Verify normalization
        assert normalized.shape == sample_feature_matrix.shape
        assert np.allclose(np.mean(normalized, axis=0), 0, atol=1e-10)
        assert np.allclose(np.std(normalized, axis=0), 1, atol=1e-10)


@pytest.mark.integration
@pytest.mark.model
class TestModelPipeline:
    """Test model training and prediction pipeline"""

    def test_train_predict_pipeline(self, sample_feature_matrix, sample_target_numbers):
        """Test complete train/predict pipeline"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            sample_feature_matrix,
            sample_target_numbers[:, 0],
            test_size=0.2,
            random_state=42
        )

        # Train
        model = RandomForestClassifier(n_estimators=20, random_state=42)
        model.fit(X_train, y_train)

        # Predict
        predictions = model.predict(X_test)

        # Verify
        assert len(predictions) == len(X_test)
        assert all(1 <= p <= 50 for p in predictions)

    def test_multi_output_prediction(self, sample_feature_matrix, sample_target_numbers):
        """Test predicting multiple numbers"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.multioutput import MultiOutputClassifier

        # Create multi-output model
        base_model = RandomForestClassifier(n_estimators=10, random_state=42)
        multi_model = MultiOutputClassifier(base_model)

        # Train on all 5 numbers
        multi_model.fit(sample_feature_matrix, sample_target_numbers)

        # Predict
        predictions = multi_model.predict(sample_feature_matrix[:5])

        # Verify shape
        assert predictions.shape == (5, 5)
        assert all(1 <= p <= 50 for row in predictions for p in row)


@pytest.mark.integration
class TestPredictionPipeline:
    """Test prediction generation pipeline"""

    def test_generate_valid_prediction(self):
        """Test generating valid lottery prediction"""
        import numpy as np

        # Simulate prediction probabilities
        probabilities = np.random.rand(50)
        probabilities /= probabilities.sum()  # Normalize

        # Get top 5 numbers
        top_5_indices = np.argsort(probabilities)[-5:]
        predicted_numbers = top_5_indices + 1  # Convert to 1-50 range

        # Verify
        assert len(predicted_numbers) == 5
        assert len(set(predicted_numbers)) == 5  # All unique
        assert all(1 <= n <= 50 for n in predicted_numbers)

    def test_prediction_with_confidence(self):
        """Test prediction with confidence scores"""
        import numpy as np

        # Simulate predictions
        probabilities = np.random.rand(50)
        probabilities /= probabilities.sum()

        # Get top predictions with confidence
        top_5_indices = np.argsort(probabilities)[-5:]
        top_5_probs = probabilities[top_5_indices]

        confidence = top_5_probs.mean()

        # Verify
        assert 0 <= confidence <= 1
        assert len(top_5_probs) == 5


@pytest.mark.integration
class TestEndToEndPipeline:
    """Test complete end-to-end pipeline"""

    def test_full_pipeline_mock(self, sample_draws):
        """Test complete pipeline with mock data"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import StandardScaler
        import numpy as np

        # 1. Feature engineering (simplified)
        features = []
        targets = []

        for i in range(len(sample_draws) - 1):
            # Use previous draws to predict next
            prev_numbers = sample_draws[i].numbers
            next_numbers = sample_draws[i + 1].numbers

            # Simple features: frequency in last draw
            feat = np.zeros(50)
            for n in prev_numbers:
                feat[n - 1] = 1

            features.append(feat)
            targets.append(next_numbers[0])  # Predict first number

        X = np.array(features)
        y = np.array(targets)

        # 2. Normalize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 3. Train model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_scaled, y)

        # 4. Make prediction
        last_draw_features = np.zeros(50)
        for n in sample_draws[-1].numbers:
            last_draw_features[n - 1] = 1

        last_scaled = scaler.transform([last_draw_features])
        prediction = model.predict(last_scaled)

        # Verify
        assert 1 <= prediction[0] <= 50

    @responses.activate
    def test_api_to_prediction(self, test_settings):
        """Test from API fetch to prediction"""
        from data.api_client import EuromillionsAPIClient
        from data.models import Draw

        # Mock API
        mock_response = [
            {
                "id": i,
                "draw_id": 2024000 + i,
                "numbers": [(i * 3 + j) % 50 + 1 for j in range(5)],
                "stars": [(i % 11) + 1, ((i + 1) % 11) + 1],
                "date": f"2024-01-{(i % 28) + 1:02d}",
                "has_winner": False,
                "prizes": []
            }
            for i in range(10)
        ]

        responses.add(
            responses.GET,
            f"{test_settings.api.base_url}/v1/draws",
            json=mock_response,
            status=200
        )

        # Fetch draws
        with EuromillionsAPIClient(test_settings) as client:
            draws = client.get_draws()

        # Verify we got valid draws
        assert len(draws) == 10
        assert all(isinstance(d, Draw) for d in draws)

        # Extract features (simplified)
        all_numbers = [n for draw in draws for n in draw.numbers]
        number_freq = np.bincount(all_numbers, minlength=51)[1:]

        # Verify features
        assert len(number_freq) == 50
        assert sum(number_freq) == 50  # 10 draws * 5 numbers


@pytest.mark.integration
@pytest.mark.slow
class TestBacktestPipeline:
    """Test backtesting pipeline"""

    def test_simple_backtest(self, historical_draws):
        """Test simple backtesting strategy"""
        from sklearn.ensemble import RandomForestClassifier
        import numpy as np

        # Use first 50% for training, rest for testing
        split = len(historical_draws) // 2
        train_draws = historical_draws[:split]
        test_draws = historical_draws[split:]

        # Extract features and targets from training
        features = []
        targets = []

        for i in range(len(train_draws) - 1):
            # Simple feature: frequency
            feat = np.zeros(50)
            for n in train_draws[i].numbers:
                feat[n - 1] = 1
            features.append(feat)
            targets.append(train_draws[i + 1].numbers[0])

        X = np.array(features)
        y = np.array(targets)

        # Train
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)

        # Test on held-out draws
        correct = 0
        for i in range(len(test_draws) - 1):
            feat = np.zeros(50)
            for n in test_draws[i].numbers:
                feat[n - 1] = 1

            pred = model.predict([feat])[0]
            actual = test_draws[i + 1].numbers

            if pred in actual:
                correct += 1

        # Calculate accuracy
        accuracy = correct / (len(test_draws) - 1)

        # Should have some predictions (even if random-level)
        assert 0 <= accuracy <= 1


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling across pipeline"""

    def test_invalid_api_data_handling(self, test_settings):
        """Test handling of invalid API data"""
        from data.api_client import EuromillionsAPIClient

        invalid_response = [{
            "id": 1,
            "draw_id": 2024001,
            "numbers": [1, 2, 3, 4, 99],  # Invalid
            "stars": [5, 9],
            "date": "2024-01-05",
            "has_winner": True,
            "prizes": []
        }]

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                f"{test_settings.api.base_url}/v1/draws",
                json=invalid_response,
                status=200
            )

            with EuromillionsAPIClient(test_settings) as client:
                # Should raise validation error
                with pytest.raises(ValueError):
                    client.get_draws()

    def test_empty_dataset_handling(self):
        """Test handling of empty datasets"""
        from sklearn.ensemble import RandomForestClassifier

        X = np.array([]).reshape(0, 10)
        y = np.array([])

        model = RandomForestClassifier(n_estimators=5)

        # Should raise error for empty dataset
        with pytest.raises(ValueError):
            model.fit(X, y)
