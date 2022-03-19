from dataclasses import dataclass 
from typing import List, Optional

@dataclass
class EmbedImage:
    """Represents a dataclass for an embed image.

    .. versionadded: 1.1.3

    .. versionchanged: 1.5.0

        Made as a dataclass rather then a standalone class.
    """
    url: str
    width: int
    height: int

@dataclass
class Embed:
    """Represents a dataclass for embedded urls in a tweet.

    .. versionadded: 1.1.3

    
    .. versionchanged: 1.5.0

        Made as a dataclass rather then a standalone class.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    start: Optional[int] = None
    end: Optional[int] = None
    url: Optional[str] = None
    expanded_url: Optional[str] = None
    display_url: Optional[str] = None
    unwound_url: Optional[str] = None
    status_code: Optional[int] = None
    images: Optional[List[EmbedImage]] = None
