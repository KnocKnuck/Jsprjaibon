# EuroMillions ML Models Documentation

**Version:** 1.0
**Date:** 2025-11-15
**Author:** ML Engineering Team

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Model Implementations](#model-implementations)
4. [Model Registry](#model-registry)
5. [Usage Examples](#usage-examples)
6. [Performance Considerations](#performance-considerations)
7. [Future Improvements](#future-improvements)

---

## Overview

The EuroMillions ML prediction system implements two complementary machine learning models:

- **Random Forest**: Ensemble learning model for robust baseline predictions
- **LSTM**: Deep learning model for capturing temporal patterns in sequential draws

Both models follow a common interface defined by the `BaseModel` abstract class, ensuring consistent API and making it easy to add new model types.

### Key Features

- **Unified Interface**: All models inherit from `BaseModel`
- **Dual Output**: Separate predictions for numbers (1-50) and stars (1-12)
- **Model Registry**: Version control and tracking system
- **Comprehensive Testing**: Unit tests for all components
- **Save/Load Support**: Persistent model storage

---

## Architecture

### Base Model Interface

All models implement the `BaseModel` abstract class:

```python
from euromillions_ml.models import BaseModel

class BaseModel(ABC):
    """Abstract base class for all models"""

    @abstractmethod
    def train(self, X, y_numbers, y_stars):
        """Train the model"""
        pass

    @abstractmethod
    def predict(self, X) -> Tuple[np.ndarray, np.ndarray]:
        """Predict numbers and stars probabilities"""
        pass

    @abstractmethod
    def save(self, path: str):
        """Save model to disk"""
        pass

    @abstractmethod
    def load(self, path: str):
        """Load model from disk"""
        pass
```

### Data Flow

```
Historical Draws
       ↓
Feature Engineering
       ↓
[Training Data: X, y_numbers, y_stars]
       ↓
    Models
    ├── Random Forest → Probabilities (Numbers + Stars)
    └── LSTM         → Probabilities (Numbers + Stars)
       ↓
Model Registry
       ↓
Prediction API
```

---

## Model Implementations

### 1. Random Forest Model

**File:** `/home/user/Jsprjaibon/euromillions_ml/models/random_forest.py`

#### Architecture

- **Algorithm**: Ensemble of decision trees
- **Implementation**: scikit-learn `RandomForestClassifier` with `MultiOutputClassifier`
- **Separate Models**: One for main numbers, one for stars

#### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `n_estimators` | 200 | Number of trees in the forest |
| `max_depth` | 15 | Maximum depth of each tree |
| `random_state` | 42 | Random seed for reproducibility |
| `n_jobs` | -1 | Use all CPU cores |
| `class_weight` | 'balanced' | Handle class imbalance |

#### Input/Output

**Input:**
- `X`: Feature matrix `(n_samples, n_features)`
- `y_numbers`: Target numbers `(n_samples, 5)` - indices 0-49
- `y_stars`: Target stars `(n_samples, 2)` - indices 0-11

**Output:**
- `numbers_probabilities`: Array `(50,)` - probability for each number 1-50
- `stars_probabilities`: Array `(12,)` - probability for each star 1-12

#### Advantages

- Fast training and prediction
- Handles non-linear relationships
- Built-in feature importance
- Robust to overfitting
- No need for feature scaling

#### Limitations

- Cannot capture temporal dependencies
- Memory intensive with many trees
- Less effective on sequential patterns

---

### 2. LSTM Neural Network

**File:** `/home/user/Jsprjaibon/euromillions_ml/models/lstm.py`

#### Architecture

```
Input Layer (sequence_length, n_features)
       ↓
LSTM Layer (128 units, return_sequences=True)
       ↓
Dropout (0.3)
       ↓
LSTM Layer (64 units, return_sequences=False)
       ↓
Dropout (0.3)
       ↓
Dense Layer (32 units, ReLU)
       ↓
    ├─→ Numbers Output (50 units, Softmax)
    └─→ Stars Output (12 units, Softmax)
```

#### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `sequence_length` | 10 | Number of past draws to consider |
| `hidden_units` | 128 | LSTM hidden units in first layer |
| `dropout` | 0.3 | Dropout rate for regularization |
| `learning_rate` | 0.001 | Adam optimizer learning rate |
| `epochs` | 100 | Training epochs |
| `batch_size` | 32 | Batch size for training |

#### Input/Output

**Input:**
- `X`: Sequences `(n_samples, sequence_length, n_features)`
- `y_numbers`: Target numbers `(n_samples, 1)` or one-hot encoded
- `y_stars`: Target stars `(n_samples, 1)` or one-hot encoded

**Output:**
- `numbers_probabilities`: Array `(50,)` - softmax probabilities
- `stars_probabilities`: Array `(12,)` - softmax probabilities

#### Advantages

- Captures temporal patterns
- Learns from sequences of draws
- Deep learning power
- Automatic feature learning

#### Limitations

- Requires more training data (300+ draws recommended)
- Slower training time
- Needs careful hyperparameter tuning
- Risk of overfitting on small datasets

---

## Model Registry

**File:** `/home/user/Jsprjaibon/euromillions_ml/models/registry.py`

The Model Registry provides version control and tracking for all trained models.

### Features

- **Version Tracking**: Maintains history of all model versions
- **Metadata Storage**: Stores hyperparameters, training info
- **Performance Metrics**: Tracks model performance over time
- **Tagging System**: Organize models with custom tags
- **Best Model Selection**: Find best performing model by metric
- **Active/Archived States**: Manage model lifecycle

### Registry Structure

```json
{
  "models": [
    {
      "name": "RandomForest",
      "version": "v2025.11.15",
      "path": "/path/to/model.pkl",
      "metadata": {
        "n_estimators": 200,
        "max_depth": 15,
        "n_samples": 1000
      },
      "metrics": {
        "accuracy": 0.85,
        "precision": 0.82
      },
      "tags": ["production", "baseline"],
      "registered_at": "2025-11-15T10:30:00",
      "active": true,
      "archived": false
    }
  ]
}
```

### Common Operations

```python
from euromillions_ml.models import ModelRegistry

# Initialize registry
registry = ModelRegistry(registry_dir="./trained_models")

# Register a model
registry.register_model(
    model_name='RandomForest',
    version='v1.0',
    metadata=model.get_metadata(),
    model_path='/path/to/model.pkl',
    metrics={'accuracy': 0.85},
    tags=['production']
)

# Get latest version
latest = registry.get_latest('RandomForest')

# Get best model by metric
best = registry.get_best_model('RandomForest', 'accuracy', higher_is_better=True)

# List all models
models = registry.list_models()

# Archive old version
registry.archive_model('RandomForest', 'v1.0')
```

---

## Usage Examples

### Training Random Forest

```python
from euromillions_ml.models import RandomForestModel, ModelRegistry
import numpy as np

# Prepare data
X = np.random.randn(1000, 50)  # 1000 samples, 50 features
y_numbers = np.random.randint(0, 50, size=(1000, 5))
y_stars = np.random.randint(0, 12, size=(1000, 2))

# Initialize and train
model = RandomForestModel(n_estimators=200, max_depth=15)
model.train(X, y_numbers, y_stars)

# Make prediction
numbers_prob, stars_prob = model.predict(X[:1])

# Get top predictions
top_numbers = np.argsort(numbers_prob)[-5:][::-1] + 1
top_stars = np.argsort(stars_prob)[-2:][::-1] + 1

print(f"Predicted numbers: {top_numbers}")
print(f"Predicted stars: {top_stars}")

# Save model
model.save("./models/rf_model.pkl")

# Register
registry = ModelRegistry()
registry.register_model(
    'RandomForest', 'v1.0',
    model.get_metadata(),
    './models/rf_model.pkl'
)
```

### Training LSTM

```python
from euromillions_ml.models import LSTMModel
import numpy as np

# Prepare sequential data
sequence_length = 10
X_seq = np.random.randn(500, sequence_length, 30)
y_numbers = np.random.randint(0, 50, size=(500, 1))
y_stars = np.random.randint(0, 12, size=(500, 1))

# Initialize and train
model = LSTMModel(
    sequence_length=10,
    hidden_units=128,
    dropout=0.3
)

model.train(
    X_seq, y_numbers, y_stars,
    epochs=50,
    batch_size=32
)

# Make prediction
numbers_prob, stars_prob = model.predict(X_seq[-1:])

# Save model
model.save("./models/lstm_model")  # Saves .h5 and .json
```

### Loading and Using Saved Models

```python
from euromillions_ml.models import RandomForestModel, LSTMModel

# Load RandomForest
rf = RandomForestModel()
rf.load("./models/rf_model.pkl")

# Load LSTM
lstm = LSTMModel()
lstm.load("./models/lstm_model")

# Use for predictions
numbers, stars = rf.predict(X_new)
```

---

## Performance Considerations

### Random Forest

#### Training Time
- **1000 samples**: ~30-60 seconds
- **5000 samples**: ~2-5 minutes
- Scales linearly with n_estimators

#### Memory Usage
- Proportional to: `n_estimators × max_depth × n_samples`
- Typical: 50-200 MB for 200 trees

#### Optimization Tips
- Reduce `n_estimators` for faster training
- Limit `max_depth` to prevent overfitting
- Use `min_samples_split` and `min_samples_leaf` for regularization

### LSTM

#### Training Time
- **500 samples, 50 epochs**: ~5-10 minutes (GPU)
- **500 samples, 50 epochs**: ~20-40 minutes (CPU)
- Benefits greatly from GPU acceleration

#### Memory Usage
- Depends on: `sequence_length × hidden_units × batch_size`
- Typical: 100-500 MB

#### Optimization Tips
- Use GPU for training (10-20x faster)
- Start with fewer epochs, use early stopping
- Reduce `batch_size` if memory is limited
- Adjust `sequence_length` based on available data

---

## Testing

### Running Unit Tests

```bash
# Test all models
pytest tests/test_models/ -v

# Test specific model
pytest tests/test_models/test_random_forest.py -v
pytest tests/test_models/test_lstm.py -v
pytest tests/test_models/test_registry.py -v

# With coverage
pytest tests/test_models/ --cov=euromillions_ml.models --cov-report=html
```

### Test Coverage

- **Base Model**: Interface validation
- **Random Forest**: Training, prediction, save/load, feature importance
- **LSTM**: Training, prediction, save/load, architecture
- **Registry**: Registration, versioning, querying, lifecycle management

---

## Future Improvements

### Model Enhancements

1. **Ensemble Methods**
   - Combine RF and LSTM predictions
   - Weighted voting based on historical performance
   - Stacking classifier

2. **Hyperparameter Optimization**
   - Grid search for optimal parameters
   - Bayesian optimization
   - Auto-tuning based on data size

3. **Additional Models**
   - Gradient Boosting (XGBoost, LightGBM)
   - Transformer models for sequence prediction
   - CNN for pattern recognition

### Feature Engineering

1. **Advanced Features**
   - Cross-correlation analysis
   - Fourier transforms for cyclical patterns
   - Graph-based features

2. **Automated Feature Selection**
   - Recursive feature elimination
   - Feature importance ranking
   - Correlation analysis

### Infrastructure

1. **Model Serving**
   - REST API for predictions
   - Model versioning in production
   - A/B testing framework

2. **Monitoring**
   - Prediction quality tracking
   - Model drift detection
   - Performance dashboards

3. **MLOps**
   - Automated retraining pipeline
   - Continuous integration for models
   - Experiment tracking (MLflow, Weights & Biases)

---

## File Structure

```
euromillions_ml/models/
├── __init__.py           # Package exports
├── base.py              # BaseModel abstract class
├── random_forest.py     # RandomForest implementation
├── lstm.py              # LSTM implementation
└── registry.py          # ModelRegistry

tests/test_models/
├── __init__.py
├── test_random_forest.py
├── test_lstm.py
└── test_registry.py

trained_models/
├── registry.json        # Model registry
├── random_forest/
│   └── rf_model_*.pkl
└── lstm/
    ├── lstm_model_*.h5
    └── lstm_model_*.json
```

---

## Dependencies

### Required Packages

```
# Core ML
scikit-learn>=1.0.0
tensorflow>=2.10.0
numpy>=1.21.0

# Model Persistence
joblib>=1.1.0

# Testing
pytest>=7.0.0
pytest-cov>=3.0.0
```

### Installation

```bash
pip install scikit-learn tensorflow numpy joblib pytest pytest-cov
```

---

## References

### Academic Papers

- Breiman, L. (2001). "Random Forests". Machine Learning.
- Hochreiter, S., & Schmidhuber, J. (1997). "Long Short-Term Memory". Neural Computation.

### Documentation

- [scikit-learn Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#forest)
- [TensorFlow LSTM](https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM)
- [Keras Sequential Model](https://keras.io/guides/sequential_model/)

---

## Support

For questions or issues:
- Review unit tests for usage examples
- Check `/home/user/Jsprjaibon/demo_train_models.py` for complete training workflow
- Consult inline documentation in source files

---

**Last Updated:** 2025-11-15
**Status:** Production Ready
**Version:** 1.0
