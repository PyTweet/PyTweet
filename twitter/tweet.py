"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
from typing import Optional, Dict, Any, List
from dateutil import parser
from .user import User
from .attachments import Poll, Media
from .metrics import TweetPublicMetrics

class Tweet:
    """
    Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of a tweet keep inside a dictionary.

    Attributes:
    ===================
    :property: text: str -> Return the tweet's text. 

    :property: id: int -> Return the tweet's id. 

    :property: author: Optional[User] -> Return a user (object) who posted the tweet. 

    :property: retweeted_by: Optional[List[User]] -> Return a list of users thats retweeted the specified tweet's id. Maximum user is 100. Return 0 if no one retweeted.

    :property: liking_users: Optional[List[User]] -> Return a list of users that liked the specified tweet's id. Maximum user is 100. Return 0 if no one retweeted.
    """
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data.get("data") or None
        self._includes = self.original_payload.get("includes")
        self._metrics = TweetPublicMetrics(self._payload.get("public_metrics"))
    
    @property
    def author(self) -> Optional[User]:
        return User(self._includes.get("users")[0])
    
    @property
    def text(self) -> str:
        return self._payload.get("text")

    @property
    def id(self) -> int:
        return self._payload.get("id")

    @property
    def retweeted_by(self) -> Optional[List[User]]:
        return self._payload.get("retweeted_by")

    @property
    def liking_users(self) -> Optional[List[User]]:
        return self._payload.get("liking_users")

    @property
    def sensitive(self):
        return self._payload.get("possibly_sensitive")

    @property
    def created_at(self) -> datetime.datetime:
        date = str(parser.parse(self._payload.get("created_at")))
        y, mo, d = date.split("-")
        h, mi, s = date.split(" ")[1].split("+")[0].split(":")

        return datetime.datetime(
            year=int(y),
            month=int(mo),
            day=int(d.split(" ")[0]),
            hour=int(h),
            minute=int(mi),
            second=int(s),
        )
        
    @property
    def source(self):
        return self._payload.get("source")

    @property
    def reply_setting(self):
        return self._payload.get("reply_settings")

    @property
    def lang(self):
        return self._payload.get("lang")

    @property
    def convertion_id(self):
        return self._payload.get("convertion_id")

    @property
    def polls(self) -> Poll:
        return [Poll(poll) for poll in self._includes.get('polls')]

    @property
    def media(self) -> Media:
        return [Media(img) for img in self._includes.get("media")]

    @property
    def like_count(self) -> int:
        return self._metrics.like_count

    @property
    def retweeted_count(self) -> int:
        return self._metrics.retweeted_count

    @property
    def reply_count(self) -> int:
        return self._metrics.reply_count

    @property
    def quote_count(self) -> int:
        return self._metrics.quote_count