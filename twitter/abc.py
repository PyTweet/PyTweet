from typing import Optional, Dict, Any, Protocol, runtime_checkable
from .http import HTTPClient


@runtime_checkable
class Messageable(Protocol):
    """
    Represent an object that can send and receive a message through DM.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of an object that can send and receive a message.

    http_client: Optional[Client] -> The HTTPClient that make the request for sending messages.

    Functions:
    ===================

    def send() -> Send a message to a specific Messageable object.
    
    def delete_message() -> Delete a message from a Messageable object.
    
    def follow() -> Follow a Messageable object.
    
    def unfollow() -> Unfollow a Messageable object.

    """

    def __init__(self, data: Dict[str, Any], **kwargs):
        self._payload = data
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None

    def send(self, text: str = None, **kwargs) -> Optional[None]:
        self.http_client.send_message(text, **kwargs)

    def delete_message(self, id: int, **kwargs):
        self.http_client.delete_message(id, kwargs)

    def follow(self, **kwargs):
        self.http_client.follow_user(self._payload.get('id'), kwargs)

    def unfollow_user(self, **kwargs):
        self.http_client.unfollow_user(self._payload.get('id'), kwargs)