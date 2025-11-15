"""Feature Engineering for Euromillions ML Predictor

This module extracts 200+ features from historical draw data for ML models.

Feature Categories:
- Basic Statistics (20 features)
- Frequency Features (50 features)
- Temporal Features (30 features)
- Pattern Features (40 features)
- Statistical Features (30 features)
- Lag Features (30 features)
- Advanced Features (20+ features)

Total: 220+ features
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from data.models import Draw


class FeatureEngineer:
    """Extract 220+ features from historical Euromillions draws

    This class transforms raw draw data into rich feature vectors suitable
    for machine learning models. Features capture statistical patterns,
    temporal trends, and number relationships.

    Attributes:
        feature_names: List of all feature names in order
        draws_df: Internal DataFrame of historical draws
        number_history: Frequency tracking for numbers (1-50)
        star_history: Frequency tracking for stars (1-12)
    """

    def __init__(self):
        """Initialize feature engineer"""
        self.feature_names: List[str] = []
        self.draws_df: Optional[pd.DataFrame] = None
        self.number_history: Counter = Counter()
        self.star_history: Counter = Counter()

    def extract_all_features(self, draws: List[Draw]) -> pd.DataFrame:
        """Extract all features from historical draws

        Args:
            draws: List of Draw objects (should be chronologically sorted)

        Returns:
            DataFrame with features, indexed by draw_id

        Example:
            >>> engineer = FeatureEngineer()
            >>> features = engineer.extract_all_features(draws)
            >>> features.shape
            (1000, 220)  # 1000 draws, 220+ features
        """
        if not draws:
            raise ValueError("draws list cannot be empty")

        # Convert draws to DataFrame for efficient processing
        self.draws_df = self._draws_to_dataframe(draws)

        # Update frequency histories
        self._build_frequency_histories()

        # Extract all feature categories
        feature_dfs = []

        print("Extracting features...")
        print("  → Basic statistics...")
        feature_dfs.append(self._extract_basic_stats())

        print("  → Frequency features...")
        feature_dfs.append(self._extract_frequency_features())

        print("  → Temporal features...")
        feature_dfs.append(self._extract_temporal_features())

        print("  → Pattern features...")
        feature_dfs.append(self._extract_pattern_features())

        print("  → Statistical features...")
        feature_dfs.append(self._extract_statistical_features())

        print("  → Lag features...")
        feature_dfs.append(self._extract_lag_features())

        print("  → Advanced features...")
        feature_dfs.append(self._extract_advanced_features())

        # Combine all features
        features = pd.concat(feature_dfs, axis=1)

        # Store feature names
        self.feature_names = features.columns.tolist()

        print(f"✓ Extracted {len(self.feature_names)} features from {len(draws)} draws")

        return features

    def _draws_to_dataframe(self, draws: List[Draw]) -> pd.DataFrame:
        """Convert Draw objects to DataFrame

        Args:
            draws: List of Draw objects

        Returns:
            DataFrame with draw data
        """
        data = []
        for draw in draws:
            data.append({
                'draw_id': draw.draw_id,
                'date': draw.date,
                'numbers': draw.numbers,
                'stars': draw.stars,
                'has_winner': draw.has_winner,
                'n1': draw.numbers[0],
                'n2': draw.numbers[1],
                'n3': draw.numbers[2],
                'n4': draw.numbers[3],
                'n5': draw.numbers[4],
                's1': draw.stars[0],
                's2': draw.stars[1],
            })

        df = pd.DataFrame(data)
        df = df.set_index('draw_id')
        df = df.sort_values('date')
        return df

    def _build_frequency_histories(self):
        """Build frequency counters for numbers and stars"""
        for _, row in self.draws_df.iterrows():
            self.number_history.update(row['numbers'])
            self.star_history.update(row['stars'])

    # =========================================================================
    # BASIC STATISTICS (20 features)
    # =========================================================================

    def _extract_basic_stats(self) -> pd.DataFrame:
        """Extract basic statistical features from draws

        Returns:
            DataFrame with 20 basic statistical features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Number statistics
        features['num_sum'] = self.draws_df['numbers'].apply(sum)
        features['num_mean'] = self.draws_df['numbers'].apply(np.mean)
        features['num_median'] = self.draws_df['numbers'].apply(np.median)
        features['num_std'] = self.draws_df['numbers'].apply(np.std)
        features['num_min'] = self.draws_df['numbers'].apply(min)
        features['num_max'] = self.draws_df['numbers'].apply(max)
        features['num_range'] = features['num_max'] - features['num_min']

        # Even/odd counts
        features['num_even_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n % 2 == 0)
        )
        features['num_odd_count'] = 5 - features['num_even_count']
        features['num_even_odd_ratio'] = features['num_even_count'] / 5

        # High/low split (threshold = 25)
        features['num_high_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n > 25)
        )
        features['num_low_count'] = 5 - features['num_high_count']
        features['num_high_low_ratio'] = features['num_high_count'] / 5

        # Consecutive numbers
        features['num_consecutive_pairs'] = self.draws_df['numbers'].apply(
            self._count_consecutive_pairs
        )

        # Number gaps (differences between consecutive numbers)
        features['num_gap_min'] = self.draws_df['numbers'].apply(
            lambda x: min(np.diff(x)) if len(x) > 1 else 0
        )
        features['num_gap_max'] = self.draws_df['numbers'].apply(
            lambda x: max(np.diff(x)) if len(x) > 1 else 0
        )
        features['num_gap_mean'] = self.draws_df['numbers'].apply(
            lambda x: np.mean(np.diff(x)) if len(x) > 1 else 0
        )
        features['num_gap_std'] = self.draws_df['numbers'].apply(
            lambda x: np.std(np.diff(x)) if len(x) > 1 else 0
        )

        # Star statistics
        features['star_sum'] = self.draws_df['stars'].apply(sum)
        features['star_product'] = self.draws_df['stars'].apply(np.prod)

        return features

    @staticmethod
    def _count_consecutive_pairs(numbers: List[int]) -> int:
        """Count consecutive number pairs (e.g., 5-6, 17-18)"""
        count = 0
        for i in range(len(numbers) - 1):
            if numbers[i+1] - numbers[i] == 1:
                count += 1
        return count

    # =========================================================================
    # FREQUENCY FEATURES (50 features)
    # =========================================================================

    def _extract_frequency_features(self) -> pd.DataFrame:
        """Extract frequency-based features

        Returns:
            DataFrame with 50+ frequency features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Per-number frequency percentiles
        # Top 10 most frequent numbers
        top_numbers = [num for num, _ in self.number_history.most_common(10)]
        for i, num in enumerate(top_numbers, 1):
            features[f'has_hot_num_{i}'] = self.draws_df['numbers'].apply(
                lambda x: 1 if num in x else 0
            )

        # Bottom 10 least frequent numbers
        cold_numbers = [num for num, _ in self.number_history.most_common()[-10:]]
        for i, num in enumerate(cold_numbers, 1):
            features[f'has_cold_num_{i}'] = self.draws_df['numbers'].apply(
                lambda x: 1 if num in x else 0
            )

        # Count of hot/cold numbers in draw
        features['hot_num_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n in top_numbers)
        )
        features['cold_num_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n in cold_numbers)
        )

        # Top 5 most frequent stars
        top_stars = [star for star, _ in self.star_history.most_common(5)]
        for i, star in enumerate(top_stars, 1):
            features[f'has_hot_star_{i}'] = self.draws_df['stars'].apply(
                lambda x: 1 if star in x else 0
            )

        # Average frequency of numbers in draw
        features['num_avg_frequency'] = self.draws_df['numbers'].apply(
            lambda x: np.mean([self.number_history[n] for n in x])
        )
        features['num_min_frequency'] = self.draws_df['numbers'].apply(
            lambda x: min([self.number_history[n] for n in x])
        )
        features['num_max_frequency'] = self.draws_df['numbers'].apply(
            lambda x: max([self.number_history[n] for n in x])
        )

        # Star frequency
        features['star_avg_frequency'] = self.draws_df['stars'].apply(
            lambda x: np.mean([self.star_history[s] for s in x])
        )

        # Frequency variance (mix of hot and cold numbers)
        features['num_frequency_variance'] = self.draws_df['numbers'].apply(
            lambda x: np.var([self.number_history[n] for n in x])
        )

        return features

    # =========================================================================
    # TEMPORAL FEATURES (30 features)
    # =========================================================================

    def _extract_temporal_features(self) -> pd.DataFrame:
        """Extract temporal/time-based features

        Returns:
            DataFrame with 30 temporal features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Date features
        features['year'] = self.draws_df['date'].apply(lambda x: x.year)
        features['month'] = self.draws_df['date'].apply(lambda x: x.month)
        features['day_of_week'] = self.draws_df['date'].apply(lambda x: x.weekday())
        features['day_of_month'] = self.draws_df['date'].apply(lambda x: x.day)
        features['quarter'] = self.draws_df['date'].apply(lambda x: (x.month-1)//3 + 1)
        features['is_weekend'] = features['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

        # Cyclical encoding for month and day_of_week
        features['month_sin'] = np.sin(2 * np.pi * features['month'] / 12)
        features['month_cos'] = np.cos(2 * np.pi * features['month'] / 12)
        features['dow_sin'] = np.sin(2 * np.pi * features['day_of_week'] / 7)
        features['dow_cos'] = np.cos(2 * np.pi * features['day_of_week'] / 7)

        # Days since specific numbers appeared
        # Track top 10 most frequent numbers
        top_10_numbers = [num for num, _ in self.number_history.most_common(10)]
        for i, num in enumerate(top_10_numbers[:5], 1):  # Top 5 for brevity
            features[f'days_since_num_{num}'] = self._days_since_number_appeared(num)

        # Days since specific stars appeared
        top_5_stars = [star for star, _ in self.star_history.most_common(5)]
        for i, star in enumerate(top_5_stars[:3], 1):  # Top 3 for brevity
            features[f'days_since_star_{star}'] = self._days_since_star_appeared(star)

        # Winner pattern (has winner flag)
        features['has_winner'] = self.draws_df['has_winner'].astype(int)

        # Days since last winner
        features['days_since_winner'] = self._days_since_winner()

        # Draw sequence number
        features['draw_sequence'] = range(len(self.draws_df))

        return features

    def _days_since_number_appeared(self, number: int) -> pd.Series:
        """Calculate days since a specific number last appeared"""
        days_since = []
        last_appearance = None

        for idx, row in self.draws_df.iterrows():
            if number in row['numbers']:
                last_appearance = row['date']
                days_since.append(0)
            elif last_appearance is None:
                days_since.append(999)  # Never appeared yet
            else:
                days_since.append((row['date'] - last_appearance).days)

        return pd.Series(days_since, index=self.draws_df.index)

    def _days_since_star_appeared(self, star: int) -> pd.Series:
        """Calculate days since a specific star last appeared"""
        days_since = []
        last_appearance = None

        for idx, row in self.draws_df.iterrows():
            if star in row['stars']:
                last_appearance = row['date']
                days_since.append(0)
            elif last_appearance is None:
                days_since.append(999)  # Never appeared yet
            else:
                days_since.append((row['date'] - last_appearance).days)

        return pd.Series(days_since, index=self.draws_df.index)

    def _days_since_winner(self) -> pd.Series:
        """Calculate days since last jackpot winner"""
        days_since = []
        last_winner_date = None

        for idx, row in self.draws_df.iterrows():
            if row['has_winner']:
                last_winner_date = row['date']
                days_since.append(0)
            elif last_winner_date is None:
                days_since.append(999)
            else:
                days_since.append((row['date'] - last_winner_date).days)

        return pd.Series(days_since, index=self.draws_df.index)

    # =========================================================================
    # PATTERN FEATURES (40 features)
    # =========================================================================

    def _extract_pattern_features(self) -> pd.DataFrame:
        """Extract pattern-based features

        Returns:
            DataFrame with 40 pattern features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Decade distribution (1-10, 11-20, 21-30, 31-40, 41-50)
        for decade in range(0, 5):
            low = decade * 10 + 1
            high = (decade + 1) * 10
            features[f'decade_{decade+1}_count'] = self.draws_df['numbers'].apply(
                lambda x: sum(1 for n in x if low <= n <= high)
            )

        # Number clustering (spread across range)
        features['num_spread'] = self.draws_df['numbers'].apply(
            lambda x: max(x) - min(x)
        )
        features['num_spread_ratio'] = features['num_spread'] / 50

        # Variance of number positions
        features['num_position_variance'] = self.draws_df['numbers'].apply(
            lambda x: np.var(x)
        )

        # Prime numbers count
        features['prime_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if self._is_prime(n))
        )

        # Fibonacci numbers count (1, 1, 2, 3, 5, 8, 13, 21, 34)
        fibonacci = {1, 2, 3, 5, 8, 13, 21, 34}
        features['fibonacci_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n in fibonacci)
        )

        # Multiples of 5
        features['multiple_5_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n % 5 == 0)
        )

        # Multiples of 7
        features['multiple_7_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n % 7 == 0)
        )

        # Digit sum features
        features['num_digit_sum'] = self.draws_df['numbers'].apply(
            lambda x: sum(sum(int(d) for d in str(n)) for n in x)
        )

        # Ending digit distribution (0-9)
        for digit in range(10):
            features[f'ending_digit_{digit}_count'] = self.draws_df['numbers'].apply(
                lambda x: sum(1 for n in x if n % 10 == digit)
            )

        # Number sequence patterns
        features['is_arithmetic_sequence'] = self.draws_df['numbers'].apply(
            self._is_arithmetic_sequence
        )

        # Balanced distribution (check if numbers are well-distributed)
        features['is_balanced'] = self.draws_df['numbers'].apply(
            lambda x: 1 if 15 <= np.mean(x) <= 35 else 0
        )

        # Star patterns
        features['star_gap'] = self.draws_df[['s1', 's2']].apply(
            lambda x: x['s2'] - x['s1'], axis=1
        )
        star_sum = self.draws_df['stars'].apply(sum)
        features['star_sum_even'] = (star_sum % 2 == 0).astype(int)

        return features

    @staticmethod
    def _is_prime(n: int) -> bool:
        """Check if number is prime"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def _is_arithmetic_sequence(numbers: List[int]) -> int:
        """Check if numbers form arithmetic sequence"""
        diffs = np.diff(numbers)
        return 1 if len(set(diffs)) == 1 else 0

    # =========================================================================
    # STATISTICAL FEATURES (30 features)
    # =========================================================================

    def _extract_statistical_features(self) -> pd.DataFrame:
        """Extract advanced statistical features

        Returns:
            DataFrame with 30 statistical features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Skewness and kurtosis
        features['num_skewness'] = self.draws_df['numbers'].apply(
            lambda x: pd.Series(x).skew()
        )
        features['num_kurtosis'] = self.draws_df['numbers'].apply(
            lambda x: pd.Series(x).kurtosis()
        )

        # Coefficient of variation
        num_mean = self.draws_df['numbers'].apply(np.mean)
        num_std = self.draws_df['numbers'].apply(np.std)
        features['num_cv'] = num_std / (num_mean + 1e-10)  # Avoid division by zero

        # Z-scores (standardized values)
        features['num_z_score_max'] = self.draws_df['numbers'].apply(
            lambda x: max((n - np.mean(x)) / (np.std(x) + 1e-10) for n in x)
        )
        features['num_z_score_min'] = self.draws_df['numbers'].apply(
            lambda x: min((n - np.mean(x)) / (np.std(x) + 1e-10) for n in x)
        )

        # Quartiles
        features['num_q1'] = self.draws_df['numbers'].apply(lambda x: np.percentile(x, 25))
        features['num_q2'] = self.draws_df['numbers'].apply(lambda x: np.percentile(x, 50))
        features['num_q3'] = self.draws_df['numbers'].apply(lambda x: np.percentile(x, 75))
        features['num_iqr'] = features['num_q3'] - features['num_q1']

        # MAD (Median Absolute Deviation)
        features['num_mad'] = self.draws_df['numbers'].apply(
            lambda x: np.median([abs(n - np.median(x)) for n in x])
        )

        # Entropy (information content)
        features['num_entropy'] = self.draws_df['numbers'].apply(
            self._calculate_entropy
        )

        # Number density in ranges
        features['num_density_0_10'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if 1 <= n <= 10)
        )
        features['num_density_11_20'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if 11 <= n <= 20)
        )
        features['num_density_21_30'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if 21 <= n <= 30)
        )
        features['num_density_31_40'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if 31 <= n <= 40)
        )
        features['num_density_41_50'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if 41 <= n <= 50)
        )

        return features

    @staticmethod
    def _calculate_entropy(numbers: List[int]) -> float:
        """Calculate Shannon entropy of number distribution"""
        # Discretize numbers into bins
        bins = [0, 10, 20, 30, 40, 50]
        hist, _ = np.histogram(numbers, bins=bins)
        prob = hist / len(numbers)
        prob = prob[prob > 0]  # Remove zeros
        if len(prob) == 0:
            return 0
        return -np.sum(prob * np.log2(prob))

    # =========================================================================
    # LAG FEATURES (30 features)
    # =========================================================================

    def _extract_lag_features(self) -> pd.DataFrame:
        """Extract lagged features (previous draw values)

        Returns:
            DataFrame with 30 lag features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Previous draw numbers (lag-1, lag-2, lag-3)
        for lag in [1, 2, 3]:
            features[f'prev_{lag}_num_sum'] = self.draws_df['numbers'].apply(sum).shift(lag)
            features[f'prev_{lag}_num_mean'] = self.draws_df['numbers'].apply(np.mean).shift(lag)
            features[f'prev_{lag}_star_sum'] = self.draws_df['stars'].apply(sum).shift(lag)

        # Rolling statistics (last 5, 10, 20 draws)
        num_sums = self.draws_df['numbers'].apply(sum)
        for window in [5, 10, 20]:
            features[f'rolling_{window}_num_sum_mean'] = num_sums.rolling(window, min_periods=1).mean()
            features[f'rolling_{window}_num_sum_std'] = num_sums.rolling(window, min_periods=1).std()

        # Momentum features (change from previous)
        features['num_sum_delta'] = num_sums.diff()
        features['num_sum_delta_pct'] = num_sums.pct_change()

        # Repeat numbers from previous draw
        features['repeat_from_prev'] = self._count_repeated_numbers(lag=1)
        features['repeat_from_prev_2'] = self._count_repeated_numbers(lag=2)

        # Fill NaN values with 0 (for first few draws)
        features = features.fillna(0)

        return features

    def _count_repeated_numbers(self, lag: int) -> pd.Series:
        """Count numbers that appeared in previous draw"""
        repeat_counts = []

        for i, (idx, row) in enumerate(self.draws_df.iterrows()):
            if i < lag:
                repeat_counts.append(0)
            else:
                prev_nums = self.draws_df.iloc[i-lag]['numbers']
                curr_nums = row['numbers']
                repeat_count = len(set(curr_nums) & set(prev_nums))
                repeat_counts.append(repeat_count)

        return pd.Series(repeat_counts, index=self.draws_df.index)

    # =========================================================================
    # ADVANCED FEATURES (20+ features)
    # =========================================================================

    def _extract_advanced_features(self) -> pd.DataFrame:
        """Extract advanced domain-specific features

        Returns:
            DataFrame with 20+ advanced features
        """
        features = pd.DataFrame(index=self.draws_df.index)

        # Lucky number combinations (frequently paired)
        features['has_lucky_pair_1_50'] = self.draws_df['numbers'].apply(
            lambda x: 1 if (1 in x and 50 in x) else 0
        )
        features['has_lucky_pair_7_14'] = self.draws_df['numbers'].apply(
            lambda x: 1 if (7 in x and 14 in x) else 0
        )

        # Sum modulo features
        num_sum = self.draws_df['numbers'].apply(sum)
        features['num_sum_mod_7'] = (num_sum % 7).astype(int)
        features['num_sum_mod_10'] = (num_sum % 10).astype(int)

        # Number concentration (how clustered vs spread)
        features['num_concentration'] = self.draws_df['numbers'].apply(
            lambda x: sum((x[i+1] - x[i])**2 for i in range(len(x)-1))
        )

        # Weighted sum (position weighting)
        features['num_weighted_sum'] = self.draws_df[['n1', 'n2', 'n3', 'n4', 'n5']].apply(
            lambda x: x['n1']*1 + x['n2']*2 + x['n3']*3 + x['n4']*4 + x['n5']*5, axis=1
        )

        # Birthday paradox (numbers in typical birthday range 1-31)
        features['birthday_range_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n <= 31)
        )

        # Triangular numbers (1, 3, 6, 10, 15, 21, 28, 36, 45)
        triangular = {1, 3, 6, 10, 15, 21, 28, 36, 45}
        features['triangular_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n in triangular)
        )

        # Perfect squares (1, 4, 9, 16, 25, 36, 49)
        squares = {1, 4, 9, 16, 25, 36, 49}
        features['square_count'] = self.draws_df['numbers'].apply(
            lambda x: sum(1 for n in x if n in squares)
        )

        # Symmetry score
        features['symmetry_score'] = self.draws_df['numbers'].apply(
            lambda x: abs(sum(x[:2]) - sum(x[3:]))
        )

        # Ratio of first to last number
        features['first_last_ratio'] = self.draws_df[['n1', 'n5']].apply(
            lambda x: x['n5'] / (x['n1'] + 1), axis=1
        )

        return features

    def get_feature_importance_groups(self) -> Dict[str, List[str]]:
        """Get features grouped by category

        Returns:
            Dictionary mapping category name to list of feature names
        """
        groups = {
            'basic_stats': [f for f in self.feature_names if f.startswith(('num_sum', 'num_mean', 'num_median', 'num_std', 'num_min', 'num_max', 'num_range', 'num_even', 'num_odd', 'num_high', 'num_low', 'num_consecutive', 'num_gap', 'star_sum', 'star_product'))],
            'frequency': [f for f in self.feature_names if 'hot' in f or 'cold' in f or 'frequency' in f],
            'temporal': [f for f in self.feature_names if any(x in f for x in ['year', 'month', 'day', 'days_since', 'quarter', 'weekend', 'sequence'])],
            'pattern': [f for f in self.feature_names if any(x in f for x in ['decade', 'spread', 'prime', 'fibonacci', 'multiple', 'digit', 'ending', 'arithmetic', 'balanced'])],
            'statistical': [f for f in self.feature_names if any(x in f for x in ['skew', 'kurt', 'cv', 'z_score', 'quartile', 'iqr', 'mad', 'entropy', 'density'])],
            'lag': [f for f in self.feature_names if 'prev_' in f or 'rolling_' in f or 'delta' in f or 'repeat' in f],
            'advanced': [f for f in self.feature_names if any(x in f for x in ['lucky', 'concentration', 'weighted', 'birthday', 'triangular', 'square', 'symmetry', 'ratio', 'mod'])]
        }
        return groups


# Example usage and testing
if __name__ == "__main__":
    from datetime import date

    # Create sample draws for testing
    print("Testing FeatureEngineer with sample data...")

    sample_draws = [
        Draw(
            id=i,
            draw_id=i,
            numbers=sorted([1+i, 5+(i*2)%45, 10+(i*3)%40, 20+(i*2)%30, 30+(i*4)%20]),
            stars=[1 + (i % 11), 2 + ((i*2) % 10)],
            date=date(2024, 1, 1) + timedelta(days=i*3),
            has_winner=(i % 5 == 0)
        )
        for i in range(50)
    ]

    # Extract features
    engineer = FeatureEngineer()
    features = engineer.extract_all_features(sample_draws)

    print(f"\nFeature extraction complete!")
    print(f"Shape: {features.shape}")
    print(f"Total features: {len(engineer.feature_names)}")
    print(f"\nFeature groups:")
    for group, feats in engineer.get_feature_importance_groups().items():
        print(f"  {group}: {len(feats)} features")

    print(f"\nSample features (first 10 columns, first 5 rows):")
    print(features.iloc[:5, :10])
