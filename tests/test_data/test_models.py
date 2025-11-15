"""Tests for Pydantic data models"""
import pytest
from datetime import date
from pydantic import ValidationError

from data.models import Prize, Draw


@pytest.mark.unit
class TestPrizeModel:
    """Test Prize model validation"""

    def test_valid_prize(self):
        """Test creating valid Prize"""
        prize = Prize(
            prize_amount=1000000.0,
            winners_count=1,
            matched_numbers=5,
            matched_stars=2
        )

        assert prize.prize_amount == 1000000.0
        assert prize.winners_count == 1
        assert prize.matched_numbers == 5
        assert prize.matched_stars == 2

    def test_prize_zero_amount(self):
        """Test Prize with zero amount"""
        prize = Prize(
            prize_amount=0.0,
            winners_count=0,
            matched_numbers=3,
            matched_stars=1
        )

        assert prize.prize_amount == 0.0

    def test_prize_negative_amount(self):
        """Test Prize with negative amount (should fail)"""
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=-1000.0,
                winners_count=1,
                matched_numbers=5,
                matched_stars=2
            )

    def test_prize_negative_winners(self):
        """Test Prize with negative winners (should fail)"""
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=1000.0,
                winners_count=-1,
                matched_numbers=5,
                matched_stars=2
            )

    def test_prize_invalid_matched_numbers(self):
        """Test Prize with invalid matched_numbers"""
        # Too many numbers
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=1000.0,
                winners_count=1,
                matched_numbers=6,
                matched_stars=2
            )

        # Negative numbers
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=1000.0,
                winners_count=1,
                matched_numbers=-1,
                matched_stars=2
            )

    def test_prize_invalid_matched_stars(self):
        """Test Prize with invalid matched_stars"""
        # Too many stars
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=1000.0,
                winners_count=1,
                matched_numbers=5,
                matched_stars=3
            )

        # Negative stars
        with pytest.raises(ValidationError):
            Prize(
                prize_amount=1000.0,
                winners_count=1,
                matched_numbers=5,
                matched_stars=-1
            )

    def test_prize_immutability(self, sample_prize):
        """Test that Prize is immutable"""
        with pytest.raises((ValidationError, AttributeError)):
            sample_prize.prize_amount = 2000000.0


@pytest.mark.unit
class TestDrawModel:
    """Test Draw model validation"""

    def test_valid_draw(self):
        """Test creating valid Draw"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[3, 12, 23, 34, 45],
            stars=[5, 9],
            date=date(2024, 1, 5),
            has_winner=True,
            prizes=[]
        )

        assert draw.id == 1
        assert draw.draw_id == 2024001
        assert draw.numbers == [3, 12, 23, 34, 45]
        assert draw.stars == [5, 9]
        assert draw.date == date(2024, 1, 5)
        assert draw.has_winner is True

    def test_draw_auto_sorts_numbers(self):
        """Test that numbers are automatically sorted"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[45, 3, 34, 12, 23],  # Unsorted
            stars=[9, 5],
            date=date(2024, 1, 5),
            has_winner=True,
            prizes=[]
        )

        assert draw.numbers == [3, 12, 23, 34, 45]
        assert draw.stars == [5, 9]

    def test_draw_invalid_number_count(self):
        """Test Draw with wrong number of numbers"""
        # Too few numbers
        with pytest.raises(ValidationError):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34],  # Only 4
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

        # Too many numbers
        with pytest.raises(ValidationError):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45, 50],  # 6 numbers
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_invalid_star_count(self):
        """Test Draw with wrong number of stars"""
        # Too few stars
        with pytest.raises(ValidationError):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45],
                stars=[5],  # Only 1
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

        # Too many stars
        with pytest.raises(ValidationError):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45],
                stars=[5, 9, 12],  # 3 stars
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_numbers_out_of_range(self):
        """Test Draw with numbers out of valid range"""
        # Number too low
        with pytest.raises(ValidationError, match="Numbers must be between 1 and 50"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[0, 12, 23, 34, 45],
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

        # Number too high
        with pytest.raises(ValidationError, match="Numbers must be between 1 and 50"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 51],
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_stars_out_of_range(self):
        """Test Draw with stars out of valid range"""
        # Star too low
        with pytest.raises(ValidationError, match="Stars must be between 1 and 12"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45],
                stars=[0, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

        # Star too high
        with pytest.raises(ValidationError, match="Stars must be between 1 and 12"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45],
                stars=[5, 13],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_duplicate_numbers(self):
        """Test Draw with duplicate numbers"""
        with pytest.raises(ValidationError, match="Numbers must be unique"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 12, 34, 45],  # 12 appears twice
                stars=[5, 9],
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_duplicate_stars(self):
        """Test Draw with duplicate stars"""
        with pytest.raises(ValidationError, match="Stars must be unique"):
            Draw(
                id=1,
                draw_id=2024001,
                numbers=[3, 12, 23, 34, 45],
                stars=[5, 5],  # 5 appears twice
                date=date(2024, 1, 5),
                has_winner=True,
                prizes=[]
            )

    def test_draw_with_prizes(self, sample_prize):
        """Test Draw with prize information"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[3, 12, 23, 34, 45],
            stars=[5, 9],
            date=date(2024, 1, 5),
            has_winner=True,
            prizes=[sample_prize]
        )

        assert len(draw.prizes) == 1
        assert draw.prizes[0].prize_amount == 1000000.0

    def test_draw_without_prizes(self):
        """Test Draw without prize information"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[3, 12, 23, 34, 45],
            stars=[5, 9],
            date=date(2024, 1, 5),
            has_winner=False,
            prizes=None
        )

        assert draw.prizes is None

    def test_draw_immutability(self, sample_draw):
        """Test that Draw is immutable"""
        with pytest.raises((ValidationError, AttributeError)):
            sample_draw.numbers = [1, 2, 3, 4, 5]

        with pytest.raises((ValidationError, AttributeError)):
            sample_draw.has_winner = False

    def test_draw_string_representation(self, sample_draw):
        """Test Draw string representation"""
        str_repr = str(sample_draw)

        assert "Draw 2024001" in str_repr
        assert "2024-01-05" in str_repr
        assert "3, 12, 23, 34, 45" in str_repr
        assert "5, 9" in str_repr

    def test_draw_dict_conversion(self, sample_draw):
        """Test converting Draw to dict"""
        draw_dict = sample_draw.dict()

        assert draw_dict['id'] == 1
        assert draw_dict['draw_id'] == 2024001
        assert draw_dict['numbers'] == [3, 12, 23, 34, 45]
        assert draw_dict['stars'] == [5, 9]
        assert draw_dict['has_winner'] is True

    def test_draw_from_dict(self):
        """Test creating Draw from dict"""
        draw_dict = {
            "id": 1,
            "draw_id": 2024001,
            "numbers": [3, 12, 23, 34, 45],
            "stars": [5, 9],
            "date": date(2024, 1, 5),
            "has_winner": True,
            "prizes": []
        }

        draw = Draw(**draw_dict)

        assert draw.id == 1
        assert draw.draw_id == 2024001


@pytest.mark.unit
class TestDrawModelEdgeCases:
    """Test edge cases for Draw model"""

    def test_draw_minimum_valid_numbers(self):
        """Test Draw with minimum valid numbers"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[1, 2, 3, 4, 5],
            stars=[1, 2],
            date=date(2024, 1, 5),
            has_winner=False,
            prizes=[]
        )

        assert draw.numbers == [1, 2, 3, 4, 5]
        assert draw.stars == [1, 2]

    def test_draw_maximum_valid_numbers(self):
        """Test Draw with maximum valid numbers"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[46, 47, 48, 49, 50],
            stars=[11, 12],
            date=date(2024, 1, 5),
            has_winner=False,
            prizes=[]
        )

        assert draw.numbers == [46, 47, 48, 49, 50]
        assert draw.stars == [11, 12]

    def test_draw_mixed_ranges(self):
        """Test Draw with numbers across full range"""
        draw = Draw(
            id=1,
            draw_id=2024001,
            numbers=[1, 15, 25, 40, 50],
            stars=[1, 12],
            date=date(2024, 1, 5),
            has_winner=False,
            prizes=[]
        )

        assert min(draw.numbers) == 1
        assert max(draw.numbers) == 50
        assert min(draw.stars) == 1
        assert max(draw.stars) == 12

    def test_draw_date_formats(self):
        """Test Draw with different date formats"""
        # Date object
        draw1 = Draw(
            id=1,
            draw_id=2024001,
            numbers=[1, 2, 3, 4, 5],
            stars=[1, 2],
            date=date(2024, 1, 5),
            has_winner=False,
            prizes=[]
        )

        # String date (should be converted)
        draw2 = Draw(
            id=2,
            draw_id=2024002,
            numbers=[1, 2, 3, 4, 5],
            stars=[1, 2],
            date="2024-01-05",
            has_winner=False,
            prizes=[]
        )

        assert draw1.date == draw2.date


@pytest.mark.unit
class TestModelSerialization:
    """Test model serialization and deserialization"""

    def test_draw_json_serialization(self, sample_draw):
        """Test serializing Draw to JSON"""
        json_str = sample_draw.json()

        assert isinstance(json_str, str)
        assert "2024001" in json_str
        assert "2024-01-05" in json_str

    def test_draw_json_deserialization(self):
        """Test deserializing Draw from JSON"""
        json_str = '{"id": 1, "draw_id": 2024001, "numbers": [3, 12, 23, 34, 45], "stars": [5, 9], "date": "2024-01-05", "has_winner": true, "prizes": []}'

        draw = Draw.parse_raw(json_str)

        assert draw.id == 1
        assert draw.draw_id == 2024001
        assert draw.numbers == [3, 12, 23, 34, 45]

    def test_prize_json_round_trip(self, sample_prize):
        """Test Prize JSON serialization round trip"""
        json_str = sample_prize.json()
        prize_copy = Prize.parse_raw(json_str)

        assert prize_copy.prize_amount == sample_prize.prize_amount
        assert prize_copy.winners_count == sample_prize.winners_count
        assert prize_copy.matched_numbers == sample_prize.matched_numbers
        assert prize_copy.matched_stars == sample_prize.matched_stars
