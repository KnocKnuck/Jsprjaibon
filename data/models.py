"""Pydantic models for API data validation"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date


class Prize(BaseModel):
    """Prize tier information for a draw"""
    prize_amount: float = Field(..., ge=0)
    winners_count: int = Field(..., ge=0)
    matched_numbers: int = Field(..., ge=0, le=5)
    matched_stars: int = Field(..., ge=0, le=2)

    class Config:
        frozen = True  # Make immutable


class Draw(BaseModel):
    """Euromillions draw result"""
    id: int
    draw_id: int
    numbers: List[int] = Field(..., min_items=5, max_items=5)
    stars: List[int] = Field(..., min_items=2, max_items=2)
    date: date
    has_winner: bool
    prizes: Optional[List[Prize]] = None

    @field_validator('numbers')
    @classmethod
    def validate_numbers(cls, v):
        """Validate numbers are in valid range and unique"""
        if not all(1 <= n <= 50 for n in v):
            raise ValueError("Numbers must be between 1 and 50")
        if len(set(v)) != 5:
            raise ValueError("Numbers must be unique")
        return sorted(v)

    @field_validator('stars')
    @classmethod
    def validate_stars(cls, v):
        """Validate stars are in valid range and unique"""
        if not all(1 <= s <= 12 for s in v):
            raise ValueError("Stars must be between 1 and 12")
        if len(set(v)) != 2:
            raise ValueError("Stars must be unique")
        return sorted(v)

    class Config:
        frozen = True  # Make immutable

    def __str__(self) -> str:
        """Human-readable representation"""
        nums = ', '.join(str(n) for n in self.numbers)
        stars = ', '.join(str(s) for s in self.stars)
        return f"Draw {self.draw_id} ({self.date}): [{nums}] + [{stars}]"
