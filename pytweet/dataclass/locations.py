from dataclasses import dataclass
from typing import Optional


@dataclass
class PlaceType:
    code: int
    name: str


@dataclass
class Location:
    country: str
    countryCode: str
    name: str
    parent_id: int
    placeType: PlaceType
    url: str
    woeid: int


@dataclass
class Trend:
    name: str
    url: str
    promoted_content: Optional[str]
    query: str
    tweet_volume: Optional[str]


@dataclass
class TimezoneInfo:
    name: str
    name_info: str
    utc_offset: int
