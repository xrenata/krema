"""
Utils part of the krema.
"""

from datetime import datetime
from base64 import b64encode
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


def image_to_data_uri(path: str):
    """Convert a image / gif to Data URI format.

    Args:
        path (str): Path to image / gif.

    Returns:
        str: Formatted version.
    """
    with open(path, "rb") as f:
        img_bytes = f.read()
        encrypt = b64encode(img_bytes).decode()

        return f"data:image/{f.name.split('.')[-1].replace('jpg', 'jpeg')};base64,{encrypt}"

def paginate(text: str, max_len: int)-> list:
    """
    Simple generator that paginates text.

    Args:
        text (str): string.
        max_len (int): How long after the text will be cut.

    Returns:
        list: Array with fragmented text.
    """
    last = 0
    pages = []
    for curr in range(0, len(text)):
        if curr % max_len == 0:
            pages.append(text[last:curr])
            last = curr
            appd_index = curr
    if appd_index != len(text)-1:
        pages.append(text[last:curr])
    return [i for i in pages if i != ""]



