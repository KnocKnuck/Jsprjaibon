"""
Data acquisition and management module.

This module handles:
- API client for pedro-mealha/euromillions-api
- Data loading and caching
- Data validation and preprocessing
"""

from typing import List

# Re-export from root data module for convenience
import sys
sys.path.insert(0, '/home/user/Jsprjaibon')

from data.models import Draw

__all__: List[str] = ["Draw"]
