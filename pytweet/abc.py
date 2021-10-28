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

from typing import Optional, Dict, Any, Protocol, TYPE_CHECKING, runtime_checkable

if TYPE_CHECKING:
    from .http import HTTPClient


@runtime_checkable
class Messageable(Protocol):
    """Represent an object that can send and receive a message through DM.
    Verion Added: 1.0.0

    Parameters:
    -----------
    data: Dict[str, Any]
        The complete data of a Messageable that can send and receive a message.

    Attributes:
    -----------
    http_client: Optional[HTTPClient]
        The HTTPClient that make the request.
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any):
        self._payload = data
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None

    def send(self, text: str = None, **kwargs: Any) -> None:
        """Send a message to a specific Messageable object.
        Verion Added: 1.1.0
        """
        self.http_client.send_message(self._payload.get("id"), text, **kwargs)

    def delete_message(self, message_id: int, **kwargs: Any) -> None:
        """Delete a message from a Messageable object.
        Verion Added: 1.1.0
        """
        self.http_client.delete_message(self._payload.get("id"), message_id, **kwargs)

    def follow(self) -> None:
        """Follow a Messageable object.
        Verion Added: 1.1.0
        """
        self.http_client.follow_user(self._payload.get("id"))

    def unfollow(self) -> None:
        """Unfollow a Messageable object.
        Verion Added: 1.1.0
        """
        self.http_client.unfollow_user(self._payload.get("id"))

    def block(self) -> None:
        """Block a Messageable object.
        Verion Added: 1.2.0
        """
        self.http_client.block_user(self._payload.get("id"))

    def unblock(self) -> None:
        """Unblock a Messageable object.
        Verion Added: 1.2.0
        """
        self.http_client.unblock_user(self._payload.get("id"))
