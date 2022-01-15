from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Location:
    """Represents a Location that Twitter has trending topic information for.
    
    .. versionadded:: 1.5.0
    """
    country: str
    country_code: str
    name: str
    parent_id: int
    place_type: PlaceType
    url: str
    woeid: int


@dataclass
class Trend:
    """Represents a twitter's trending topics display as Trend.
    
    .. versionadded:: 1.5.0
    """
    name: str
    url: str
    promoted_content: Optional[str]
    query: str
    tweet_volume: Optional[str]


@dataclass
class TimezoneInfo:
    """Represents a TimezoneInfo for the user's setting.
    
    .. versionadded:: 1.5.0
    """
    name: str
    name_info: str
    utc_offset: int


@dataclass
class PlaceType:
    """Represents a place type consist of the code and name for :class:`Location`.
    
    .. versionadded:: 1.5.0
    """
    code: int
    name: str
