import datetime
from typing import Dict, Any, Union, Optional, TYPE_CHECKING
from .enums import MessageEventsTypeEnum, MessageTypeEnum
from .user import User

if TYPE_CHECKING:
    from .http import HTTPClient

class Message:
    """Represent the base Message of all Message types in twitter, this include DirrectMessage & Tweet 
    Version Added: 1.2.0

    Parameters:
    -----------
    text: Optional[str]
        The messages's text.

    id: Union[str, int]
        The messages's ID.
    """
    def __init__(self, text: Optional[str], id: Union[str, int]):
        self.text = text
        self.id = id

class DirectMessage(Message):
    """Represent a Direct Message in twitter.
    Version Added: 1.2.0

    Paramaters:
    -----------

    data: Dict[str, Any]
        The message data keep inside a dictionary.

    http_client: Optional[HTTPClient]
        The http client that made the request.
    """
    def __init__(self, data: Dict[str, Any], **kwargs):
        self.original_payload=data
        self._payload = data.get('event', None)
        self.message_create = self._payload.get('message_create', None)
        self.message_data = self.message_create.get('message_data', None)
        self.entities = self.message_data.get("entities", None)

        super().__init__(self.message_data.get('text'), self._payload.get('id'))
        self.http_client: HTTPClient = kwargs.get('http_client', None)

    def __repr__(self) -> str:
        return "Message(text:{0.text} id:{0.id} author: {0.author})"

    def __str__(self) -> str:
        return self.text

    @property
    def event_type(self):
        return MessageEventsTypeEnum(self._payload.get("type", None))

    @property
    def type(self):
        return MessageTypeEnum(1)

    @property
    def author(self) -> User:
        if not self.http_client:
            return None

        user_id=self.message_create.get("target").get("recipient_id")
        user=self.http_client.fetch_user(user_id, self.http_client)
        return user

    @property
    def created_at(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(float(self._payload.get("created_timestamp")))    