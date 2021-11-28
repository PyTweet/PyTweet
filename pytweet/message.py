from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .attachments import QuickReply, CTA, File
from .entities import Hashtags, Symbols, Urls, UserMentions
from .enums import MessageEventTypeEnum, MessageTypeEnum
from .user import User

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = ("Message", "DirectMessage", "WelcomeMessage", "WelcomeMessageRule")


class Message:
    """Represents the base Message of all Message types in Twitter.

    Parameters
    ------------
    text: Optional[:class:`str`]
        The messages's text.
    id: Union[:class:`str`, :class:`int`]
        The messages's unique ID.
    type: :class:`int`.
        The message's type in int form, it will get form to MessageTypeEnum.


    .. versionadded:: 1.2.0
    """

    if TYPE_CHECKING:
        _text: Optional[str]
        _id: Union[str, int]
        _type: int

    def __init__(self, text: Optional[str], id: Union[str, int], type: int):
        self._text = text
        self._id = id
        self._type = type

    def __repr__(self) -> str:
        return "Message(text={0.text} id={0.id})".format(self)

    def __str__(self) -> str:
        return self.text

    @property
    def text(self) -> str:
        """:class:`str`: Returns the message's text.

        .. versionadded:: 1.3.5
        """
        return self._text

    @property
    def id(self) -> int:
        """:class:`int`: Returns the message's id.

        .. versionadded:: 1.3.5
        """
        return int(self._id)

    @property
    def type(self) -> MessageTypeEnum:
        """:class:`MessageTypeEnum`: Returns the message's type.

        .. versionadded:: 1.3.5
        """
        return MessageTypeEnum(self._type)


class DirectMessage(Message):
    """Represents a Direct Message in Twitter.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any], *, http_client: HTTPClient):
        self.original_payload = data
        self._payload = data.get("event", None)
        self.message_create = self._payload.get("message_create", None)
        self.message_data = self.message_create.get("message_data", None)
        self.entities = self.message_data.get("entities", None)
        self.quick_reply_data = self.message_data.get("quick_reply")
        self.cta_data = self.message_data.get("ctas")

        super().__init__(self.message_data.get("text"), self._payload.get("id"), 0)
        self.http_client = http_client
        self.timestamp = round(datetime.datetime.utcnow().timestamp())

    def __repr__(self) -> str:
        return "DirectMessage(text={0.text} id={0.id} recipient={0.recipient})".format(self)

    def __str__(self) -> str:
        return self.text

    def delete(self) -> None:
        """Make a Request to delete the DirectMessage.

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

    def mark_read(self) -> None:
        """Mark the DirectMessage as read, it also mark other messages before the DirectMessage was sent as read.

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
    def recipient(self) -> User:
        """:class:`User`: Returns the recipient that received the message.

        .. versionadded:: 1.2.0
        """
        return self.message_create.get("target").get("recipient")

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
        """List[:class:`UserMentions`]: Returns the messages usermentions.

        .. versionadded:: 1.2.0
        """
        return [UserMentions(data) for data in self.entities.get("user_mentions")]

    @property
    def urls(self) -> Optional[List[Urls]]:
        """List[:class:`Urls`]: Returns the message's urls.

        .. versionadded:: 1.2.0
        """
        return [Urls(data) for data in self.entities.get("urls")]

    @property
    def quick_reply(self) -> Optional[QuickReply]:
        """Optional[:class:`QuickReply`]: Returns the quick reply attachment in a message, if none found it return None.

        .. versionadded:: 1.3.5
        """
        if self.quick_reply_data and self.quick_reply_data.get("options"):
            attachment = QuickReply(self.quick_reply_data.get("type"))
            for option in self.quick_reply_data.get("options"):
                attachment.add_option(**option)
            return attachment
        return None

    @property
    def cta(self) -> Optional[CTA]:
        """Optional[:class:`CTA`]: Returns the message's cta.

        .. versionadded:: 1.3.5
        """
        if self.cta_data:
            attachment = CTA()
            for button in self.cta_data:
                attachment.add_button(**button)
            return attachment
        return None


class WelcomeMessage(Message):
    """Represent a Welcome Message in a Direct Message.

    Parameters
    ------------
    name: Optional[:class:`str`]
        A human readable name for the Welcome Message.
    text: :class:`str`
        The welcome message main text.
    id: Union[:class:`str`, :class:`int`]
        The welcome message unique id.
    timestamp: Optional[:class:`str`]
        The welcome message timestamp.
    http_client: :class:`HTTPClient`
        The http client that make the request.


    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        text: str,
        id: Union[str, int],
        timestamp: str,
        http_client: HTTPClient,
    ):
        super().__init__(text, id, 2)
        self._name = name
        self._timestamp = timestamp
        self.http_client = http_client

    def __repr__(self) -> str:
        return "WelcomeMessage(text={0.text} id={0.id})".format(self)

    def __str__(self) -> str:
        return self.text

    def set_rule(self) -> WelcomeMessageRule:
        """Set a new Welcome Message Rule that determines which Welcome Message will be shown in a given conversation. Returns the created rule if successful.

        .. versionadded:: 1.3.5
        """
        try:
            int(self.id)
        except Exception as e:
            raise e

        data: Dict[str, Union[int, Dict[str, int]]] = {"welcome_message_rule": {"welcome_message_id": str(self.id)}}

        res: dict = self.http_client.request(
            "POST",
            "1.1",
            "/direct_messages/welcome_messages/rules/new.json",
            json=data,
            auth=True,
        )

        args: list = [v for k, v in res.get("welcome_message_rule").items()]
        return WelcomeMessageRule(args[0], args[2], args[1], http_client=self.http_client)

    def update(
        self,
        text: str = None,
        *,
        file: Optional[File] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> WelcomeMessage:
        """Updates the Welcome Message, you dont need to use set_rule again since this update your default welcome message.

        Parameters
        -----------
        text: :class:`str`
            The welcome message main text
        file: Optional[:class:`File`]:
            Represent a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
        quick_reply: Optional[:class:`QuickReply`]
            The message's :class:`QuickReply` attachments.
        cta: Optional[:class:`CTA`]
            The message's :class:`CTA` attachment.

        Returns
        ---------
        :class:`WelcomeMessage`
            Returns your :class:`WelcomeMessage` instance.


        .. versionadded:: 1.3.5
        """
        data = {"message_data": {}}
        message_data = data["message_data"]

        message_data["text"] = str(text)

        if file:
            media_id = self.http_client.upload(file, "INIT")
            self.http_client.upload(file, "APPEND", media_id=media_id)
            self.http_client.upload(file, "FINALIZE", media_id=media_id)
            message_data["attachment"] = {}
            message_data["attachment"]["type"] = "media"
            message_data["attachment"]["media"] = {}
            message_data["attachment"]["media"]["id"] = str(media_id)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        res = self.http_client.request(
            "PUT",
            "1.1",
            "/direct_messages/welcome_messages/update.json",
            params={"id": str(self.id)},
            json=message_data,
            auth=True,
        )

        welcome_message = res.get("welcome_message")
        message_data = welcome_message.get("message_data")

        name = res.get("name")
        id = welcome_message.get("id")
        timestamp = welcome_message.get("created_timestamp")
        text = message_data.get("text")

        return WelcomeMessage(name, text=text, id=id, timestamp=timestamp)

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
        """:class:`datetime.datetime`: Returns the welcome message created date.

        .. versionadded:: 1.3.5
        """
        timestamp = str(self._timestamp)[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def name(self) -> str:
        """:class:`str`: Returns the welcome message's name.

        .. versionadded:: 1.3.5
        """
        return self._name


class WelcomeMessageRule(Message):
    """Represent a Welcome Message Rule in a Direct Message. This object is returns by WelcomeMessage.set_rule or client.fetch_welcome_message_rules, it determines which Welcome Message will be shown in a given conversation.

    Parameters
    ------------
    id: Union[:class:`str`, :class:`int`]
        The welcome message rule unique id.
    welcome_message_id: Union[:class:`str`, :class:`int`]
        The welcome message unique id.
    timestamp: Optional[:class:`str`]
        The welcome message rule created timestamp.
    http_client: :class:`HTTPClient`
        The http client that make the request.


    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        id: Union[str, int],
        welcome_message_id: Union[str, int],
        timestamp: Union[str, int],
        *,
        http_client: HTTPClient,
    ):
        super().__init__(None, id=id, type=3)
        self._welcome_message_id = welcome_message_id
        self._timestamp = timestamp
        self.http_client = http_client

    def __repr__(self) -> str:
        return (
            "WelcomeMessageRule(id={0.id} welcome_message_id={0.welcome_message_id} created_at={0.created_at})".format(
                self
            )
        )

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
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the WelcomeMessageRule created time.

        .. versionadded:: 1.3.5
        """
        timestamp = str(self._timestamp)[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def welcome_message_id(self) -> Union[str, int]:
        """Union[:class:`str`, :class:`int`]: Returns the welcome message's id.

        .. versionadded:: 1.3.5
        """
        return int(self._welcome_message_id)
