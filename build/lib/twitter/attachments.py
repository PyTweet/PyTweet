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
from dateutil import parser
from typing import Dict, List, Any

class Media:
    """
    Represent a Media attachment in a tweet.

    Parameters:
    ===================
    data: Dict[str, Any] -> The full data of the media in a dictionary. 

    Attributes:
    ====================
    :property: type: str -> Return the media's type.

    :property: url: str -> Return the media's url.

    :property: width: int -> Return the media's width. 

    :property: height: int -> Return the media's height.

    :property: media_key: str -> Return the media's unique key.
    """
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def type(self) -> str:
        return self._payload.get("type")

    @property
    def url(self) -> str:
        return self._payload.get("url")

    @property
    def width(self) -> int:
        return self._payload.get("width")

    @property
    def height(self) -> int:
        return self._payload.get("height")

    @property
    def media_key(self) -> str:
        return self._payload.get("media_key")

class PollOptions:
    def __init__(self, options: List[dict]):
        self.position = options.get("position")
        self.label = options.get("label")
        self.votes = options.get("votes")


class Poll:
    """
    Represent a Poll attachment in a tweet.

    Parameters:
    ===================
    data: Dict[str, Any] -> The full data of the poll in a dictionary. 

    Attributes:
    ====================
    :property: id: int -> Return the poll unique ID.

    :property: options: List[PollOptions] -> Return a list of :class: PollOptions 

    :property: voting_status: bool -> Return True if the poll is still open for voting, if its closed it return False

    :property: duration: int -> Return the poll duration in seconds.

    :property: end_date: datetime.datetime -> Return the end date in datetime.datetime object. 
    """
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def id(self) -> int:
        return int(self._payload.get("id"))

    @property
    def options(self) -> List[PollOptions]:
        return [PollOptions(option) for option in self._payload.get("options")]

    @property
    def voting_status(self) -> bool:
        return True if self._payload.get("voting_status") == "open" else False

    @property
    def duration(self) -> int:
        return self._payload.get("duration_minutes") * 60

    @property
    def end_date(self) -> datetime.datetime:
        date = str(parser.parse(self._payload.get("end_datetime")))
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