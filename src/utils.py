"""
Utils part of the krema.
"""

from datetime import datetime
from os.path import basename


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

    Examples:
        >>> krema.utils.dict_to_query({"hello": "world", "int": 1})
        "?hello=world&int=1"
    """

    if len(data) == 0:
        return ""

    return f"?{'&'.join(f'{key}={value}' for key, value in data.items())}"


def file_builder(path: str) -> dict:
    """File builder is a function that helps you while sending files.
    
    Args:
        path (str): File path.

    Returns:
        dict: Converted version for discord API.

    Examples:
        >>> krema.utils.file_builder("./path/to/file.txt")
        {
            "name": "file",
            "value": b"hi",
            "filename": "file.txt",
            "content_type": "application/octet-stream"
        }
    """

    file = open(path, "rb")
    data, name = file.read(), file.name

    file.close()

    return {
        "name": "file",
        "value": data,
        "filename": basename(name),
        "content_type": "application/octet-stream"
    }
