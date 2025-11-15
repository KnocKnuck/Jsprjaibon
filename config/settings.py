"""Configuration management with Pydantic validation"""
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings
from typing import Tuple
import yaml
from pathlib import Path


class APISettings(BaseSettings):
    """API configuration settings"""
    base_url: HttpUrl = "https://euromillions.api.pedromealha.dev"
    timeout: int = Field(30, ge=5, le=120)
    rate_limit: float = Field(2.0, ge=0.5)
    retry_attempts: int = Field(4, ge=1, le=10)
    retry_backoff: float = Field(2.0, ge=1.0)

    class Config:
        env_prefix = "EUROMILLIONS_API_"


class DataSettings(BaseSettings):
    """Data storage and caching settings"""
    cache_dir: str = "./data/cache"
    cache_ttl_historical: int = 0  # Never expire
    cache_ttl_current: int = 86400  # 24 hours

    class Config:
        env_prefix = "EUROMILLIONS_DATA_"


class LotterySettings(BaseSettings):
    """Euromillions game rules and constraints"""
    numbers_range: Tuple[int, int] = (1, 50)
    stars_range: Tuple[int, int] = (1, 12)
    numbers_count: int = 5
    stars_count: int = 2

    @field_validator('numbers_range', 'stars_range')
    @classmethod
    def validate_range(cls, v):
        """Ensure range start is less than end"""
        if v[0] >= v[1]:
            raise ValueError("Range start must be less than end")
        return v

    class Config:
        env_prefix = "EUROMILLIONS_LOTTERY_"


class Settings(BaseSettings):
    """Main application settings"""
    api: APISettings = APISettings()
    data: DataSettings = DataSettings()
    lottery: LotterySettings = LotterySettings()

    @classmethod
    def load_from_yaml(cls, path: str = "config.yaml") -> "Settings":
        """Load settings from YAML file

        Args:
            path: Path to YAML configuration file

        Returns:
            Settings instance with validated configuration

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config validation fails
        """
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(config_path) as f:
            config_dict = yaml.safe_load(f)

        return cls(**config_dict)

    class Config:
        env_prefix = "EUROMILLIONS_"
