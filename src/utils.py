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


def dict_to_query(data: dict) -> str:
    """Convert a dictionary to the query string.

    Args:
        data (dict): The dictionary object will be converted.

    Returns:
        str: Converted version.
    """

    if len(data) == 0:
        return ""

    return f"?{'&'.join(f'{key}={value}' for key, value in data.items())}"
