"""Utilities module."""
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Optional

from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    """Custom JSON encoder."""

    def default(self, obj: Any) -> Any:
        """Convert `obj` to a JSON serializable type. Overrides the default
        `JSONEncoder` of `Flask`.
        """
        if isinstance(obj, date):
            return obj.isoformat() + ("Z" if isinstance(obj, datetime) else "")
        return super().default(obj)


def datetime_format(value: date, format: Optional[str] = None):
    format = format or (
        "%Y-%m-%dT%H:%M:%S%z" if isinstance(value, datetime) else "%Y-%m-%d"
    )
    return value.strftime(format)


@dataclass
class URL:
    loc: str
    lastmod: Optional[date] = None
    changefreq: Optional[str] = None
    priority: Optional[float] = None
