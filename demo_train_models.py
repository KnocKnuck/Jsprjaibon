#!/usr/bin/env python3
"""
Demo Training Script for RandomForest and LSTM Models

This script demonstrates the actual usage of the implemented models
with sample data and showcases the model registry functionality.

Usage:
    python demo_train_models.py --model all  # Train both models
    python demo_train_models.py --model rf   # Train RandomForest only
    python demo_train_models.py --model lstm # Train LSTM only
"""

import argparse
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from euromillions_ml.models import RandomForestModel, LSTMModel, ModelRegistry


def generate_sample_data(n_samples: int = 1000, sequence_length: int = 10):
    """
    Generate sample training data for demonstration.

    In production, this would load real historical lottery data.

    Args:
        n_samples: Number of training samples
        sequence_length: Length of sequences for LSTM

    Returns:
        Tuple of (X, y_numbers, y_stars)
    """
    print(f"Generating {n_samples} sample training instances...")

    np.random.seed(42)

    # Features: simulate historical patterns
    n_features = 50
    X = np.random.randn(n_samples, n_features)

    # Targets: 5 main numbers (1-50) and 2 stars (1-12)
    y_numbers = np.random.randint(0, 50, size=(n_samples, 5))
    y_stars = np.random.randint(0, 12, size=(n_samples, 2))

    print(f"✓ Generated data - X: {X.shape}, Numbers: {y_numbers.shape}, Stars: {y_stars.shape}")

    return X, y_numbers, y_stars


def generate_sequence_data(n_samples: int = 500, sequence_length: int = 10):
    """
    Generate sequential data for LSTM training.

    Args:
        n_samples: Number of sequences
        sequence_length: Length of each sequence

    Returns:
        Tuple of (X_seq, y_numbers, y_stars)
    """
    print(f"Generating {n_samples} sequential samples (length={sequence_length})...")

    np.random.seed(42)

    n_features = 30
    X_seq = np.random.randn(n_samples, sequence_length, n_features)

    # Targets: single draw prediction
    y_numbers = np.random.randint(0, 50, size=(n_samples, 1))
    y_stars = np.random.randint(0, 12, size=(n_samples, 1))

    print(f"✓ Generated sequences - X: {X_seq.shape}, Numbers: {y_numbers.shape}, Stars: {y_stars.shape}")

    return X_seq, y_numbers, y_stars


def train_random_forest(X, y_numbers, y_stars, registry: ModelRegistry):
    """
    Train and register RandomForest model.

    Args:
        X: Feature matrix
        y_numbers: Target numbers
        y_stars: Target stars
        registry: Model registry instance
    """
    print("\n" + "="*60)
    print("TRAINING RANDOM FOREST MODEL")
    print("="*60)

    # Initialize model
    model = RandomForestModel(
        n_estimators=200,
        max_depth=15,
        random_state=42
    )

    # Train
    model.train(X, y_numbers, y_stars)

    # Test prediction
    print("\nTesting prediction on sample data...")
    numbers_pred, stars_pred = model.predict(X[:1])

    print(f"Numbers probabilities (top 10):")
    top_numbers = np.argsort(numbers_pred)[-10:][::-1]
    for i, num in enumerate(top_numbers, 1):
        print(f"  {i}. Number {num+1}: {numbers_pred[num]:.4f}")

    print(f"\nStars probabilities (top 5):")
    top_stars = np.argsort(stars_pred)[-5:][::-1]
    for i, star in enumerate(top_stars, 1):
        print(f"  {i}. Star {star+1}: {stars_pred[star]:.4f}")

    # Save model
    model_dir = Path("./trained_models/random_forest")
    model_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = model_dir / f"rf_model_{timestamp}.pkl"

    model.save(str(model_path))

    # Register in registry
    version = datetime.now().strftime("v%Y.%m.%d")
    registry.register_model(
        model_name='RandomForest',
        version=version,
        metadata=model.get_metadata(),
        model_path=str(model_path),
        metrics={
            'trained_on': timestamp,
            'model_type': 'ensemble'
        },
        tags=['production-ready', 'baseline']
    )

    print(f"\n✓ RandomForest model saved and registered")
    print(f"  Path: {model_path}")
    print(f"  Size: {model_path.stat().st_size / 1024:.2f} KB")

    return model


def train_lstm(X, y_numbers, y_stars, registry: ModelRegistry):
    """
    Train and register LSTM model.

    Args:
        X: Sequential feature data
        y_numbers: Target numbers
        y_stars: Target stars
        registry: Model registry instance
    """
    print("\n" + "="*60)
    print("TRAINING LSTM MODEL")
    print("="*60)

    # Initialize model
    model = LSTMModel(
        sequence_length=10,
        hidden_units=128,
        dropout=0.3
    )

    # Train
    model.train(
        X, y_numbers, y_stars,
        epochs=10,  # Reduced for demo
        batch_size=32,
        validation_split=0.2
    )

    # Test prediction
    print("\nTesting prediction on sample sequence...")
    numbers_pred, stars_pred = model.predict(X[:1])

    print(f"Numbers probabilities (top 10):")
    top_numbers = np.argsort(numbers_pred)[-10:][::-1]
    for i, num in enumerate(top_numbers, 1):
        print(f"  {i}. Number {num+1}: {numbers_pred[num]:.4f}")

    print(f"\nStars probabilities (top 5):")
    top_stars = np.argsort(stars_pred)[-5:][::-1]
    for i, star in enumerate(top_stars, 1):
        print(f"  {i}. Star {star+1}: {stars_pred[star]:.4f}")

    # Save model
    model_dir = Path("./trained_models/lstm")
    model_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = model_dir / f"lstm_model_{timestamp}"

    model.save(str(model_path))

    # Register in registry
    version = datetime.now().strftime("v%Y.%m.%d")
    registry.register_model(
        model_name='LSTM',
        version=version,
        metadata=model.get_metadata(),
        model_path=str(model_path),
        metrics={
            'trained_on': timestamp,
            'model_type': 'deep_learning',
            'final_loss': model.metadata.get('final_loss', 0)
        },
        tags=['deep-learning', 'sequential']
    )

    # Get file sizes
    h5_size = Path(str(model_path) + '.h5').stat().st_size / 1024
    json_size = Path(str(model_path) + '.json').stat().st_size / 1024

    print(f"\n✓ LSTM model saved and registered")
    print(f"  Path: {model_path}")
    print(f"  Model size: {h5_size:.2f} KB")
    print(f"  Metadata size: {json_size:.2f} KB")

    return model


def main():
    """Main training workflow."""
    parser = argparse.ArgumentParser(description='Train EuroMillions prediction models')
    parser.add_argument(
        '--model',
        choices=['all', 'rf', 'lstm'],
        default='all',
        help='Which model to train (default: all)'
    )
    parser.add_argument(
        '--samples',
        type=int,
        default=1000,
        help='Number of training samples (default: 1000)'
    )

    args = parser.parse_args()

    print("\n" + "="*60)
    print("EUROMILLIONS ML MODEL TRAINING")
    print("="*60)
    print(f"Training mode: {args.model.upper()}")
    print(f"Samples: {args.samples}")

    # Initialize model registry
    registry = ModelRegistry(registry_dir="./trained_models")

    # Train models based on selection
    if args.model in ['all', 'rf']:
        X, y_numbers, y_stars = generate_sample_data(n_samples=args.samples)
        train_random_forest(X, y_numbers, y_stars, registry)

    if args.model in ['all', 'lstm']:
        X_seq, y_numbers_seq, y_stars_seq = generate_sequence_data(
            n_samples=min(args.samples, 500),  # LSTM needs less data for demo
            sequence_length=10
        )
        train_lstm(X_seq, y_numbers_seq, y_stars_seq, registry)

    # Print registry summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE - REGISTRY SUMMARY")
    print("="*60)
    registry.print_summary()

    # List all models
    print("\nRegistered Models:")
    for model in registry.list_models():
        print(f"\n  {model['name']} {model['version']}")
        print(f"    Path: {model['path']}")
        print(f"    Tags: {', '.join(model['tags'])}")
        print(f"    Registered: {model['registered_at']}")

    print("\n✓ All training tasks completed successfully!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
