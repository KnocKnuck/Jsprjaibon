"""
Model Registry for version control and tracking of trained models.

This module provides a centralized system for registering, versioning,
and managing trained models with their metadata and performance metrics.
"""

from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import json
import shutil


class ModelRegistry:
    """
    Version control and tracking system for trained models.

    Maintains a registry of all trained models with their versions,
    metadata, performance metrics, and storage locations.

    Attributes:
        registry_dir (Path): Directory where models and registry are stored
        registry_file (Path): Path to the registry JSON file
        registry (Dict): In-memory registry data
    """

    def __init__(self, registry_dir: str = "./models"):
        """
        Initialize the model registry.

        Args:
            registry_dir: Directory to store models and registry file
        """
        self.registry_dir = Path(registry_dir)
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.registry_dir / "registry.json"
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """
        Load registry from disk or create new one.

        Returns:
            Registry dictionary with 'models' list
        """
        if self.registry_file.exists():
            try:
                with open(self.registry_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Corrupt registry file. Creating new registry.")
                return {'models': []}
        return {'models': []}

    def _save_registry(self):
        """Save registry to disk."""
        with open(self.registry_file, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def register_model(
        self,
        model_name: str,
        version: str,
        metadata: Dict,
        model_path: str,
        metrics: Optional[Dict] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Register a trained model in the registry.

        Args:
            model_name: Name of the model (e.g., 'RandomForest', 'LSTM')
            version: Version string (e.g., 'v1.0', '2024-01-15')
            metadata: Model metadata (hyperparameters, training info, etc.)
            model_path: Path where the model is saved
            metrics: Optional performance metrics
            tags: Optional list of tags for categorization
        """
        entry = {
            'name': model_name,
            'version': version,
            'path': model_path,
            'metadata': metadata,
            'metrics': metrics or {},
            'tags': tags or [],
            'registered_at': datetime.now().isoformat(),
            'active': True,
            'archived': False
        }

        self.registry['models'].append(entry)
        self._save_registry()
        print(f"✓ Registered {model_name} v{version}")
        print(f"  Path: {model_path}")
        if metrics:
            print(f"  Metrics: {metrics}")

    def get_latest(self, model_name: str) -> Optional[Dict]:
        """
        Get the latest active version of a model.

        Args:
            model_name: Name of the model to retrieve

        Returns:
            Model entry dictionary or None if not found
        """
        models = [
            m for m in self.registry['models']
            if m['name'] == model_name and m['active'] and not m.get('archived', False)
        ]
        if not models:
            return None
        return sorted(models, key=lambda x: x['registered_at'])[-1]

    def get_version(self, model_name: str, version: str) -> Optional[Dict]:
        """
        Get a specific version of a model.

        Args:
            model_name: Name of the model
            version: Version string

        Returns:
            Model entry dictionary or None if not found
        """
        for model in self.registry['models']:
            if model['name'] == model_name and model['version'] == version:
                return model
        return None

    def list_models(self, active_only: bool = True) -> List[Dict]:
        """
        List all registered models.

        Args:
            active_only: If True, only return active models

        Returns:
            List of model entry dictionaries
        """
        if active_only:
            return [m for m in self.registry['models'] if m['active']]
        return self.registry['models']

    def list_versions(self, model_name: str) -> List[Dict]:
        """
        List all versions of a specific model.

        Args:
            model_name: Name of the model

        Returns:
            List of model entries sorted by registration date
        """
        versions = [m for m in self.registry['models'] if m['name'] == model_name]
        return sorted(versions, key=lambda x: x['registered_at'])

    def deactivate_model(self, model_name: str, version: str):
        """
        Deactivate a specific model version.

        Args:
            model_name: Name of the model
            version: Version to deactivate
        """
        for model in self.registry['models']:
            if model['name'] == model_name and model['version'] == version:
                model['active'] = False
                self._save_registry()
                print(f"✓ Deactivated {model_name} v{version}")
                return
        print(f"Model {model_name} v{version} not found")

    def archive_model(self, model_name: str, version: str):
        """
        Archive a model version (mark as archived, keep in registry).

        Args:
            model_name: Name of the model
            version: Version to archive
        """
        for model in self.registry['models']:
            if model['name'] == model_name and model['version'] == version:
                model['archived'] = True
                model['active'] = False
                model['archived_at'] = datetime.now().isoformat()
                self._save_registry()
                print(f"✓ Archived {model_name} v{version}")
                return
        print(f"Model {model_name} v{version} not found")

    def delete_model(self, model_name: str, version: str, delete_files: bool = False):
        """
        Delete a model from the registry.

        Args:
            model_name: Name of the model
            version: Version to delete
            delete_files: If True, also delete model files from disk
        """
        for i, model in enumerate(self.registry['models']):
            if model['name'] == model_name and model['version'] == version:
                if delete_files:
                    model_path = Path(model['path'])
                    if model_path.exists():
                        if model_path.is_dir():
                            shutil.rmtree(model_path)
                        else:
                            model_path.unlink()
                        # Also delete metadata files if they exist
                        json_path = model_path.with_suffix('.json')
                        if json_path.exists():
                            json_path.unlink()
                        print(f"✓ Deleted model files at {model_path}")

                del self.registry['models'][i]
                self._save_registry()
                print(f"✓ Removed {model_name} v{version} from registry")
                return
        print(f"Model {model_name} v{version} not found")

    def update_metrics(self, model_name: str, version: str, metrics: Dict):
        """
        Update performance metrics for a model.

        Args:
            model_name: Name of the model
            version: Model version
            metrics: Dictionary of metrics to update
        """
        for model in self.registry['models']:
            if model['name'] == model_name and model['version'] == version:
                model['metrics'].update(metrics)
                model['metrics_updated_at'] = datetime.now().isoformat()
                self._save_registry()
                print(f"✓ Updated metrics for {model_name} v{version}")
                return
        print(f"Model {model_name} v{version} not found")

    def add_tags(self, model_name: str, version: str, tags: List[str]):
        """
        Add tags to a model.

        Args:
            model_name: Name of the model
            version: Model version
            tags: List of tags to add
        """
        for model in self.registry['models']:
            if model['name'] == model_name and model['version'] == version:
                current_tags = set(model.get('tags', []))
                current_tags.update(tags)
                model['tags'] = list(current_tags)
                self._save_registry()
                print(f"✓ Added tags to {model_name} v{version}: {tags}")
                return
        print(f"Model {model_name} v{version} not found")

    def find_by_tag(self, tag: str) -> List[Dict]:
        """
        Find all models with a specific tag.

        Args:
            tag: Tag to search for

        Returns:
            List of model entries with the specified tag
        """
        return [m for m in self.registry['models'] if tag in m.get('tags', [])]

    def get_best_model(self, model_name: str, metric: str, higher_is_better: bool = True) -> Optional[Dict]:
        """
        Get the best performing model based on a specific metric.

        Args:
            model_name: Name of the model
            metric: Metric to compare (e.g., 'accuracy', 'loss')
            higher_is_better: If True, return model with highest metric value

        Returns:
            Best model entry or None if not found
        """
        models = [
            m for m in self.registry['models']
            if m['name'] == model_name and m['active'] and metric in m.get('metrics', {})
        ]

        if not models:
            return None

        if higher_is_better:
            return max(models, key=lambda x: x['metrics'][metric])
        else:
            return min(models, key=lambda x: x['metrics'][metric])

    def export_registry(self, output_path: str):
        """
        Export registry to a JSON file.

        Args:
            output_path: Path where to save the exported registry
        """
        with open(output_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
        print(f"✓ Registry exported to {output_path}")

    def get_summary(self) -> Dict:
        """
        Get a summary of the registry.

        Returns:
            Dictionary with registry statistics
        """
        total_models = len(self.registry['models'])
        active_models = len([m for m in self.registry['models'] if m['active']])
        archived_models = len([m for m in self.registry['models'] if m.get('archived', False)])

        model_types = {}
        for model in self.registry['models']:
            name = model['name']
            model_types[name] = model_types.get(name, 0) + 1

        return {
            'total_models': total_models,
            'active_models': active_models,
            'archived_models': archived_models,
            'model_types': model_types,
            'registry_path': str(self.registry_file)
        }

    def print_summary(self):
        """Print a formatted summary of the registry."""
        summary = self.get_summary()

        print("\n" + "="*50)
        print("MODEL REGISTRY SUMMARY")
        print("="*50)
        print(f"Total Models: {summary['total_models']}")
        print(f"Active Models: {summary['active_models']}")
        print(f"Archived Models: {summary['archived_models']}")
        print(f"\nModel Types:")
        for model_type, count in summary['model_types'].items():
            print(f"  - {model_type}: {count}")
        print(f"\nRegistry Path: {summary['registry_path']}")
        print("="*50 + "\n")
