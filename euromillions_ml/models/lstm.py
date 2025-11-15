"""
LSTM (Long Short-Term Memory) neural network implementation for EuroMillions prediction.

This module implements a deep learning model using LSTM layers to capture
temporal patterns in lottery draw sequences.
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from typing import Tuple, Optional, Dict
from pathlib import Path
import json

from .base import BaseModel


class LSTMModel(BaseModel):
    """
    LSTM Neural Network for lottery prediction.

    Uses recurrent neural networks to learn patterns from sequences
    of historical draws and predict future numbers and stars.

    Attributes:
        sequence_length (int): Number of past draws to consider
        hidden_units (int): Number of LSTM hidden units
        dropout (float): Dropout rate for regularization
        model: Keras model instance
    """

    def __init__(
        self,
        sequence_length: int = 10,
        hidden_units: int = 128,
        dropout: float = 0.3
    ):
        """
        Initialize LSTM model.

        Args:
            sequence_length: Number of past draws to use as input (default: 10)
            hidden_units: Number of LSTM hidden units (default: 128)
            dropout: Dropout rate for regularization (default: 0.3)
        """
        super().__init__("LSTM")
        self.sequence_length = sequence_length
        self.hidden_units = hidden_units
        self.dropout = dropout
        self.model = None
        self.history = None

    def _build_model(self, input_shape: Tuple[int, int]) -> keras.Model:
        """
        Build LSTM neural network architecture.

        Architecture:
        - Input layer (sequence_length, n_features)
        - LSTM layer (hidden_units) with return sequences
        - Dropout layer
        - LSTM layer (64)
        - Dropout layer
        - Dense layer (32) with ReLU
        - Two output heads:
          * Numbers output (50 classes, softmax)
          * Stars output (12 classes, softmax)

        Args:
            input_shape: Shape of input sequences (sequence_length, n_features)

        Returns:
            Compiled Keras model
        """
        inputs = keras.Input(shape=input_shape, name='input')

        # First LSTM layer - captures long-term dependencies
        x = layers.LSTM(
            self.hidden_units,
            return_sequences=True,
            name='lstm_1'
        )(inputs)
        x = layers.Dropout(self.dropout, name='dropout_1')(x)

        # Second LSTM layer - refines patterns
        x = layers.LSTM(64, return_sequences=False, name='lstm_2')(x)
        x = layers.Dropout(self.dropout, name='dropout_2')(x)

        # Dense layer for feature combination
        x = layers.Dense(32, activation='relu', name='dense_hidden')(x)

        # Output layers - separate heads for numbers and stars
        numbers_output = layers.Dense(
            50,
            activation='softmax',
            name='numbers'
        )(x)
        stars_output = layers.Dense(
            12,
            activation='softmax',
            name='stars'
        )(x)

        # Build and compile model
        model = keras.Model(inputs=inputs, outputs=[numbers_output, stars_output])

        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss={
                'numbers': 'categorical_crossentropy',
                'stars': 'categorical_crossentropy'
            },
            metrics=['accuracy']
        )

        return model

    def train(
        self,
        X: np.ndarray,
        y_numbers: np.ndarray,
        y_stars: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32,
        validation_split: float = 0.2
    ):
        """
        Train LSTM model on sequential data.

        Args:
            X: Input sequences of shape (n_samples, sequence_length, n_features)
               or (n_samples, n_features) which will be reshaped
            y_numbers: Target labels for main numbers (n_samples, 5)
            y_stars: Target labels for star numbers (n_samples, 2)
            epochs: Number of training epochs (default: 100)
            batch_size: Batch size for training (default: 32)
            validation_split: Fraction of data to use for validation (default: 0.2)
        """
        print(f"Training LSTM on {X.shape[0]} sequences...")

        # Reshape X for LSTM if needed (samples, sequence_length, features)
        if len(X.shape) == 2:
            # Assume we need to reshape based on sequence_length
            n_samples = X.shape[0]
            n_features = X.shape[1] // self.sequence_length
            X = X.reshape(n_samples, self.sequence_length, n_features)
            print(f"Reshaped input to: {X.shape}")

        # Build model
        print(f"Building LSTM model with input shape: {(X.shape[1], X.shape[2])}")
        self.model = self._build_model((X.shape[1], X.shape[2]))

        # Display model summary
        print("\nModel Architecture:")
        self.model.summary()

        # Convert targets to categorical if needed
        if len(y_numbers.shape) == 2 and y_numbers.shape[1] != 50:
            # Assuming y_numbers contains class indices, not one-hot
            # For now, we'll work with the first column or create proper encoding
            y_numbers_cat = self._encode_multi_label(y_numbers, num_classes=50)
        else:
            y_numbers_cat = y_numbers

        if len(y_stars.shape) == 2 and y_stars.shape[1] != 12:
            y_stars_cat = self._encode_multi_label(y_stars, num_classes=12)
        else:
            y_stars_cat = y_stars

        # Early stopping to prevent overfitting
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        )

        # Model checkpoint
        checkpoint_path = '/tmp/lstm_best.h5'
        model_checkpoint = keras.callbacks.ModelCheckpoint(
            checkpoint_path,
            monitor='val_loss',
            save_best_only=True
        )

        # Train model
        print(f"\nTraining for {epochs} epochs with batch size {batch_size}...")
        self.history = self.model.fit(
            X,
            {'numbers': y_numbers_cat, 'stars': y_stars_cat},
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=[early_stopping, model_checkpoint],
            verbose=1
        )

        self.trained = True
        self.metadata = {
            'model_type': 'LSTM',
            'sequence_length': self.sequence_length,
            'hidden_units': self.hidden_units,
            'dropout': self.dropout,
            'epochs_trained': len(self.history.history['loss']),
            'final_loss': float(self.history.history['loss'][-1]),
            'final_val_loss': float(self.history.history['val_loss'][-1]),
            'n_samples': X.shape[0],
            'input_shape': list(X.shape[1:])
        }
        print("✓ LSTM training complete")

    def _encode_multi_label(self, y: np.ndarray, num_classes: int) -> np.ndarray:
        """
        Encode multi-label targets to categorical format.

        Args:
            y: Target array of shape (n_samples, n_labels)
            num_classes: Total number of classes

        Returns:
            Categorical array suitable for training
        """
        # For multi-label, we'll use the first column or aggregate
        # This is a simplified encoding - might need adjustment based on actual data format
        if y.shape[1] == 1:
            return keras.utils.to_categorical(y.flatten(), num_classes=num_classes)
        else:
            # Take first label as primary target
            return keras.utils.to_categorical(y[:, 0], num_classes=num_classes)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict probabilities for numbers and stars.

        Args:
            X: Input features or sequences

        Returns:
            Tuple of (numbers_probabilities, stars_probabilities)
            - numbers_probabilities: Array of shape (50,) with probability for each number
            - stars_probabilities: Array of shape (12,) with probability for each star

        Raises:
            ValueError: If model has not been trained
        """
        if not self.trained:
            raise ValueError("Model not trained. Call train() first.")

        # Reshape if needed
        if len(X.shape) == 2:
            n_samples = X.shape[0]
            n_features = X.shape[1] // self.sequence_length
            X = X.reshape(n_samples, self.sequence_length, n_features)

        # Predict
        numbers_pred, stars_pred = self.model.predict(X, verbose=0)

        # Return first prediction (or average if multiple samples)
        if numbers_pred.shape[0] == 1:
            return numbers_pred[0], stars_pred[0]
        else:
            return numbers_pred.mean(axis=0), stars_pred.mean(axis=0)

    def save(self, path: str):
        """
        Save LSTM model to disk.

        Saves both the Keras model (.h5) and metadata (.json).

        Args:
            path: File path where model should be saved (without extension)
        """
        if not self.trained:
            raise ValueError("Cannot save untrained model")

        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)

        # Save Keras model
        model_path = str(path_obj.with_suffix('.h5'))
        self.model.save(model_path)

        # Save metadata separately
        metadata_path = str(path_obj.with_suffix('.json'))
        with open(metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)

        print(f"✓ Model saved to {model_path}")
        print(f"✓ Metadata saved to {metadata_path}")

    def load(self, path: str):
        """
        Load LSTM model from disk.

        Args:
            path: File path from which to load the model (without extension)
        """
        path_obj = Path(path)

        # Load Keras model
        model_path = str(path_obj.with_suffix('.h5'))
        self.model = keras.models.load_model(model_path)

        # Load metadata
        metadata_path = str(path_obj.with_suffix('.json'))
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)

        # Restore hyperparameters
        self.sequence_length = self.metadata.get('sequence_length', self.sequence_length)
        self.hidden_units = self.metadata.get('hidden_units', self.hidden_units)
        self.dropout = self.metadata.get('dropout', self.dropout)

        self.trained = True
        print(f"✓ Model loaded from {model_path}")
        print(f"✓ Metadata loaded from {metadata_path}")

    def plot_training_history(self, save_path: Optional[str] = None):
        """
        Plot training history (loss and accuracy curves).

        Args:
            save_path: Optional path to save the plot
        """
        if self.history is None:
            raise ValueError("No training history available")

        try:
            import matplotlib.pyplot as plt

            fig, axes = plt.subplots(2, 2, figsize=(12, 8))

            # Loss plots
            axes[0, 0].plot(self.history.history['loss'], label='Training Loss')
            axes[0, 0].plot(self.history.history['val_loss'], label='Validation Loss')
            axes[0, 0].set_title('Model Loss')
            axes[0, 0].set_xlabel('Epoch')
            axes[0, 0].set_ylabel('Loss')
            axes[0, 0].legend()

            # Numbers accuracy
            axes[0, 1].plot(self.history.history['numbers_accuracy'], label='Training')
            axes[0, 1].plot(self.history.history['val_numbers_accuracy'], label='Validation')
            axes[0, 1].set_title('Numbers Accuracy')
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('Accuracy')
            axes[0, 1].legend()

            # Stars accuracy
            axes[1, 0].plot(self.history.history['stars_accuracy'], label='Training')
            axes[1, 0].plot(self.history.history['val_stars_accuracy'], label='Validation')
            axes[1, 0].set_title('Stars Accuracy')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Accuracy')
            axes[1, 0].legend()

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path)
                print(f"✓ Training history plot saved to {save_path}")
            else:
                plt.show()

        except ImportError:
            print("matplotlib not available for plotting")
