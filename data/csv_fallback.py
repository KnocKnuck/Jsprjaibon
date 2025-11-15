"""CSV fallback for when API is unavailable

This module provides fallback data loading from CSV files when the
Euromillions API is rate-limited or unavailable. It also includes
utilities to create sample CSV data for testing purposes.
"""
import pandas as pd
from pathlib import Path
from typing import List
from datetime import datetime, date
import structlog

from data.models import Draw

logger = structlog.get_logger()


def load_from_csv(csv_path: str = "data/euromillions_historical.csv") -> List[Draw]:
    """Load draws from CSV file

    Args:
        csv_path: Path to CSV file with historical draws

    Returns:
        List of Draw objects parsed from CSV

    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    logger.info("loading_from_csv", path=csv_path)

    try:
        df = pd.read_csv(csv_path)
        logger.info("csv_loaded", rows=len(df))
    except Exception as e:
        logger.error("csv_load_failed", path=csv_path, error=str(e))
        raise ValueError(f"Failed to load CSV: {e}")

    draws = []
    for idx, row in df.iterrows():
        try:
            # Parse numbers and stars
            numbers = [int(row[f'N{i}']) for i in range(1, 6)]
            stars = [int(row[f'E{i}']) for i in range(1, 3)]

            # Parse date
            draw_date = datetime.strptime(str(row['Date']), '%Y-%m-%d').date()

            # Create Draw object
            draw = Draw(
                id=int(row.get('id', idx)),
                draw_id=int(row.get('draw_id', idx)),
                numbers=numbers,
                stars=stars,
                date=draw_date,
                has_winner=bool(row.get('has_winner', False)),
                prizes=None  # CSV doesn't include prize details
            )
            draws.append(draw)

        except Exception as e:
            logger.warning("row_parse_failed", row=idx, error=str(e))
            continue

    logger.info("csv_parse_complete", total_draws=len(draws))
    return draws


def create_sample_csv(output_path: str = "data/euromillions_historical.csv", num_draws: int = 200):
    """Create sample CSV with recent data for testing

    Args:
        output_path: Path where CSV file will be created
        num_draws: Number of sample draws to generate (default: 200)

    Note:
        This generates MOCK data for testing purposes only.
        Do NOT use for actual predictions!
    """
    import random
    from datetime import timedelta

    logger.info("creating_sample_csv", output_path=output_path, num_draws=num_draws)

    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    data = []
    # Start from ~400 days ago to have enough history
    start_date = datetime.now().date() - timedelta(days=num_draws * 2)

    for i in range(num_draws):
        # Euromillions draws are typically Tue/Fri
        draw_date = start_date + timedelta(days=i * 2)

        # Generate random but valid numbers
        numbers = sorted(random.sample(range(1, 51), 5))  # 5 numbers from 1-50
        stars = sorted(random.sample(range(1, 13), 2))    # 2 stars from 1-12

        data.append({
            'id': i + 1,
            'draw_id': i + 1,
            'Date': draw_date.isoformat(),
            'N1': numbers[0],
            'N2': numbers[1],
            'N3': numbers[2],
            'N4': numbers[3],
            'N5': numbers[4],
            'E1': stars[0],
            'E2': stars[1],
            'has_winner': random.choice([True, False])
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

    logger.info("sample_csv_created", path=output_path, rows=len(data))
    print(f"✓ Created sample CSV with {len(data)} draws at {output_path}")

    return output_path


def load_real_csv(csv_path: str = "data/euromillions_real.csv") -> List[Draw]:
    """Load real Euromillions data from CSV if available

    This is for loading actual historical data that was previously
    fetched from the API and saved to CSV for offline use.

    Args:
        csv_path: Path to CSV with real historical data

    Returns:
        List of Draw objects
    """
    return load_from_csv(csv_path)


def export_draws_to_csv(draws: List[Draw], output_path: str = "data/euromillions_export.csv"):
    """Export Draw objects to CSV format

    Useful for caching API results to CSV for faster loading later.

    Args:
        draws: List of Draw objects to export
        output_path: Where to save the CSV file
    """
    logger.info("exporting_to_csv", path=output_path, count=len(draws))

    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    data = []
    for draw in draws:
        data.append({
            'id': draw.id,
            'draw_id': draw.draw_id,
            'Date': draw.date.isoformat(),
            'N1': draw.numbers[0] if len(draw.numbers) > 0 else None,
            'N2': draw.numbers[1] if len(draw.numbers) > 1 else None,
            'N3': draw.numbers[2] if len(draw.numbers) > 2 else None,
            'N4': draw.numbers[3] if len(draw.numbers) > 3 else None,
            'N5': draw.numbers[4] if len(draw.numbers) > 4 else None,
            'E1': draw.stars[0] if len(draw.stars) > 0 else None,
            'E2': draw.stars[1] if len(draw.stars) > 1 else None,
            'has_winner': draw.has_winner
        })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)

    logger.info("export_complete", path=output_path, rows=len(data))
    print(f"✓ Exported {len(draws)} draws to {output_path}")

    return output_path
