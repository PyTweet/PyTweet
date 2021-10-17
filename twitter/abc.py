from typing import Optional, Dict, Any, Protocol, runtime_checkable
from .errors import UnfinishFunctionError
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

    def send() -> Send a message to a specific user.

    """

    def __init__(self, data: Dict[str, Any], **kwargs):
        self._payload = data
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None

    def send(self, text: str = None, **kwargs) -> Optional[None]:
        self.http_client.send_message(text, **kwargs)
