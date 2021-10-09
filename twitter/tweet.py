from .user import User
from typing import Optional, Dict, Any

class Tweet:
    """
    Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of a tweet keep inside a dictionary.

    Attributes:
    ===================
    :property: author: Optional[User] -> Return a user (object) who posted the tweet.

    :property: text: str -> Return the tweet's text. 
    
    :property: id: int -> Return the tweet's id. 
    """
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data['data']
    
    @property
    def author(self) -> Optional[User]:
        return User(self.original_payload.get("includes").get("users")[0])
    #)
    @property
    def text(self) -> str:
        return self._payload.get('text')

    @property
    def id(self) -> int:
        return self._payload.get('id')