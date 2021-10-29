"""
The MIT License (MIT)

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

from typing import Dict, Any
from .enums import RelationsTypeEnum

class RelationFollow:
    """Represent the follow relation from a follow request.
    Version Added: 1.2.0

    Parameters
    -----------
    data: Payload
        The data of the relations

    Attributes
    -----------

    original_payload
        The data paramater.

    _payload
        The data paramater in data key.
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data["data"]

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return "Followed(type: {0.type} following: {0.following} pending: {0.pending})".format(self)

    @property
    def pending(self) -> bool:
        """bool: Check if the relation is pending."""
        return self._payload.get("pending", False)

    @property
    def following(self) -> bool:
        """bool: Check if the relation is following."""
        return self._payload.get("following", False)

    @property
    def type(self):
        """RelationType: Check what relation type it is."""
        return RelationsTypeEnum(1 if self._payload["following"] else 0)
