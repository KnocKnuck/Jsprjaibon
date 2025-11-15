"""Tests for feature normalizer"""
import pytest
import numpy as np
import pickle
from pathlib import Path
from sklearn.preprocessing import StandardScaler, MinMaxScaler


@pytest.mark.unit
class TestNormalizerBasics:
    """Test basic normalizer functionality"""

    def test_standard_scaler_fit_transform(self, sample_feature_matrix):
        """Test fit_transform with StandardScaler"""
        scaler = StandardScaler()

        scaled = scaler.fit_transform(sample_feature_matrix)

        # Mean should be ~0, std should be ~1
        assert np.allclose(np.mean(scaled, axis=0), 0, atol=1e-10)
        assert np.allclose(np.std(scaled, axis=0), 1, atol=1e-10)
        assert scaled.shape == sample_feature_matrix.shape

    def test_minmax_scaler_fit_transform(self, sample_feature_matrix):
        """Test fit_transform with MinMaxScaler"""
        scaler = MinMaxScaler()

        scaled = scaler.fit_transform(sample_feature_matrix)

        # All values should be in [0, 1]
        assert np.all(scaled >= 0)
        assert np.all(scaled <= 1)
        assert scaled.shape == sample_feature_matrix.shape

    def test_transform_only(self, sample_feature_matrix):
        """Test using transform without fit (should fail)"""
        scaler = StandardScaler()

        # Should raise error if not fitted
        with pytest.raises(Exception):
            scaler.transform(sample_feature_matrix)

    def test_fit_then_transform(self, sample_feature_matrix):
        """Test separate fit and transform calls"""
        scaler = StandardScaler()

        # Fit on training data
        scaler.fit(sample_feature_matrix[:80])

        # Transform test data
        scaled = scaler.transform(sample_feature_matrix[80:])

        assert scaled.shape == (20, sample_feature_matrix.shape[1])


@pytest.mark.unit
class TestNormalizerSaveLoad:
    """Test saving and loading normalizer"""

    def test_save_scaler(self, sample_feature_matrix, temp_dir):
        """Test saving fitted scaler"""
        scaler = StandardScaler()
        scaler.fit(sample_feature_matrix)

        # Save scaler
        scaler_path = temp_dir / "scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

        assert scaler_path.exists()

    def test_load_scaler(self, sample_feature_matrix, temp_dir):
        """Test loading saved scaler"""
        scaler = StandardScaler()
        scaler.fit(sample_feature_matrix)

        # Save
        scaler_path = temp_dir / "scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

        # Load
        with open(scaler_path, 'rb') as f:
            loaded_scaler = pickle.load(f)

        # Should produce same results
        original_scaled = scaler.transform(sample_feature_matrix)
        loaded_scaled = loaded_scaler.transform(sample_feature_matrix)

        assert np.allclose(original_scaled, loaded_scaled)

    def test_save_load_round_trip(self, sample_feature_matrix, temp_dir):
        """Test complete save/load round trip"""
        scaler = MinMaxScaler()
        scaler.fit(sample_feature_matrix)

        # Get transform before save
        scaled_before = scaler.transform(sample_feature_matrix)

        # Save and load
        scaler_path = temp_dir / "scaler.pkl"
        with open(scaler_path, 'wb') as f:
            pickle.dump(scaler, f)

        with open(scaler_path, 'rb') as f:
            loaded_scaler = pickle.load(f)

        # Get transform after load
        scaled_after = loaded_scaler.transform(sample_feature_matrix)

        # Should be identical
        assert np.array_equal(scaled_before, scaled_after)


@pytest.mark.unit
class TestNormalizerEdgeCases:
    """Test edge cases for normalization"""

    def test_single_sample(self):
        """Test normalizing single sample"""
        scaler = StandardScaler()

        # Fit on multiple samples
        train = np.random.rand(100, 10)
        scaler.fit(train)

        # Transform single sample
        single = np.random.rand(1, 10)
        scaled = scaler.transform(single)

        assert scaled.shape == (1, 10)

    def test_zero_variance_feature(self):
        """Test handling of zero variance features"""
        # Create data with constant feature
        data = np.random.rand(100, 10)
        data[:, 5] = 1.0  # Constant feature

        scaler = StandardScaler()

        # Should handle without error
        scaled = scaler.fit_transform(data)

        # Constant feature should become 0
        assert np.allclose(scaled[:, 5], 0)

    def test_all_zeros(self):
        """Test normalizing all-zero column"""
        data = np.random.rand(100, 10)
        data[:, 3] = 0.0  # All zeros

        scaler = StandardScaler()
        scaled = scaler.fit_transform(data)

        # Should handle gracefully
        assert np.allclose(scaled[:, 3], 0)

    def test_negative_values(self):
        """Test normalizing negative values"""
        data = np.random.randn(100, 10)  # Can be negative

        scaler = StandardScaler()
        scaled = scaler.fit_transform(data)

        # Should work fine
        assert scaled.shape == data.shape
        assert np.allclose(np.mean(scaled, axis=0), 0, atol=1e-10)


@pytest.mark.unit
class TestNormalizerConsistency:
    """Test normalizer consistency"""

    def test_fit_transform_vs_fit_then_transform(self, sample_feature_matrix):
        """Test that fit_transform equals fit then transform"""
        scaler1 = StandardScaler()
        scaler2 = StandardScaler()

        # Method 1: fit_transform
        scaled1 = scaler1.fit_transform(sample_feature_matrix)

        # Method 2: fit then transform
        scaler2.fit(sample_feature_matrix)
        scaled2 = scaler2.transform(sample_feature_matrix)

        # Should be identical
        assert np.allclose(scaled1, scaled2)

    def test_multiple_transforms_same_result(self, sample_feature_matrix):
        """Test that multiple transforms give same result"""
        scaler = StandardScaler()
        scaler.fit(sample_feature_matrix)

        # Transform multiple times
        scaled1 = scaler.transform(sample_feature_matrix)
        scaled2 = scaler.transform(sample_feature_matrix)
        scaled3 = scaler.transform(sample_feature_matrix)

        # All should be identical
        assert np.array_equal(scaled1, scaled2)
        assert np.array_equal(scaled2, scaled3)

    def test_scaler_parameters_preserved(self, sample_feature_matrix):
        """Test that scaler parameters are preserved"""
        scaler = StandardScaler()
        scaler.fit(sample_feature_matrix)

        # Get parameters
        mean_before = scaler.mean_.copy()
        scale_before = scaler.scale_.copy()

        # Transform shouldn't change parameters
        scaler.transform(sample_feature_matrix)

        mean_after = scaler.mean_
        scale_after = scaler.scale_

        assert np.array_equal(mean_before, mean_after)
        assert np.array_equal(scale_before, scale_after)


@pytest.mark.unit
class TestInverseTransform:
    """Test inverse transformation"""

    def test_standard_scaler_inverse(self, sample_feature_matrix):
        """Test inverse transform with StandardScaler"""
        scaler = StandardScaler()

        scaled = scaler.fit_transform(sample_feature_matrix)
        reconstructed = scaler.inverse_transform(scaled)

        # Should recover original data
        assert np.allclose(reconstructed, sample_feature_matrix, rtol=1e-5)

    def test_minmax_scaler_inverse(self, sample_feature_matrix):
        """Test inverse transform with MinMaxScaler"""
        scaler = MinMaxScaler()

        scaled = scaler.fit_transform(sample_feature_matrix)
        reconstructed = scaler.inverse_transform(scaled)

        # Should recover original data
        assert np.allclose(reconstructed, sample_feature_matrix, rtol=1e-5)

    def test_round_trip_preserves_data(self, sample_feature_matrix):
        """Test that transform -> inverse_transform preserves data"""
        scaler = StandardScaler()

        # Original data
        original = sample_feature_matrix.copy()

        # Round trip
        scaled = scaler.fit_transform(original)
        recovered = scaler.inverse_transform(scaled)

        # Should be very close to original
        assert np.allclose(original, recovered, rtol=1e-10)


@pytest.mark.integration
class TestNormalizerIntegration:
    """Integration tests for normalizer"""

    def test_normalizer_with_pipeline(self, sample_feature_matrix):
        """Test normalizer in ML pipeline"""
        from sklearn.pipeline import Pipeline
        from sklearn.linear_model import Ridge

        # Create pipeline
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('model', Ridge())
        ])

        # Generate dummy targets
        y = np.random.rand(sample_feature_matrix.shape[0])

        # Fit pipeline
        pipeline.fit(sample_feature_matrix, y)

        # Predict
        predictions = pipeline.predict(sample_feature_matrix)

        assert predictions.shape == y.shape

    def test_normalizer_with_train_test_split(self):
        """Test normalizer with train/test split"""
        from sklearn.model_selection import train_test_split

        # Generate data
        X = np.random.rand(100, 50)
        y = np.random.rand(100)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Fit scaler on training data only
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Shapes should be correct
        assert X_train_scaled.shape == X_train.shape
        assert X_test_scaled.shape == X_test.shape

        # Training data should be normalized
        assert np.allclose(np.mean(X_train_scaled, axis=0), 0, atol=1e-10)


@pytest.mark.unit
class TestCustomNormalizer:
    """Test custom normalizer implementation (if any)"""

    def test_robust_scaling(self):
        """Test robust scaling (less sensitive to outliers)"""
        from sklearn.preprocessing import RobustScaler

        # Create data with outliers
        data = np.random.rand(100, 10)
        data[0, 0] = 1000  # Outlier

        scaler = RobustScaler()
        scaled = scaler.fit_transform(data)

        # Should handle outliers better than StandardScaler
        assert scaled.shape == data.shape

    def test_feature_range_customization(self):
        """Test custom feature range for MinMaxScaler"""
        data = np.random.rand(100, 10)

        # Scale to [-1, 1] instead of [0, 1]
        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaled = scaler.fit_transform(data)

        assert np.all(scaled >= -1)
        assert np.all(scaled <= 1)
        assert np.min(scaled) < 0  # Should have negative values


@pytest.mark.performance
class TestNormalizerPerformance:
    """Test normalizer performance"""

    def test_large_dataset_normalization(self):
        """Test normalization performance on large dataset"""
        import time

        # Large dataset
        large_data = np.random.rand(10000, 250)

        scaler = StandardScaler()

        start = time.time()
        scaler.fit_transform(large_data)
        elapsed = time.time() - start

        # Should be fast (< 1 second)
        assert elapsed < 1.0, f"Normalization too slow: {elapsed}s"

    def test_memory_efficient_normalization(self):
        """Test memory efficiency of normalization"""
        # Create large dataset
        data = np.random.rand(5000, 250)

        scaler = StandardScaler()
        scaled = scaler.fit_transform(data)

        # Memory should not explode (roughly 2x original size)
        original_size = data.nbytes
        scaled_size = scaled.nbytes

        assert scaled_size <= original_size * 1.5
