from datetime import datetime

from htranslate import translate_to_h, translate_from_h


def from_datetime(dt: datetime, delimiter: str = ":") -> str:
    """Create an h encoded time string from a datetime object.

    Args:
        dt (datetime): The datetime object to use.
        delimiter (str, optional): The character delimiter for the encoding. Defaults to ":".

    Returns:
        str: The h encoded time string.
    """

    return translate_to_h(dt.isoformat(), delimiter=delimiter)

def to_datetime(hs: str, delimiter: str = ":") -> datetime:
    """Create a datetime object from a given h encoded time string.

    Args:
        hs (str): The h encoded time string to decode.
        delimiter (str, optional): The character delimiter for the encoding. Defaults to ":".

    Returns:
        datetime: The constructed datetime object.
    """

    return datetime.fromisoformat(translate_from_h(hs, delimiter=delimiter))


__all__ = (
    "from_datetime",
    "to_datetime",
)
