import datetime
from typing import TYPE_CHECKING, Any, Dict, Optional, Union, List

from .enums import MessageEventTypeEnum, MessageTypeEnum
from .user import User
from .entities import Hashtags, Symbols, UserMentions, Urls

if TYPE_CHECKING:
    from .http import HTTPClient


__all__ = (
    "Message",
    "DirectMessage",
)


class Message:
    """Represents the base Message of all Message types in Twitter, this include DirrectMessage & Tweet

    Parameters
    ------------
    text: Optional[:class:`str`]
        The messages's text.

    id: Union[:class:`str`, :class:`int`]
        The messages's unique ID.

    .. versionadded:: 1.2.0
    """

    def __init__(self, text: Optional[str], id: Union[str, int]):
        self._text = text
        self._id = id

    def __repr__(self) -> str:
        return "Message(text: {0.text} id: {0.id})".format(self)

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        return self._text

    @property
    def id(self) -> int:
        return int(self._id)


class DirectMessage(Message):
    """Represents a Direct Message in Twitter.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any):
        self.original_payload = data
        self._payload = data.get("event", None)
        self.message_create = self._payload.get("message_create", None)
        self.message_data = self.message_create.get("message_data", None)
        self.entities = self.message_data.get("entities", None)

        super().__init__(self.message_data.get("text"), self._payload.get("id"))
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client", None)
        self.timestamp = round(datetime.datetime.utcnow().timestamp())

    def __repr__(self) -> str:
        return "Message(text:{0.text} id:{0.id} author: {0.author})"

    def __str__(self) -> str:
        return self.text

    def delete(self) -> None:
        """Delete a DirectMessage object.

        Parameters
        ------------
        event_id: :class:`int`
            The event id. Every time a Direct Message is created, its going to return a unique ID called event id.

        .. versionadded:: 1.1.0
        """
        self.http_client.delete_message(self.id)
        return None

    @property
    def event_type(self) -> MessageEventTypeEnum:
        """:class:`MessageEventTypeEnum`: Returns the message event type.

        .. versionadded:: 1.2.0
        """
        return MessageEventTypeEnum(self._payload.get("type", None))

    @property
    def type(self) -> MessageTypeEnum:
        """:class:`MessageTypesEnum`: Returns the message type.

        .. versionadded:: 1.2.0
        """
        return MessageTypeEnum(0)

    @property
    def author(self) -> User:
        """:class:`User`: Returns the author of the message in User object.

        .. versionadded:: 1.2.0
        """
        if not self.http_client:
            return None

        user_id = self.message_create.get("target").get("recipient_id")
        user = self.http_client.fetch_user(user_id, http_client=self.http_client)
        return user

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the time when the Direct Message event was created.

        .. versionadded:: 1.2.0
        """
        return datetime.datetime.fromtimestamp(self.timestamp)

    @property
    def hashtags(self) -> Optional[List[Hashtags]]:
        """List[:class:`Hashtags`]: Returns the messages's hashtags.

        .. versionadded:: 1.2.0
        """
        return [Hashtags(data) for data in self.entities.get("hashtags")]

    @property
    def symbols(self) -> Optional[List[Symbols]]:
        """List[:class:`Symbols`]: Returns the messages's hashtags.

        .. versionadded:: 1.2.0
        """
        return [Symbols(data) for data in self.entities.get("symbols")]

    @property
    def mentions(self) -> Optional[List[UserMentions]]:
        """List[:class:`UserMentions`]: Returns the messages usermetions.

        .. versionadded:: 1.2.0
        """
        return [UserMentions(data) for data in self.entities.get("user_mentions")]

    @property
    def urls(self) -> Optional[List[Urls]]:
        """List[:class:`Urls`]: Returns the message's urls.

        .. versionadded:: 1.2.0
        """
        return [Urls(data) for data in self.entities.get("urls")]
