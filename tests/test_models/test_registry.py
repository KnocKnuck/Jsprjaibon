"""
Unit tests for Model Registry implementation.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
import json

from euromillions_ml.models.registry import ModelRegistry


class TestModelRegistry:
    """Test cases for Model Registry."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    @pytest.fixture
    def registry(self, temp_dir):
        """Create a test registry."""
        return ModelRegistry(registry_dir=temp_dir)

    @pytest.fixture
    def sample_metadata(self):
        """Sample model metadata."""
        return {
            'n_estimators': 200,
            'max_depth': 15,
            'n_samples': 1000,
            'n_features': 50
        }

    @pytest.fixture
    def sample_metrics(self):
        """Sample model metrics."""
        return {
            'accuracy': 0.85,
            'precision': 0.82,
            'recall': 0.88
        }

    def test_registry_initialization(self, temp_dir):
        """Test registry initialization."""
        registry = ModelRegistry(registry_dir=temp_dir)

        assert registry.registry_dir == Path(temp_dir)
        assert registry.registry_file.exists()
        assert 'models' in registry.registry

    def test_register_model(self, registry, sample_metadata):
        """Test registering a model."""
        registry.register_model(
            model_name='RandomForest',
            version='v1.0',
            metadata=sample_metadata,
            model_path='/path/to/model.pkl'
        )

        assert len(registry.registry['models']) == 1
        model_entry = registry.registry['models'][0]

        assert model_entry['name'] == 'RandomForest'
        assert model_entry['version'] == 'v1.0'
        assert model_entry['metadata'] == sample_metadata
        assert model_entry['active'] is True
        assert 'registered_at' in model_entry

    def test_register_multiple_models(self, registry, sample_metadata):
        """Test registering multiple models."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('LSTM', 'v1.0', sample_metadata, '/path2')
        registry.register_model('RandomForest', 'v1.1', sample_metadata, '/path3')

        assert len(registry.registry['models']) == 3

    def test_get_latest_model(self, registry, sample_metadata):
        """Test getting the latest version of a model."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('RandomForest', 'v1.1', sample_metadata, '/path2')
        registry.register_model('RandomForest', 'v1.2', sample_metadata, '/path3')

        latest = registry.get_latest('RandomForest')

        assert latest is not None
        assert latest['version'] == 'v1.2'

    def test_get_latest_nonexistent(self, registry):
        """Test getting latest of nonexistent model."""
        latest = registry.get_latest('NonexistentModel')

        assert latest is None

    def test_get_specific_version(self, registry, sample_metadata):
        """Test getting a specific model version."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('RandomForest', 'v1.1', sample_metadata, '/path2')

        model = registry.get_version('RandomForest', 'v1.0')

        assert model is not None
        assert model['version'] == 'v1.0'

    def test_list_models(self, registry, sample_metadata):
        """Test listing all models."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('LSTM', 'v1.0', sample_metadata, '/path2')

        models = registry.list_models()

        assert len(models) == 2

    def test_list_versions(self, registry, sample_metadata):
        """Test listing all versions of a model."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('RandomForest', 'v1.1', sample_metadata, '/path2')
        registry.register_model('LSTM', 'v1.0', sample_metadata, '/path3')

        versions = registry.list_versions('RandomForest')

        assert len(versions) == 2
        assert all(v['name'] == 'RandomForest' for v in versions)

    def test_deactivate_model(self, registry, sample_metadata):
        """Test deactivating a model."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        registry.deactivate_model('RandomForest', 'v1.0')

        model = registry.get_version('RandomForest', 'v1.0')
        assert model['active'] is False

        # Should not appear in get_latest
        latest = registry.get_latest('RandomForest')
        assert latest is None

    def test_archive_model(self, registry, sample_metadata):
        """Test archiving a model."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        registry.archive_model('RandomForest', 'v1.0')

        model = registry.get_version('RandomForest', 'v1.0')
        assert model['archived'] is True
        assert model['active'] is False
        assert 'archived_at' in model

    def test_delete_model(self, registry, sample_metadata):
        """Test deleting a model from registry."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        registry.delete_model('RandomForest', 'v1.0')

        assert len(registry.registry['models']) == 0

    def test_update_metrics(self, registry, sample_metadata, sample_metrics):
        """Test updating model metrics."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        registry.update_metrics('RandomForest', 'v1.0', sample_metrics)

        model = registry.get_version('RandomForest', 'v1.0')
        assert model['metrics'] == sample_metrics
        assert 'metrics_updated_at' in model

    def test_add_tags(self, registry, sample_metadata):
        """Test adding tags to a model."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        registry.add_tags('RandomForest', 'v1.0', ['production', 'best'])

        model = registry.get_version('RandomForest', 'v1.0')
        assert 'production' in model['tags']
        assert 'best' in model['tags']

    def test_find_by_tag(self, registry, sample_metadata):
        """Test finding models by tag."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1', tags=['production'])
        registry.register_model('LSTM', 'v1.0', sample_metadata, '/path2', tags=['experimental'])
        registry.register_model('RandomForest', 'v1.1', sample_metadata, '/path3', tags=['production'])

        production_models = registry.find_by_tag('production')

        assert len(production_models) == 2
        assert all(m['name'] == 'RandomForest' for m in production_models)

    def test_get_best_model(self, registry, sample_metadata):
        """Test getting best model by metric."""
        registry.register_model(
            'RandomForest', 'v1.0', sample_metadata, '/path1',
            metrics={'accuracy': 0.85}
        )
        registry.register_model(
            'RandomForest', 'v1.1', sample_metadata, '/path2',
            metrics={'accuracy': 0.90}
        )
        registry.register_model(
            'RandomForest', 'v1.2', sample_metadata, '/path3',
            metrics={'accuracy': 0.88}
        )

        best = registry.get_best_model('RandomForest', 'accuracy', higher_is_better=True)

        assert best is not None
        assert best['version'] == 'v1.1'
        assert best['metrics']['accuracy'] == 0.90

    def test_get_summary(self, registry, sample_metadata):
        """Test getting registry summary."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')
        registry.register_model('LSTM', 'v1.0', sample_metadata, '/path2')

        summary = registry.get_summary()

        assert summary['total_models'] == 2
        assert summary['active_models'] == 2
        assert 'RandomForest' in summary['model_types']
        assert 'LSTM' in summary['model_types']

    def test_export_registry(self, registry, sample_metadata, temp_dir):
        """Test exporting registry."""
        registry.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        export_path = Path(temp_dir) / 'exported_registry.json'
        registry.export_registry(str(export_path))

        assert export_path.exists()

        with open(export_path, 'r') as f:
            exported = json.load(f)

        assert len(exported['models']) == 1

    def test_persistence(self, temp_dir, sample_metadata):
        """Test that registry persists across instances."""
        # Create registry and add model
        registry1 = ModelRegistry(registry_dir=temp_dir)
        registry1.register_model('RandomForest', 'v1.0', sample_metadata, '/path1')

        # Create new registry instance
        registry2 = ModelRegistry(registry_dir=temp_dir)

        assert len(registry2.registry['models']) == 1
        model = registry2.get_version('RandomForest', 'v1.0')
        assert model is not None
