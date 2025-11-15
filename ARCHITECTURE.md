# Euromillions ML Predictor - System Architecture

## 1. System Architecture Overview

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EUROMILLIONS ML PREDICTOR                         │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│   DATA       │────▶│  FEATURES    │────▶│   MODELS     │────▶│  OUTPUT  │
│  INGESTION   │     │ ENGINEERING  │     │  TRAINING    │     │ RESULTS  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────┘
      │                     │                     │                   │
      ▼                     ▼                     ▼                   ▼
┌──────────┐         ┌──────────┐         ┌──────────┐         ┌──────────┐
│ Scraper  │         │Feature   │         │ LSTM     │         │Terminal  │
│ FDJ Web  │         │Extract   │         │RandomFor.│         │Display   │
│ CSV Load │         │Normalize │         │ Markov   │         │Metrics   │
│ Validate │         │          │         │ Hybrid   │         │Export    │
└──────────┘         └──────────┘         └──────────┘         └──────────┘
```

### Data Flow Pipeline

```
1. DATA ACQUISITION
   ├─ Web Scraper (FDJ website) ──┐
   └─ CSV Fallback Loader ────────┼──▶ Raw Historical Data
                                  │
2. DATA VALIDATION                │
   └─ Schema Check ───────────────┤
   └─ Quality Control ────────────┼──▶ Validated Dataset
                                  │
3. FEATURE ENGINEERING            │
   ├─ Frequency Analysis ─────────┤
   ├─ Pattern Detection ──────────┤
   ├─ Statistical Features ───────┤
   └─ Time-based Features ────────┼──▶ Feature Matrix (X)
                                  │
4. DATA NORMALIZATION             │
   └─ MinMax/Standard Scaling ────┼──▶ Normalized Features
                                  │
5. MODEL TRAINING                 │
   ├─ LSTM (TensorFlow) ──────────┤
   ├─ Random Forest (sklearn) ────┤
   ├─ Markov Chain ───────────────┤
   └─ Hybrid Ensemble ────────────┼──▶ Trained Models
                                  │
6. PREDICTION/BACKTEST            │
   ├─ Single Prediction ──────────┤
   ├─ Batch Prediction ───────────┤
   └─ Historical Backtest ────────┼──▶ Predictions + Metrics
                                  │
7. OUTPUT GENERATION              │
   ├─ Terminal Display ───────────┤
   ├─ Metrics Calculation ────────┤
   └─ Export (CSV/JSON) ──────────┴──▶ Final Results
```

### Core Components

1. **Data Layer**: Acquisition, validation, and storage of historical lottery data
2. **Feature Layer**: Transform raw draws into ML-ready features
3. **Model Layer**: Multiple ML algorithms with ensemble capability
4. **Prediction Layer**: Generate predictions and backtesting
5. **Presentation Layer**: CLI interface and result visualization

---

## 2. Module Structure & Detailed Design

### Project Directory Layout

```
euromillions_ml/
├── __init__.py                 # Package initialization
├── data/
│   ├── __init__.py
│   ├── scraper.py              # Web scraping from FDJ
│   ├── loader.py               # CSV data loading
│   └── validator.py            # Data validation and cleaning
├── features/
│   ├── __init__.py
│   ├── engineering.py          # Feature extraction logic
│   └── normalizer.py           # Data normalization
├── models/
│   ├── __init__.py
│   ├── base.py                 # Base model interface
│   ├── lstm.py                 # LSTM neural network
│   ├── random_forest.py        # Random Forest classifier
│   ├── markov.py               # Markov chain model
│   └── hybrid.py               # Ensemble fusion model
├── prediction/
│   ├── __init__.py
│   ├── predictor.py            # Main prediction engine
│   └── backtest.py             # Backtesting functionality
└── utils/
    ├── __init__.py
    ├── display.py              # Terminal formatting
    ├── metrics.py              # Performance metrics
    └── config.py               # Configuration management

main.py                          # CLI entry point
config.yaml                      # Configuration file
requirements.txt                 # Python dependencies
tests/                           # Unit and integration tests
data/                            # Data storage directory
models/                          # Saved model checkpoints
logs/                            # Application logs
```

---

### 2.1 Data Module (`euromillions_ml/data/`)

#### 2.1.1 `scraper.py` - Web Scraping

**Responsibility**: Fetch historical Euromillions draw data from FDJ website

**Main Classes**:
- `FDJScraper`: Web scraper for FDJ official website

**Key Methods**:
```python
class FDJScraper:
    """Scraper for FDJ Euromillions historical data."""

    def __init__(self, cache_dir: str = "data/cache"):
        """Initialize scraper with caching directory."""
        self.base_url = "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million"
        self.cache_dir = cache_dir
        self.session = requests.Session()

    def fetch_historical_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> pd.DataFrame:
        """
        Fetch historical draws between dates.

        Args:
            start_date: Start date for data collection
            end_date: End date for data collection

        Returns:
            DataFrame with columns: date, n1, n2, n3, n4, n5, s1, s2
        """
        pass

    def fetch_latest_draw(self) -> Dict[str, Any]:
        """Fetch the most recent draw results."""
        pass

    def parse_draw_page(self, html: str) -> List[Dict]:
        """Parse HTML page and extract draw information."""
        pass

    def cache_results(self, data: pd.DataFrame, filename: str):
        """Cache scraped data to avoid repeated requests."""
        pass
```

**Input**: Date range, URL configuration
**Output**: DataFrame with draw history (date, 5 numbers, 2 stars)

---

#### 2.1.2 `loader.py` - CSV Data Loading

**Responsibility**: Load historical data from CSV files (fallback/offline mode)

**Main Classes**:
- `DataLoader`: Generic data loading interface

**Key Methods**:
```python
class DataLoader:
    """Load Euromillions data from various sources."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir

    def load_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            filepath: Path to CSV file

        Returns:
            DataFrame with standardized columns
        """
        pass

    def load_from_cache(self, cache_key: str) -> Optional[pd.DataFrame]:
        """Load previously cached data."""
        pass

    def merge_sources(
        self,
        sources: List[pd.DataFrame]
    ) -> pd.DataFrame:
        """Merge multiple data sources, removing duplicates."""
        pass

    def get_date_range(self, df: pd.DataFrame) -> Tuple[datetime, datetime]:
        """Get min and max dates from dataset."""
        pass
```

**Input**: CSV file path or cache key
**Output**: Standardized DataFrame

---

#### 2.1.3 `validator.py` - Data Validation

**Responsibility**: Validate data integrity and clean anomalies

**Main Classes**:
- `DataValidator`: Validation and cleaning logic

**Key Methods**:
```python
class DataValidator:
    """Validate and clean Euromillions data."""

    NUMBERS_RANGE = (1, 50)      # Valid range for main numbers
    STARS_RANGE = (1, 12)        # Valid range for star numbers
    REQUIRED_COLS = ['date', 'n1', 'n2', 'n3', 'n4', 'n5', 's1', 's2']

    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame has required columns."""
        pass

    def validate_ranges(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate number ranges and remove invalid rows.

        Returns:
            Cleaned DataFrame with only valid draws
        """
        pass

    def check_duplicates(self, df: pd.DataFrame) -> List[int]:
        """Identify duplicate draw dates."""
        pass

    def remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Remove duplicate entries, keeping most recent."""
        pass

    def validate_date_sequence(self, df: pd.DataFrame) -> bool:
        """Check for gaps in date sequence."""
        pass

    def generate_validation_report(
        self,
        df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Generate comprehensive validation report.

        Returns:
            {
                'total_rows': int,
                'valid_rows': int,
                'duplicates': int,
                'invalid_numbers': int,
                'date_gaps': List[Tuple[datetime, datetime]]
            }
        """
        pass
```

**Input**: Raw DataFrame
**Output**: Validated and cleaned DataFrame + validation report

---

### 2.2 Features Module (`euromillions_ml/features/`)

#### 2.2.1 `engineering.py` - Feature Engineering

**Responsibility**: Transform raw draws into ML-ready features

**Main Classes**:
- `FeatureEngineer`: Feature extraction and transformation

**Key Methods**:
```python
class FeatureEngineer:
    """Extract features from historical draw data."""

    def __init__(self, lookback_window: int = 50):
        """
        Initialize feature engineer.

        Args:
            lookback_window: Number of past draws to consider
        """
        self.lookback_window = lookback_window

    def extract_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract all feature types.

        Returns:
            Feature matrix with columns for each feature type
        """
        features = pd.DataFrame()
        features = pd.concat([
            features,
            self.frequency_features(df),
            self.pattern_features(df),
            self.statistical_features(df),
            self.temporal_features(df),
            self.pair_correlation_features(df)
        ], axis=1)
        return features

    def frequency_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate frequency-based features.

        Features:
        - Number frequency (last N draws)
        - Star frequency (last N draws)
        - Hot/cold number indicators
        - Overdue number counts
        """
        pass

    def pattern_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect pattern-based features.

        Features:
        - Consecutive number count
        - Even/odd ratio
        - High/low ratio (1-25 vs 26-50)
        - Sum of numbers
        - Number spread (max - min)
        """
        pass

    def statistical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate statistical features.

        Features:
        - Mean, median, std of draw numbers
        - Skewness and kurtosis
        - Quartile distributions
        """
        pass

    def temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Time-based features.

        Features:
        - Day of week
        - Month
        - Quarter
        - Days since last appearance (per number)
        """
        pass

    def pair_correlation_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Number pair correlation features.

        Features:
        - Frequently paired numbers
        - Rarely paired numbers
        - Pair frequency matrix
        """
        pass

    def create_sequences(
        self,
        features: pd.DataFrame,
        sequence_length: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for LSTM training.

        Args:
            features: Feature matrix
            sequence_length: Length of input sequences

        Returns:
            (X_sequences, y_targets) for LSTM
        """
        pass
```

**Input**: Historical draws DataFrame
**Output**: Feature matrix (n_samples, n_features)

---

#### 2.2.2 `normalizer.py` - Data Normalization

**Responsibility**: Scale and normalize features for ML models

**Main Classes**:
- `FeatureNormalizer`: Normalization and scaling

**Key Methods**:
```python
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from typing import Literal

class FeatureNormalizer:
    """Normalize features for ML models."""

    def __init__(
        self,
        method: Literal['minmax', 'standard'] = 'minmax'
    ):
        """
        Initialize normalizer.

        Args:
            method: 'minmax' for [0,1] scaling or 'standard' for z-score
        """
        self.method = method
        self.scaler = MinMaxScaler() if method == 'minmax' else StandardScaler()
        self.fitted = False

    def fit(self, X: np.ndarray) -> 'FeatureNormalizer':
        """Fit scaler on training data."""
        self.scaler.fit(X)
        self.fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform features using fitted scaler."""
        if not self.fitted:
            raise ValueError("Normalizer must be fitted before transform")
        return self.scaler.transform(X)

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform in one step."""
        return self.fit(X).transform(X)

    def inverse_transform(self, X_scaled: np.ndarray) -> np.ndarray:
        """Reverse normalization."""
        return self.scaler.inverse_transform(X_scaled)

    def save_scaler(self, filepath: str):
        """Save fitted scaler to disk."""
        import joblib
        joblib.dump(self.scaler, filepath)

    def load_scaler(self, filepath: str):
        """Load fitted scaler from disk."""
        import joblib
        self.scaler = joblib.load(filepath)
        self.fitted = True
```

**Input**: Raw feature matrix
**Output**: Normalized feature matrix

---

### 2.3 Models Module (`euromillions_ml/models/`)

#### 2.3.1 `base.py` - Base Model Interface

**Responsibility**: Abstract base class for all models

**Main Classes**:
```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """Abstract base class for prediction models."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.is_trained = False

    @abstractmethod
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """Train the model. Returns training metrics."""
        pass

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions on input data."""
        pass

    @abstractmethod
    def save_model(self, filepath: str):
        """Save trained model to disk."""
        pass

    @abstractmethod
    def load_model(self, filepath: str):
        """Load trained model from disk."""
        pass

    def predict_draw(
        self,
        X: np.ndarray,
        n_numbers: int = 5,
        n_stars: int = 2
    ) -> Dict[str, List[int]]:
        """
        Predict a complete Euromillions draw.

        Returns:
            {'numbers': [n1, n2, n3, n4, n5], 'stars': [s1, s2]}
        """
        pass
```

---

#### 2.3.2 `lstm.py` - LSTM Neural Network

**Responsibility**: Deep learning time-series prediction using LSTM

**Main Classes**:
- `LSTMModel`: LSTM neural network implementation

**Key Methods**:
```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class LSTMModel(BaseModel):
    """LSTM model for sequence prediction."""

    def __init__(
        self,
        sequence_length: int = 10,
        n_features: int = 100,
        lstm_units: List[int] = [128, 64],
        dropout_rate: float = 0.2
    ):
        super().__init__("LSTM")
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.model = self._build_model()

    def _build_model(self) -> keras.Model:
        """
        Build LSTM architecture.

        Architecture:
        - Input: (sequence_length, n_features)
        - LSTM layers with dropout
        - Dense output layers for numbers and stars
        """
        inputs = layers.Input(shape=(self.sequence_length, self.n_features))

        x = inputs
        for i, units in enumerate(self.lstm_units):
            return_sequences = (i < len(self.lstm_units) - 1)
            x = layers.LSTM(
                units,
                return_sequences=return_sequences,
                name=f'lstm_{i+1}'
            )(x)
            x = layers.Dropout(self.dropout_rate)(x)

        # Separate heads for numbers and stars
        numbers_out = layers.Dense(50, activation='softmax', name='numbers')(x)
        stars_out = layers.Dense(12, activation='softmax', name='stars')(x)

        model = keras.Model(inputs=inputs, outputs=[numbers_out, stars_out])
        return model

    def train(
        self,
        X_train: np.ndarray,
        y_train: Tuple[np.ndarray, np.ndarray],  # (numbers, stars)
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        epochs: int = 100,
        batch_size: int = 32
    ) -> Dict[str, Any]:
        """
        Train LSTM model.

        Returns:
            Training history with loss and accuracy metrics
        """
        self.model.compile(
            optimizer='adam',
            loss={
                'numbers': 'sparse_categorical_crossentropy',
                'stars': 'sparse_categorical_crossentropy'
            },
            metrics=['accuracy']
        )

        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5
            )
        ]

        history = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val) if X_val is not None else None,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )

        self.is_trained = True
        return history.history

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict probabilities for numbers and stars."""
        return self.model.predict(X)

    def save_model(self, filepath: str):
        """Save model weights and architecture."""
        self.model.save(filepath)

    def load_model(self, filepath: str):
        """Load model from disk."""
        self.model = keras.models.load_model(filepath)
        self.is_trained = True
```

**Input**: 3D sequences (n_samples, sequence_length, n_features)
**Output**: Probability distributions for numbers and stars

---

#### 2.3.3 `random_forest.py` - Random Forest

**Responsibility**: Ensemble tree-based prediction

**Main Classes**:
- `RandomForestModel`: Random Forest classifier

**Key Methods**:
```python
from sklearn.ensemble import RandomForestClassifier
import joblib

class RandomForestModel(BaseModel):
    """Random Forest model for lottery prediction."""

    def __init__(
        self,
        n_estimators: int = 200,
        max_depth: Optional[int] = 20,
        min_samples_split: int = 5,
        n_jobs: int = -1
    ):
        super().__init__("RandomForest")
        self.model_numbers = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            n_jobs=n_jobs,
            random_state=42
        )
        self.model_stars = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            n_jobs=n_jobs,
            random_state=42
        )

    def train(
        self,
        X_train: np.ndarray,
        y_train: Tuple[np.ndarray, np.ndarray],
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[Tuple[np.ndarray, np.ndarray]] = None
    ) -> Dict[str, Any]:
        """
        Train separate Random Forests for numbers and stars.

        Returns:
            Training metrics including feature importance
        """
        y_numbers, y_stars = y_train

        # Train numbers model
        self.model_numbers.fit(X_train, y_numbers)

        # Train stars model
        self.model_stars.fit(X_train, y_stars)

        self.is_trained = True

        metrics = {
            'numbers_score': self.model_numbers.score(X_train, y_numbers),
            'stars_score': self.model_stars.score(X_train, y_stars),
            'feature_importance': self.model_numbers.feature_importances_
        }

        if X_val is not None and y_val is not None:
            y_val_numbers, y_val_stars = y_val
            metrics['val_numbers_score'] = self.model_numbers.score(X_val, y_val_numbers)
            metrics['val_stars_score'] = self.model_stars.score(X_val, y_val_stars)

        return metrics

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict probabilities for numbers and stars."""
        numbers_proba = self.model_numbers.predict_proba(X)
        stars_proba = self.model_stars.predict_proba(X)
        return numbers_proba, stars_proba

    def save_model(self, filepath: str):
        """Save models to disk."""
        joblib.dump({
            'numbers': self.model_numbers,
            'stars': self.model_stars
        }, filepath)

    def load_model(self, filepath: str):
        """Load models from disk."""
        models = joblib.load(filepath)
        self.model_numbers = models['numbers']
        self.model_stars = models['stars']
        self.is_trained = True
```

**Input**: 2D feature matrix (n_samples, n_features)
**Output**: Probability distributions

---

#### 2.3.4 `markov.py` - Markov Chain Model

**Responsibility**: Transition probability modeling

**Main Classes**:
- `MarkovModel`: Markov chain based prediction

**Key Methods**:
```python
class MarkovModel(BaseModel):
    """Markov Chain model for lottery prediction."""

    def __init__(self, order: int = 1):
        """
        Initialize Markov model.

        Args:
            order: Order of Markov chain (1=first-order, 2=second-order)
        """
        super().__init__("Markov")
        self.order = order
        self.transition_matrix_numbers = None
        self.transition_matrix_stars = None
        self.state_counts = None

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Build transition probability matrices.

        Returns:
            Statistics about transition probabilities
        """
        # Build transition matrices from historical sequences
        self.transition_matrix_numbers = self._build_transition_matrix(
            y_train,
            n_states=50
        )
        self.transition_matrix_stars = self._build_transition_matrix(
            y_train,
            n_states=12
        )

        self.is_trained = True
        return {'transition_matrix_built': True}

    def _build_transition_matrix(
        self,
        sequences: np.ndarray,
        n_states: int
    ) -> np.ndarray:
        """
        Build transition probability matrix.

        Returns:
            Matrix of shape (n_states, n_states) with probabilities
        """
        matrix = np.zeros((n_states, n_states))

        for seq in sequences:
            for i in range(len(seq) - 1):
                current = seq[i] - 1  # 0-indexed
                next_state = seq[i + 1] - 1
                matrix[current][next_state] += 1

        # Normalize to probabilities
        row_sums = matrix.sum(axis=1, keepdims=True)
        matrix = np.divide(matrix, row_sums, where=row_sums != 0)

        return matrix

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Predict using transition probabilities."""
        # Use last state to predict next state probabilities
        numbers_proba = self.transition_matrix_numbers
        stars_proba = self.transition_matrix_stars
        return numbers_proba, stars_proba

    def save_model(self, filepath: str):
        """Save transition matrices."""
        np.savez(
            filepath,
            numbers=self.transition_matrix_numbers,
            stars=self.transition_matrix_stars,
            order=self.order
        )

    def load_model(self, filepath: str):
        """Load transition matrices."""
        data = np.load(filepath)
        self.transition_matrix_numbers = data['numbers']
        self.transition_matrix_stars = data['stars']
        self.order = int(data['order'])
        self.is_trained = True
```

**Input**: Historical draw sequences
**Output**: Transition probability matrices

---

#### 2.3.5 `hybrid.py` - Hybrid Ensemble Model

**Responsibility**: Combine predictions from multiple models

**Main Classes**:
- `HybridModel`: Ensemble fusion of all models

**Key Methods**:
```python
class HybridModel(BaseModel):
    """Hybrid ensemble combining multiple models."""

    def __init__(
        self,
        models: List[BaseModel],
        weights: Optional[List[float]] = None
    ):
        """
        Initialize hybrid model.

        Args:
            models: List of trained models
            weights: Optional weights for each model (auto if None)
        """
        super().__init__("Hybrid")
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Train all sub-models and optimize weights.

        Returns:
            Combined training metrics
        """
        metrics = {}

        for i, model in enumerate(self.models):
            print(f"Training {model.model_name}...")
            model_metrics = model.train(X_train, y_train, X_val, y_val)
            metrics[model.model_name] = model_metrics

        # Optimize weights based on validation performance
        if X_val is not None and y_val is not None:
            self.weights = self._optimize_weights(X_val, y_val)

        self.is_trained = True
        return metrics

    def _optimize_weights(
        self,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> List[float]:
        """
        Optimize model weights using validation set.

        Uses grid search to find best weight combination
        """
        # Simple approach: weight by validation accuracy
        scores = []
        for model in self.models:
            pred = model.predict(X_val)
            score = self._calculate_accuracy(pred, y_val)
            scores.append(score)

        # Normalize scores to weights
        total = sum(scores)
        weights = [s / total for s in scores]
        return weights

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Combine predictions from all models using weights.

        Returns:
            Weighted average of probability distributions
        """
        all_numbers_proba = []
        all_stars_proba = []

        for model, weight in zip(self.models, self.weights):
            numbers_proba, stars_proba = model.predict(X)
            all_numbers_proba.append(numbers_proba * weight)
            all_stars_proba.append(stars_proba * weight)

        # Combine weighted predictions
        combined_numbers = np.sum(all_numbers_proba, axis=0)
        combined_stars = np.sum(all_stars_proba, axis=0)

        return combined_numbers, combined_stars

    def save_model(self, filepath: str):
        """Save all models and weights."""
        for i, model in enumerate(self.models):
            model.save_model(f"{filepath}_{model.model_name}")

        # Save weights
        np.save(f"{filepath}_weights.npy", self.weights)

    def load_model(self, filepath: str):
        """Load all models and weights."""
        for model in self.models:
            model.load_model(f"{filepath}_{model.model_name}")

        self.weights = np.load(f"{filepath}_weights.npy").tolist()
        self.is_trained = True
```

**Input**: Same as individual models
**Output**: Ensemble-averaged predictions

---

### 2.4 Prediction Module (`euromillions_ml/prediction/`)

#### 2.4.1 `predictor.py` - Prediction Engine

**Responsibility**: Generate predictions using trained models

**Main Classes**:
- `Predictor`: Main prediction interface

**Key Methods**:
```python
class Predictor:
    """Main prediction engine."""

    def __init__(
        self,
        model: BaseModel,
        feature_engineer: FeatureEngineer,
        normalizer: FeatureNormalizer
    ):
        self.model = model
        self.feature_engineer = feature_engineer
        self.normalizer = normalizer

    def predict_next_draw(
        self,
        historical_data: pd.DataFrame,
        n_predictions: int = 1
    ) -> List[Dict[str, List[int]]]:
        """
        Predict next draw(s).

        Args:
            historical_data: Recent draw history
            n_predictions: Number of draw predictions to generate

        Returns:
            List of predictions: [{'numbers': [...], 'stars': [...]}]
        """
        # Extract features
        features = self.feature_engineer.extract_all_features(historical_data)

        # Normalize
        X = self.normalizer.transform(features.values)

        # Predict
        numbers_proba, stars_proba = self.model.predict(X)

        # Convert probabilities to draw predictions
        predictions = []
        for _ in range(n_predictions):
            pred = self._proba_to_draw(numbers_proba, stars_proba)
            predictions.append(pred)

        return predictions

    def _proba_to_draw(
        self,
        numbers_proba: np.ndarray,
        stars_proba: np.ndarray
    ) -> Dict[str, List[int]]:
        """
        Convert probability distributions to a draw.

        Strategy: Top-K selection with diversity constraints
        """
        # Select top 5 numbers
        numbers_idx = np.argsort(numbers_proba[0])[-5:]
        numbers = sorted((numbers_idx + 1).tolist())

        # Select top 2 stars
        stars_idx = np.argsort(stars_proba[0])[-2:]
        stars = sorted((stars_idx + 1).tolist())

        return {'numbers': numbers, 'stars': stars}

    def batch_predict(
        self,
        historical_data: pd.DataFrame,
        n_draws: int = 10
    ) -> pd.DataFrame:
        """
        Generate batch predictions.

        Returns:
            DataFrame with predicted draws
        """
        predictions = self.predict_next_draw(historical_data, n_draws)
        return pd.DataFrame(predictions)
```

**Input**: Historical data
**Output**: Predicted draws

---

#### 2.4.2 `backtest.py` - Backtesting Framework

**Responsibility**: Evaluate model performance on historical data

**Main Classes**:
- `Backtester`: Backtesting engine

**Key Methods**:
```python
class Backtester:
    """Backtest model predictions against historical data."""

    def __init__(
        self,
        predictor: Predictor,
        metrics_calculator: 'MetricsCalculator'
    ):
        self.predictor = predictor
        self.metrics = metrics_calculator

    def run_backtest(
        self,
        data: pd.DataFrame,
        train_size: float = 0.8,
        window_size: int = 50
    ) -> Dict[str, Any]:
        """
        Run sliding window backtest.

        Args:
            data: Full historical dataset
            train_size: Proportion for initial training
            window_size: Size of training window

        Returns:
            Backtest results with metrics
        """
        split_idx = int(len(data) * train_size)

        results = []

        # Sliding window approach
        for i in range(split_idx, len(data)):
            # Training window
            train_data = data.iloc[max(0, i - window_size):i]

            # True draw
            true_draw = data.iloc[i]

            # Predict
            predictions = self.predictor.predict_next_draw(train_data, n_predictions=1)
            pred_draw = predictions[0]

            # Calculate metrics
            metrics = self.metrics.calculate_draw_metrics(
                pred_draw,
                true_draw
            )

            results.append({
                'date': true_draw['date'],
                'predicted': pred_draw,
                'actual': true_draw,
                'metrics': metrics
            })

        # Aggregate metrics
        return self._aggregate_results(results)

    def _aggregate_results(
        self,
        results: List[Dict]
    ) -> Dict[str, Any]:
        """
        Aggregate backtest results.

        Returns:
            {
                'total_draws': int,
                'avg_numbers_matched': float,
                'avg_stars_matched': float,
                'best_match': Dict,
                'distribution': Dict
            }
        """
        pass
```

**Input**: Historical data
**Output**: Backtest metrics and analysis

---

### 2.5 Utils Module (`euromillions_ml/utils/`)

#### 2.5.1 `display.py` - Terminal Display

**Responsibility**: Format and display results in terminal

**Main Classes**:
- `TerminalDisplay`: Terminal output formatting

**Key Methods**:
```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class TerminalDisplay:
    """Format output for terminal display."""

    def __init__(self):
        self.console = Console()

    def show_prediction(self, prediction: Dict[str, List[int]]):
        """Display prediction in formatted table."""
        table = Table(title="Euromillions Prediction")

        table.add_column("Type", style="cyan")
        table.add_column("Numbers", style="green")

        numbers_str = " - ".join(map(str, prediction['numbers']))
        stars_str = " - ".join(map(str, prediction['stars']))

        table.add_row("Numbers", numbers_str)
        table.add_row("Stars", stars_str)

        self.console.print(table)

    def show_backtest_results(self, results: Dict[str, Any]):
        """Display backtest results."""
        panel = Panel.fit(
            f"[bold]Backtest Results[/bold]\n\n"
            f"Total Draws: {results['total_draws']}\n"
            f"Avg Numbers Matched: {results['avg_numbers_matched']:.2f}\n"
            f"Avg Stars Matched: {results['avg_stars_matched']:.2f}",
            border_style="blue"
        )
        self.console.print(panel)

    def show_progress(self, current: int, total: int, message: str):
        """Display progress bar."""
        from rich.progress import Progress

        with Progress() as progress:
            task = progress.add_task(message, total=total)
            progress.update(task, completed=current)
```

---

#### 2.5.2 `metrics.py` - Performance Metrics

**Responsibility**: Calculate prediction accuracy metrics

**Main Classes**:
- `MetricsCalculator`: Metric computation

**Key Methods**:
```python
class MetricsCalculator:
    """Calculate prediction performance metrics."""

    def calculate_draw_metrics(
        self,
        predicted: Dict[str, List[int]],
        actual: pd.Series
    ) -> Dict[str, Any]:
        """
        Calculate metrics for a single draw prediction.

        Returns:
            {
                'numbers_matched': int,
                'stars_matched': int,
                'prize_tier': str,
                'accuracy_score': float
            }
        """
        actual_numbers = set([
            actual['n1'], actual['n2'], actual['n3'],
            actual['n4'], actual['n5']
        ])
        actual_stars = set([actual['s1'], actual['s2']])

        pred_numbers = set(predicted['numbers'])
        pred_stars = set(predicted['stars'])

        numbers_matched = len(pred_numbers & actual_numbers)
        stars_matched = len(pred_stars & actual_stars)

        prize_tier = self._determine_prize_tier(numbers_matched, stars_matched)

        accuracy = (numbers_matched / 5.0 + stars_matched / 2.0) / 2.0

        return {
            'numbers_matched': numbers_matched,
            'stars_matched': stars_matched,
            'prize_tier': prize_tier,
            'accuracy_score': accuracy
        }

    def _determine_prize_tier(
        self,
        numbers: int,
        stars: int
    ) -> str:
        """
        Determine Euromillions prize tier.

        Tiers:
        - 1: 5 numbers + 2 stars
        - 2: 5 numbers + 1 star
        - 3: 5 numbers + 0 stars
        - ...
        """
        if numbers == 5 and stars == 2:
            return "Tier 1 (Jackpot)"
        elif numbers == 5 and stars == 1:
            return "Tier 2"
        elif numbers == 5 and stars == 0:
            return "Tier 3"
        elif numbers == 4 and stars == 2:
            return "Tier 4"
        # ... more tiers
        else:
            return "No prize"

    def calculate_aggregate_metrics(
        self,
        all_metrics: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Calculate aggregate metrics across multiple predictions.

        Returns:
            {
                'avg_numbers_matched': float,
                'avg_stars_matched': float,
                'avg_accuracy': float,
                'prize_distribution': Dict[str, int]
            }
        """
        pass
```

---

## 3. Technical Stack

### Core Technologies

**Python Version**: 3.9+

**Machine Learning Libraries**:
- `tensorflow>=2.13.0` - Deep learning framework for LSTM
- `keras>=2.13.0` - High-level neural network API
- `scikit-learn>=1.3.0` - Traditional ML algorithms (Random Forest)
- `numpy>=1.24.0` - Numerical computing
- `pandas>=2.0.0` - Data manipulation

**Web Scraping**:
- `beautifulsoup4>=4.12.0` - HTML parsing
- `requests>=2.31.0` - HTTP requests
- `lxml>=4.9.0` - XML/HTML parser

**Data Processing**:
- `scipy>=1.11.0` - Scientific computing
- `joblib>=1.3.0` - Model serialization

**Visualization & CLI**:
- `rich>=13.5.0` - Terminal formatting
- `matplotlib>=3.7.0` - Plotting (optional)
- `seaborn>=0.12.0` - Statistical visualization (optional)

**Configuration & Utilities**:
- `pyyaml>=6.0` - YAML configuration
- `python-dotenv>=1.0.0` - Environment variables
- `argparse` - CLI argument parsing (built-in)

**Testing**:
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting

**Development**:
- `black>=23.7.0` - Code formatting
- `flake8>=6.1.0` - Linting
- `mypy>=1.5.0` - Type checking

---

## 4. Data Architecture

### Raw Data Format

**CSV Schema**:
```
date,n1,n2,n3,n4,n5,s1,s2
2024-01-05,7,23,34,42,48,3,9
2024-01-02,12,18,29,35,47,2,11
...
```

**DataFrame Structure**:
```python
pd.DataFrame({
    'date': pd.DatetimeIndex,  # Draw date
    'n1': int,                 # Number 1 (1-50)
    'n2': int,                 # Number 2 (1-50)
    'n3': int,                 # Number 3 (1-50)
    'n4': int,                 # Number 4 (1-50)
    'n5': int,                 # Number 5 (1-50)
    's1': int,                 # Star 1 (1-12)
    's2': int                  # Star 2 (1-12)
})
```

### Feature Engineering Schema

**Feature Categories**:

1. **Frequency Features** (120 features):
   - `num_freq_1` to `num_freq_50`: Frequency of each number in last N draws
   - `star_freq_1` to `star_freq_12`: Frequency of each star
   - `num_hot_1` to `num_hot_10`: Top 10 hot numbers
   - `num_cold_1` to `num_cold_10`: Top 10 cold numbers
   - `num_overdue_1` to `num_overdue_50`: Days since last appearance

2. **Pattern Features** (15 features):
   - `consecutive_count`: Count of consecutive numbers
   - `even_count`: Count of even numbers
   - `odd_count`: Count of odd numbers
   - `high_count`: Count of numbers > 25
   - `low_count`: Count of numbers <= 25
   - `sum_numbers`: Sum of all numbers
   - `range_numbers`: max - min
   - `mean_numbers`: Average value
   - `median_numbers`: Median value
   - `std_numbers`: Standard deviation

3. **Statistical Features** (8 features):
   - `skewness`: Distribution skewness
   - `kurtosis`: Distribution kurtosis
   - `q1`, `q2`, `q3`: Quartiles
   - `iqr`: Interquartile range

4. **Temporal Features** (10 features):
   - `day_of_week`: 0-6 (Monday-Sunday)
   - `month`: 1-12
   - `quarter`: 1-4
   - `days_since_last`: Days since previous draw

5. **Correlation Features** (50 features):
   - `pair_freq_1_2` to `pair_freq_49_50`: Pair occurrence frequencies

**Total Features**: ~200-300 depending on configuration

### ML Dataset Structure

**Training Data (X, y)**:

```python
# For LSTM
X_lstm: np.ndarray  # Shape: (n_samples, sequence_length, n_features)
y_lstm: Tuple[
    np.ndarray,  # Numbers shape: (n_samples, 5)
    np.ndarray   # Stars shape: (n_samples, 2)
]

# For RandomForest/Markov
X_flat: np.ndarray  # Shape: (n_samples, n_features)
y_numbers: np.ndarray  # Shape: (n_samples, 5)
y_stars: np.ndarray    # Shape: (n_samples, 2)
```

**Data Split**:
- Training: 80%
- Validation: 10%
- Test: 10%

---

## 5. ML Pipeline

### Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. DATA ACQUISITION                                             │
├─────────────────────────────────────────────────────────────────┤
│ IF web_scraping_enabled:                                        │
│     data = FDJScraper().fetch_historical_data(start, end)       │
│ ELSE:                                                           │
│     data = DataLoader().load_csv(filepath)                      │
│ data.to_csv("data/cache/historical.csv")                       │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. DATA VALIDATION                                              │
├─────────────────────────────────────────────────────────────────┤
│ validator = DataValidator()                                     │
│ IF NOT validator.validate_schema(data):                         │
│     RAISE ValidationError("Invalid schema")                     │
│ data = validator.validate_ranges(data)                          │
│ data = validator.remove_duplicates(data)                        │
│ report = validator.generate_validation_report(data)             │
│ LOG.info(report)                                                │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. FEATURE ENGINEERING                                          │
├─────────────────────────────────────────────────────────────────┤
│ engineer = FeatureEngineer(lookback_window=50)                  │
│ features = engineer.extract_all_features(data)                  │
│   ├─ freq_features = frequency_features(data)                   │
│   ├─ pattern_features = pattern_features(data)                  │
│   ├─ stat_features = statistical_features(data)                 │
│   ├─ temporal_features = temporal_features(data)                │
│   └─ corr_features = pair_correlation_features(data)            │
│ features.to_csv("data/features/engineered.csv")                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. DATA NORMALIZATION                                           │
├─────────────────────────────────────────────────────────────────┤
│ normalizer = FeatureNormalizer(method='minmax')                 │
│ X_normalized = normalizer.fit_transform(features.values)        │
│ normalizer.save_scaler("models/scaler.pkl")                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. TRAIN-TEST SPLIT                                             │
├─────────────────────────────────────────────────────────────────┤
│ FROM sklearn.model_selection IMPORT train_test_split            │
│ X_train, X_temp, y_train, y_temp = train_test_split(            │
│     X_normalized, y, test_size=0.2, shuffle=False               │
│ )                                                               │
│ X_val, X_test, y_val, y_test = train_test_split(                │
│     X_temp, y_temp, test_size=0.5, shuffle=False                │
│ )                                                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. MODEL SELECTION & INITIALIZATION                             │
├─────────────────────────────────────────────────────────────────┤
│ IF model_type == "lstm":                                        │
│     model = LSTMModel(sequence_length=10, n_features=X.shape[1])│
│ ELIF model_type == "random_forest":                             │
│     model = RandomForestModel(n_estimators=200)                 │
│ ELIF model_type == "markov":                                    │
│     model = MarkovModel(order=1)                                │
│ ELIF model_type == "hybrid":                                    │
│     lstm = LSTMModel(...)                                       │
│     rf = RandomForestModel(...)                                 │
│     markov = MarkovModel(...)                                   │
│     model = HybridModel([lstm, rf, markov])                     │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 7. MODEL TRAINING                                               │
├─────────────────────────────────────────────────────────────────┤
│ LOG.info(f"Training {model.model_name}...")                     │
│ history = model.train(                                          │
│     X_train, y_train,                                           │
│     X_val, y_val,                                               │
│     epochs=100,                                                 │
│     batch_size=32                                               │
│ )                                                               │
│ model.save_model(f"models/{model.model_name}_trained.h5")       │
│ LOG.info("Training complete")                                   │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 8. PREDICTION                                                   │
├─────────────────────────────────────────────────────────────────┤
│ predictor = Predictor(model, engineer, normalizer)              │
│ predictions = predictor.predict_next_draw(                      │
│     historical_data=data,                                       │
│     n_predictions=config.n_predictions                          │
│ )                                                               │
│ FOR pred IN predictions:                                        │
│     LOG.info(f"Numbers: {pred['numbers']}")                     │
│     LOG.info(f"Stars: {pred['stars']}")                         │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 9. VALIDATION (BACKTEST MODE)                                   │
├─────────────────────────────────────────────────────────────────┤
│ IF mode == "backtest":                                          │
│     backtester = Backtester(predictor, MetricsCalculator())     │
│     results = backtester.run_backtest(                          │
│         data=data,                                              │
│         train_size=0.8,                                         │
│         window_size=50                                          │
│     )                                                           │
│     display.show_backtest_results(results)                      │
│     results.to_csv("results/backtest_results.csv")              │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ 10. OUTPUT                                                      │
├─────────────────────────────────────────────────────────────────┤
│ display = TerminalDisplay()                                     │
│ FOR prediction IN predictions:                                  │
│     display.show_prediction(prediction)                         │
│                                                                 │
│ IF export_format:                                               │
│     pd.DataFrame(predictions).to_csv("results/predictions.csv") │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. API/Interface Design

### CLI Interface

**Main Entry Point**: `main.py`

```python
import argparse
from euromillions_ml import Predictor, Backtester

def main():
    parser = argparse.ArgumentParser(
        description="Euromillions ML Predictor"
    )

    # Mode selection
    parser.add_argument(
        '--mode',
        choices=['predict', 'backtest', 'train'],
        default='predict',
        help='Operating mode'
    )

    # Model selection
    parser.add_argument(
        '--model',
        choices=['lstm', 'random_forest', 'markov', 'hybrid'],
        default='hybrid',
        help='Model to use'
    )

    # Data source
    parser.add_argument(
        '--data-source',
        choices=['scrape', 'csv'],
        default='csv',
        help='Data source'
    )

    parser.add_argument(
        '--csv-path',
        type=str,
        default='data/historical.csv',
        help='Path to CSV file'
    )

    # Prediction parameters
    parser.add_argument(
        '--n-predictions',
        type=int,
        default=1,
        help='Number of predictions to generate'
    )

    # Training parameters
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help='Number of training epochs'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Training batch size'
    )

    # Output options
    parser.add_argument(
        '--export',
        choices=['csv', 'json', 'none'],
        default='none',
        help='Export format'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='results/predictions.csv',
        help='Output file path'
    )

    # Logging
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level'
    )

    args = parser.parse_args()

    # Execute based on mode
    if args.mode == 'predict':
        run_prediction(args)
    elif args.mode == 'backtest':
        run_backtest(args)
    elif args.mode == 'train':
        run_training(args)

if __name__ == '__main__':
    main()
```

**Usage Examples**:

```bash
# Generate single prediction using hybrid model
python main.py --mode predict --model hybrid --n-predictions 1

# Run backtest with LSTM
python main.py --mode backtest --model lstm --data-source csv

# Train Random Forest and export predictions
python main.py --mode train --model random_forest --epochs 50 --export csv

# Scrape latest data and predict
python main.py --mode predict --data-source scrape --n-predictions 5
```

### Configuration File

**config.yaml**:

```yaml
# Data Configuration
data:
  source: "csv"  # "csv" or "scrape"
  csv_path: "data/historical.csv"
  cache_dir: "data/cache"
  scraper:
    base_url: "https://www.fdj.fr/jeux-de-tirage/euromillions-my-million"
    timeout: 30
    retry_attempts: 3

# Feature Engineering
features:
  lookback_window: 50
  include_frequency: true
  include_patterns: true
  include_statistics: true
  include_temporal: true
  include_correlations: true

# Model Configuration
models:
  lstm:
    sequence_length: 10
    lstm_units: [128, 64]
    dropout_rate: 0.2
    epochs: 100
    batch_size: 32

  random_forest:
    n_estimators: 200
    max_depth: 20
    min_samples_split: 5

  markov:
    order: 1

  hybrid:
    weights: null  # Auto-optimize if null

# Training Configuration
training:
  train_split: 0.8
  val_split: 0.1
  test_split: 0.1
  shuffle: false
  random_state: 42

# Prediction Configuration
prediction:
  n_predictions: 1
  strategy: "top_k"  # "top_k" or "sampling"
  diversity_constraint: true

# Backtest Configuration
backtest:
  window_size: 50
  step_size: 1

# Output Configuration
output:
  export_format: "csv"
  output_dir: "results"
  display_format: "rich"  # "rich" or "plain"

# Logging
logging:
  level: "INFO"
  file: "logs/euromillions_ml.log"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

---

## 7. Error Handling & Logging

### Error Handling Strategy

**Custom Exceptions**:

```python
# euromillions_ml/utils/exceptions.py

class EuromillionsMLError(Exception):
    """Base exception for Euromillions ML."""
    pass

class DataValidationError(EuromillionsMLError):
    """Raised when data validation fails."""
    pass

class ScraperError(EuromillionsMLError):
    """Raised when web scraping fails."""
    pass

class ModelNotTrainedError(EuromillionsMLError):
    """Raised when attempting to use untrained model."""
    pass

class FeatureEngineeringError(EuromillionsMLError):
    """Raised when feature extraction fails."""
    pass
```

**Error Handling Pattern**:

```python
import logging
from euromillions_ml.utils.exceptions import ScraperError

logger = logging.getLogger(__name__)

def fetch_data_with_fallback(scraper, loader, config):
    """Fetch data with automatic fallback to CSV."""
    try:
        # Try scraping
        logger.info("Attempting to scrape data from FDJ...")
        data = scraper.fetch_historical_data(
            config['start_date'],
            config['end_date']
        )
        logger.info(f"Successfully scraped {len(data)} draws")
        return data

    except ScraperError as e:
        logger.warning(f"Scraping failed: {e}")
        logger.info("Falling back to CSV data source...")

        try:
            data = loader.load_csv(config['csv_path'])
            logger.info(f"Loaded {len(data)} draws from CSV")
            return data

        except FileNotFoundError as e:
            logger.error(f"CSV file not found: {e}")
            raise DataValidationError(
                "No data source available. Please provide valid CSV or fix scraper."
            )

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise
```

### Logging Configuration

```python
# euromillions_ml/utils/logging_config.py

import logging
import logging.handlers
from pathlib import Path

def setup_logging(config: dict):
    """Configure logging for the application."""

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(config['level'])

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(config['level'])
    console_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # File handler (rotating)
    file_handler = logging.handlers.RotatingFileHandler(
        config['file'],
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)  # Always DEBUG in file
    file_formatter = logging.Formatter(config['format'])
    file_handler.setFormatter(file_formatter)

    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Suppress verbose libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('tensorflow').setLevel(logging.WARNING)

    return logger
```

**Logging Levels**:

- `DEBUG`: Detailed information for debugging (feature values, model internals)
- `INFO`: General information (training progress, predictions)
- `WARNING`: Warning messages (fallback to CSV, missing data)
- `ERROR`: Error messages (validation failures, model errors)

---

## 8. Performance Considerations

### Optimization Strategies

#### 8.1 NumPy Vectorization

```python
# BAD: Python loops
def calculate_frequencies_slow(draws):
    frequencies = {}
    for draw in draws:
        for number in draw:
            frequencies[number] = frequencies.get(number, 0) + 1
    return frequencies

# GOOD: NumPy vectorization
def calculate_frequencies_fast(draws: np.ndarray):
    """10-100x faster using NumPy."""
    unique, counts = np.unique(draws.flatten(), return_counts=True)
    return dict(zip(unique, counts))
```

#### 8.2 Batch Processing

```python
class Predictor:
    def batch_predict(self, data: pd.DataFrame, batch_size: int = 100):
        """Process predictions in batches to reduce memory usage."""
        n_samples = len(data)
        predictions = []

        for i in range(0, n_samples, batch_size):
            batch = data.iloc[i:i+batch_size]
            batch_preds = self._predict_batch(batch)
            predictions.extend(batch_preds)

        return predictions
```

#### 8.3 Data Caching

```python
import hashlib
import pickle
from pathlib import Path

class CacheManager:
    """Cache expensive computations."""

    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_str = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, key: str):
        """Retrieve from cache."""
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    def set(self, key: str, value):
        """Store in cache."""
        cache_file = self.cache_dir / f"{key}.pkl"
        with open(cache_file, 'wb') as f:
            pickle.dump(value, f)

# Usage
cache = CacheManager()

def extract_features(data: pd.DataFrame):
    cache_key = cache.get_cache_key(data.shape, data.iloc[0]['date'])

    # Check cache
    features = cache.get(cache_key)
    if features is not None:
        logger.info("Loading features from cache")
        return features

    # Compute features
    logger.info("Computing features...")
    features = engineer.extract_all_features(data)

    # Cache results
    cache.set(cache_key, features)
    return features
```

#### 8.4 GPU Acceleration (LSTM)

```python
import tensorflow as tf

def configure_gpu():
    """Configure TensorFlow for GPU usage."""
    gpus = tf.config.list_physical_devices('GPU')

    if gpus:
        try:
            # Enable memory growth
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)

            logger.info(f"Using GPU: {gpus}")
            return True
        except RuntimeError as e:
            logger.warning(f"GPU configuration failed: {e}")
            return False
    else:
        logger.info("No GPU detected, using CPU")
        return False

# In LSTMModel.__init__
if configure_gpu():
    self.device = '/GPU:0'
else:
    self.device = '/CPU:0'

with tf.device(self.device):
    self.model = self._build_model()
```

#### 8.5 Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
from functools import partial

def process_draw(draw_data, feature_engineer):
    """Process single draw features."""
    return feature_engineer.extract_all_features(draw_data)

def parallel_feature_extraction(data: pd.DataFrame, n_workers: int = 4):
    """Extract features in parallel."""
    draws = np.array_split(data, n_workers)

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        feature_fn = partial(process_draw, feature_engineer=engineer)
        results = list(executor.map(feature_fn, draws))

    return pd.concat(results, ignore_index=True)
```

### Performance Benchmarks

**Target Performance**:
- Data loading: < 1 second for 1000 draws
- Feature extraction: < 5 seconds for 1000 draws
- LSTM training: < 10 minutes (100 epochs, GPU)
- Random Forest training: < 2 minutes
- Prediction: < 0.1 seconds per draw
- Backtest (1000 draws): < 5 minutes

---

## 9. Code Quality Standards

### PEP 8 Compliance

**Tools**:
- `black`: Auto-formatter
- `flake8`: Linter
- `isort`: Import sorting

**Configuration** (`.flake8`):
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git, __pycache__, venv
```

**Configuration** (`pyproject.toml`):
```toml
[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
line_length = 88
```

### Type Hints

**All functions must include type hints**:

```python
from typing import List, Dict, Tuple, Optional, Union
import numpy as np
import pandas as pd

def calculate_frequencies(
    draws: pd.DataFrame,
    lookback_window: int = 50,
    number_range: Tuple[int, int] = (1, 50)
) -> Dict[int, float]:
    """
    Calculate number frequencies.

    Args:
        draws: Historical draw data
        lookback_window: Number of past draws to consider
        number_range: Valid range for numbers

    Returns:
        Dictionary mapping number to frequency

    Raises:
        ValueError: If draws is empty or invalid
    """
    if draws.empty:
        raise ValueError("Draw data cannot be empty")

    # Implementation...
    return frequencies
```

### Docstrings (Google Style)

```python
class FeatureEngineer:
    """Extract ML features from lottery draw data.

    This class implements various feature extraction strategies including
    frequency analysis, pattern detection, and statistical measures.

    Attributes:
        lookback_window: Number of historical draws to analyze
        cache_dir: Directory for caching computed features

    Example:
        >>> engineer = FeatureEngineer(lookback_window=50)
        >>> features = engineer.extract_all_features(draws_df)
        >>> print(features.shape)
        (1000, 250)
    """

    def __init__(self, lookback_window: int = 50):
        """Initialize feature engineer.

        Args:
            lookback_window: Number of past draws to consider for features.
                Must be >= 10 for meaningful statistics.

        Raises:
            ValueError: If lookback_window < 10
        """
        if lookback_window < 10:
            raise ValueError("lookback_window must be >= 10")

        self.lookback_window = lookback_window
```

### Testing Strategy

**Test Structure**:

```
tests/
├── __init__.py
├── conftest.py                 # Pytest fixtures
├── test_data/
│   ├── test_scraper.py
│   ├── test_loader.py
│   └── test_validator.py
├── test_features/
│   ├── test_engineering.py
│   └── test_normalizer.py
├── test_models/
│   ├── test_lstm.py
│   ├── test_random_forest.py
│   ├── test_markov.py
│   └── test_hybrid.py
├── test_prediction/
│   ├── test_predictor.py
│   └── test_backtest.py
└── test_utils/
    ├── test_display.py
    └── test_metrics.py
```

**Example Unit Test**:

```python
# tests/test_features/test_engineering.py

import pytest
import pandas as pd
import numpy as np
from euromillions_ml.features.engineering import FeatureEngineer

@pytest.fixture
def sample_draws():
    """Create sample draw data for testing."""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100, freq='3D'),
        'n1': np.random.randint(1, 51, 100),
        'n2': np.random.randint(1, 51, 100),
        'n3': np.random.randint(1, 51, 100),
        'n4': np.random.randint(1, 51, 100),
        'n5': np.random.randint(1, 51, 100),
        's1': np.random.randint(1, 13, 100),
        's2': np.random.randint(1, 13, 100),
    })

def test_frequency_features_shape(sample_draws):
    """Test frequency features output shape."""
    engineer = FeatureEngineer(lookback_window=50)
    features = engineer.frequency_features(sample_draws)

    assert features.shape[0] == len(sample_draws)
    assert features.shape[1] > 0  # Has features

def test_frequency_features_range(sample_draws):
    """Test frequency values are in valid range."""
    engineer = FeatureEngineer(lookback_window=50)
    features = engineer.frequency_features(sample_draws)

    # Frequencies should be between 0 and 1
    assert (features >= 0).all().all()
    assert (features <= 1).all().all()

def test_feature_engineer_empty_data():
    """Test error handling for empty data."""
    engineer = FeatureEngineer()
    empty_df = pd.DataFrame()

    with pytest.raises(ValueError, match="empty"):
        engineer.extract_all_features(empty_df)
```

**Integration Test**:

```python
# tests/test_integration.py

def test_full_pipeline():
    """Test complete prediction pipeline."""
    # Load data
    loader = DataLoader()
    data = loader.load_csv("tests/fixtures/sample_data.csv")

    # Validate
    validator = DataValidator()
    data = validator.validate_ranges(data)

    # Extract features
    engineer = FeatureEngineer(lookback_window=20)
    features = engineer.extract_all_features(data)

    # Normalize
    normalizer = FeatureNormalizer()
    X = normalizer.fit_transform(features.values)

    # Train model
    model = RandomForestModel(n_estimators=10)  # Small for test
    y_numbers = data[['n1', 'n2', 'n3', 'n4', 'n5']].values
    y_stars = data[['s1', 's2']].values

    model.train(X[:80], (y_numbers[:80], y_stars[:80]))

    # Predict
    predictor = Predictor(model, engineer, normalizer)
    predictions = predictor.predict_next_draw(data[:80], n_predictions=1)

    # Validate prediction format
    assert len(predictions) == 1
    assert 'numbers' in predictions[0]
    assert 'stars' in predictions[0]
    assert len(predictions[0]['numbers']) == 5
    assert len(predictions[0]['stars']) == 2
```

**Coverage Goal**: Minimum 80% code coverage

```bash
pytest --cov=euromillions_ml --cov-report=html --cov-report=term
```

---

## 10. Deployment & Usage

### Installation

```bash
# Clone repository
git clone https://github.com/user/euromillions-ml-predictor.git
cd euromillions-ml-predictor

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black euromillions_ml/
isort euromillions_ml/
```

### Quick Start

```bash
# 1. Generate prediction with default settings
python main.py

# 2. Run backtest
python main.py --mode backtest --model hybrid

# 3. Train specific model
python main.py --mode train --model lstm --epochs 200

# 4. Generate multiple predictions
python main.py --n-predictions 10 --export csv --output my_predictions.csv
```

### Project Initialization Checklist

- [ ] Create virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Download historical data or configure scraper
- [ ] Place CSV in `data/historical.csv` (if using CSV mode)
- [ ] Review and customize `config.yaml`
- [ ] Run data validation: `python -m euromillions_ml.data.validator`
- [ ] Train initial models: `python main.py --mode train --model hybrid`
- [ ] Run backtest to validate: `python main.py --mode backtest`
- [ ] Generate predictions: `python main.py --mode predict`

---

## Summary

This architecture provides:

1. **Modularity**: Clear separation of concerns across data, features, models, prediction, and utils
2. **Extensibility**: Easy to add new models, features, or data sources
3. **Robustness**: Comprehensive error handling and validation
4. **Performance**: Optimized with caching, vectorization, and optional GPU support
5. **Maintainability**: Type hints, docstrings, and extensive testing
6. **Usability**: Rich CLI interface with flexible configuration

The system follows ML best practices with proper train/val/test splits, feature engineering, normalization, and backtesting capabilities.
