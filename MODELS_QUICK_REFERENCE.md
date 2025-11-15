# EuroMillions ML Models - Quick Reference

## Installation

```bash
pip install -r requirements.txt
```

## Basic Usage

### Random Forest

```python
from euromillions_ml.models import RandomForestModel
import numpy as np

# Initialize
model = RandomForestModel(
    n_estimators=200,
    max_depth=15,
    random_state=42
)

# Train
X = np.random.randn(1000, 50)  # 1000 samples, 50 features
y_numbers = np.random.randint(0, 50, size=(1000, 5))  # 5 numbers
y_stars = np.random.randint(0, 12, size=(1000, 2))    # 2 stars

model.train(X, y_numbers, y_stars)

# Predict
numbers_prob, stars_prob = model.predict(X[:1])

# Get top predictions
top_numbers = np.argsort(numbers_prob)[-5:][::-1] + 1  # Top 5 numbers
top_stars = np.argsort(stars_prob)[-2:][::-1] + 1      # Top 2 stars

# Save/Load
model.save("./models/rf_model.pkl")
model.load("./models/rf_model.pkl")

# Feature importance
importance = model.get_feature_importance()
```

### LSTM

```python
from euromillions_ml.models import LSTMModel
import numpy as np

# Initialize
model = LSTMModel(
    sequence_length=10,
    hidden_units=128,
    dropout=0.3
)

# Train
X_seq = np.random.randn(500, 10, 30)  # 500 sequences, length 10, 30 features
y_numbers = np.random.randint(0, 50, size=(500, 1))
y_stars = np.random.randint(0, 12, size=(500, 1))

model.train(
    X_seq, y_numbers, y_stars,
    epochs=50,
    batch_size=32,
    validation_split=0.2
)

# Predict
numbers_prob, stars_prob = model.predict(X_seq[-1:])

# Save/Load
model.save("./models/lstm_model")  # Creates .h5 and .json files
model.load("./models/lstm_model")
```

### Model Registry

```python
from euromillions_ml.models import ModelRegistry

# Initialize
registry = ModelRegistry(registry_dir="./trained_models")

# Register a model
registry.register_model(
    model_name='RandomForest',
    version='v1.0',
    metadata=model.get_metadata(),
    model_path='./models/rf_model.pkl',
    metrics={'accuracy': 0.85, 'precision': 0.82},
    tags=['production', 'baseline']
)

# Get latest version
latest = registry.get_latest('RandomForest')

# Get specific version
model_v1 = registry.get_version('RandomForest', 'v1.0')

# List all models
all_models = registry.list_models()

# Get best model by metric
best = registry.get_best_model('RandomForest', 'accuracy', higher_is_better=True)

# Find by tag
production_models = registry.find_by_tag('production')

# Update metrics
registry.update_metrics('RandomForest', 'v1.0', {'accuracy': 0.90})

# Archive old version
registry.archive_model('RandomForest', 'v1.0')

# Print summary
registry.print_summary()
```

## Training Script

```bash
# Train both models
python demo_train_models.py --model all --samples 1000

# Train Random Forest only
python demo_train_models.py --model rf --samples 2000

# Train LSTM only
python demo_train_models.py --model lstm --samples 500
```

## Running Tests

```bash
# All tests
pytest tests/test_models/ -v

# Specific model
pytest tests/test_models/test_random_forest.py -v

# With coverage
pytest tests/test_models/ --cov=euromillions_ml.models --cov-report=html
```

## Model Specifications

### Random Forest
- **Input**: `(n_samples, n_features)`
- **Output**: Numbers `(50,)`, Stars `(12,)` probability arrays
- **Training Time**: ~45s for 1000 samples
- **Memory**: 50-200 MB

### LSTM
- **Input**: `(n_samples, sequence_length, n_features)`
- **Output**: Numbers `(50,)`, Stars `(12,)` probability arrays (softmax)
- **Training Time**: ~10min (GPU) for 500 samples, 50 epochs
- **Memory**: 100-500 MB

## File Paths

```
/home/user/Jsprjaibon/
├── euromillions_ml/models/
│   ├── base.py              # BaseModel class
│   ├── random_forest.py     # RandomForest implementation
│   ├── lstm.py              # LSTM implementation
│   └── registry.py          # ModelRegistry
│
├── tests/test_models/       # Unit tests
│
├── demo_train_models.py     # Training demo script
└── MODELS_DOCUMENTATION.md  # Full documentation
```

## Common Issues

**Import Error**: Install dependencies first
```bash
pip install -r requirements.txt
```

**LSTM Slow**: Use GPU for faster training
```python
# Check if GPU is available
import tensorflow as tf
print("GPU Available:", tf.config.list_physical_devices('GPU'))
```

**Model Not Trained Error**: Call `train()` before `predict()`
```python
model.train(X, y_numbers, y_stars)  # Train first
numbers_prob, stars_prob = model.predict(X_new)  # Then predict
```

## More Information

- Full Documentation: `/home/user/Jsprjaibon/MODELS_DOCUMENTATION.md`
- Implementation Report: `/home/user/Jsprjaibon/MODELS_IMPLEMENTATION_REPORT.md`
- Unit Tests: `/home/user/Jsprjaibon/tests/test_models/`
