from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .attachments import QuickReply
from .entities import Hashtags, Symbols, Urls, UserMentions
from .enums import MessageEventTypeEnum, MessageTypeEnum
from .user import User

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = ("Message", "DirectMessage", "WelcomeMessage", "WelcomeMessageRule")


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

    def __init__(self, text: Optional[str], id: Union[str, int], type: int):
        self._text = text
        self._id = id
        self._type = type

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

    @property
    def type(self) -> MessageTypeEnum:
        return MessageTypeEnum(self._type)


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

        super().__init__(self.message_data.get("text"), self._payload.get("id"), 0)
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client", None)
        self.timestamp = round(datetime.datetime.utcnow().timestamp())

    def __repr__(self) -> str:
        return "Message(text:{0.text} id:{0.id} author: {0.author})".format(self)

    def __str__(self) -> str:
        return self.text

    def delete(self) -> None:
        """Make a Request to delete the DirectMessage.

        Parameters
        -----------
        id:
            The Direct Message event id.


        .. versionadded:: 1.1.0
        """
        self.http_client.request(
            "DELETE",
            "1.1",
            f"/direct_messages/events/destroy.json?id={self.id}",
            auth=True,
        )

        try:
            self.http_client.message_cache.pop(int(self.id))
        except KeyError:
            pass

    def mark_read(self):
        """Mark the DirectMessage as read, it also mark other messages before the message was sent as read.

        .. versionadded:: 1.3.5
        """
        self.http_client.request(
            "POST",
            "1.1",
            "/direct_messages/mark_read.json",
            params={
                "last_read_event_id": str(self.id),
                "recipient_id": str(self.author.id),
            },
            auth=True,
        )

    @property
    def event_type(self) -> MessageEventTypeEnum:
        """:class:`MessageEventTypeEnum`: Returns the message event type.

        .. versionadded:: 1.2.0
        """
        return MessageEventTypeEnum(self._payload.get("type", None))

    @property
    def author(self) -> User:
        """:class:`User`: Returns the author of the message in User object.

        .. versionadded:: 1.2.0
        """
        user = self.message_create.get("target").get("recipient")
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


class WelcomeMessage(Message):
    """Represent a Welcome Message in a Direct Message.

    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        text: Optional[str] = None,
        welcome_message_id: Union[str, int],
        timestamp: str,
        http_client,
    ):
        super().__init__(text, welcome_message_id, 2)
        self._name = name
        self._timestamp = timestamp
        self.http_client = http_client

    def __repr__(self) -> str:
        return "WelcomeMessage(id: {0.id} name: {0.name} timestamp: {0._timestamp} created_at: {0.created_at})".format(
            self
        )

    def __str__(self) -> str:
        return self.text

    def set_rules(self) -> WelcomeMessageRule:
        """Set a new Welcome Message Rule that determines which Welcome Message will be shown in a given conversation. Returns the created rule if successful.

        .. versionadded:: 1.3.5
        """
        try:
            int(self.id)
        except Exception as e:
            raise e

        data = {"welcome_message_rule": {"welcome_message_id": str(self.id)}}

        res = self.http_client.request(
            "POST",
            "1.1",
            "/direct_messages/welcome_messages/rules/new.json",
            json=data,
            auth=True,
        )

        args = [v for k, v in res.get("welcome_message_rule").items()]
        return WelcomeMessageRule(args[0], args[2], args[1], http_client=self.http_client)

    def update(self, text: str = None, *, quick_reply: QuickReply = None) -> WelcomeMessage:
        """Updates the Welcome Message, you dont need to use set_rule again since this update your default welcome message.

        Parameters
        -----------
        text: :class:`str`
            The welcome message main text

        .. versionadded:: 1.3.5
        """
        data = {"message_data": {}}

        data["message_data"]["text"] = str(text)

        if quick_reply:
            data["message_data"]["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.options,
            }

        res = self.http_client.request(
            "PUT",
            "1.1",
            "/direct_messages/welcome_messages/update.json",
            params={"id": str(self.id)},
            json=data,
            auth=True,
        )

        welcome_message = res.get("welcome_message")
        message_data = welcome_message.get("message_data")

        name = res.get("name")
        id = welcome_message.get("id")
        timestamp = welcome_message.get("created_timestamp")
        text = message_data.get("text")

        return WelcomeMessage(name, text=text, welcome_message_id=id, timestamp=timestamp)

    def delete(self):
        """Delete the Welcome Message.

        .. versionadded:: 1.3.5
        """
        self.http_client.request(
            "DELETE",
            "1.1",
            "/direct_messages/welcome_messages/destroy.json",
            params={"id": str(self.id)},
            auth=True,
        )

    @property
    def created_at(self) -> datetime.datetime:
        timestamp = str(self._timestamp)[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def name(self) -> str:
        return self._name


class WelcomeMessageRule(Message):
    """Represent a Welcome Message Rule in a Direct Message. This object is returns by WelcomeMessage.set_rule or client.fetch_welcome_message_rules, it determines which Welcome Message will be shown in a given conversation.

    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        welcome_message_rule_id: Union[str, int],
        welcome_message_id: Union[str, int],
        timestamp: Union[str, int],
        *,
        http_client,
    ):
        super().__init__(id=welcome_message_rule_id, type=3)
        self._welcome_message_id = welcome_message_id
        self._timestamp = timestamp
        self.http_client = http_client

    def __repr__(self) -> str:
        return "WelcomeMessageRule(id: {0.id} welcome_message_id: {0.} created_at: {0.created_at})".format(self)

    def delete(self):
        """Delete the Welcome Message Rule.

        .. versionadded:: 1.3.5
        """
        self.http_client.request(
            "DELETE",
            "1.1",
            "/direct_messages/welcome_messages/rules/destroy.json",
            params={"id": str(self.id)},
            auth=True,
        )

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the WelcomeMessageRule created time."""
        timestamp = str(self._timestamp)[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def welcome_message_id(self) -> Union[str, int]:
        """Union[:class:`str`, :class:`int`]: Returns the welcome message's id."""
        return int(self._welcome_message_id)
