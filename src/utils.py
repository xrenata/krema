"""
Utils part of the krema.
"""

from datetime import datetime


def convert_iso(date: str) -> datetime:
    """Convert a ISO format to datetime object.

    Args:
        date (str): Valid ISO date.

    Returns:
        datetime: Converted object.
    """

    return datetime.fromisoformat(date)