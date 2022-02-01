from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from .app import ApplicationInfo
from .attachments import CTA, File, QuickReply
from .entities import Hashtag, Symbol, Url, UserMention
from .enums import MessageEventTypeEnum, MessageTypeEnum
from .user import User

if TYPE_CHECKING:
    from .http import HTTPClient
    from .type import ID

__all__ = ("Message", "DirectMessage", "WelcomeMessage", "WelcomeMessageRule")


class Message:
    """Represents the base Message of all Message types in Twitter.

    .. versionadded:: 1.2.0
    """

    __slots__ = ("_text", "_id", "_type")

    def __init__(self, text: Optional[str], id: ID, type: int):
        self._text = text
        self._id = id
        self._type = type

    def __repr__(self) -> str:
        return "Message(text={0.text} id={0.id})".format(self)

    @property
    def text(self) -> str:
        """:class:`str`: Returns the message's text.

        .. versionadded:: 1.2.0
        """
        return self._text

    @property
    def id(self) -> int:
        """:class:`int`: Returns the message's id, or if its a direct message it returns an event id.

        .. versionadded:: 1.2.0
        """
        return int(self._id)

    @property
    def type(self) -> MessageTypeEnum:
        """:class:`MessageTypeEnum`: Returns the message's type.

        .. versionadded:: 1.2.0
        """
        return MessageTypeEnum(self._type)


class DirectMessage(Message):
    """Represents a Direct Message in Twitter.

    .. versionadded:: 1.2.0
    """

    __slots__ = (
        "__original_payload",
        "_payload",
        "__message_create",
        "__message_data",
        "__entities",
        "_quick_reply_data",
        "_cta_data",
        "http_client",
    )

    def __init__(self, data: Dict[str, Any], *, http_client: HTTPClient):
        self.__original_payload = data
        self._payload = data.get("event", None)
        self.__message_create = self._payload.get("message_create", None)
        self.__message_data = self.__message_create.get("message_data", None)
        self.__entities = self.__message_data.get("entities", None)
        self._quick_reply_data = self.__message_data.get("quick_reply")
        self._cta_data = self.__message_data.get("ctas")
        self.http_client = http_client
        super().__init__(self.__message_data.get("text"), self._payload.get("id"), 0)

    def __repr__(self) -> str:
        return "DirectMessage(text={0.text} id={0.id} recipient={0.recipient})".format(self)

    @property
    def event_type(self) -> MessageEventTypeEnum:
        """:class:`MessageEventTypeEnum`: Returns the message event type.

        .. versionadded:: 1.2.0
        """
        return MessageEventTypeEnum(self._payload.get("type", None))

    @property
    def recipient(self) -> User:
        """:class:`User`: Returns the user that received the direct message.

        .. versionadded:: 1.2.0
        """
        return self.__message_create.get("target", {}).get("recipient")

    @property
    def author(self) -> Optional[User]:
        """:class:`User`: Returns the user that sent the direct message.

        .. versionadded:: 1.5.0
        """
        return self.__message_create.get("target", {}).get("sender", None)

    @property
    def application_info(self) -> Optional[ApplicationInfo]:
        """:class:`ApplicationInfo`: Returns the direct messages's source application info if there is, else it return None.

        .. versionadded:: 1.5.0
        """
        return self.__message_create.get("target", {}).get("application_info", None)

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the time when the Direct Message event was created.

        .. versionadded:: 1.2.0
        """
        return datetime.datetime.fromtimestamp(int(self._payload.get("created_timestamp")) / 1000)

    @property
    def hashtags(self) -> Optional[List[Hashtag]]:
        """List[:class:`Hashtag`]: Returns the messages's hashtags.

        .. versionadded:: 1.2.0
        """
        return [Hashtag(data) for data in self.__entities.get("hashtag")]

    @property
    def symbols(self) -> Optional[List[Symbol]]:
        """List[:class:`Symbol`]: Returns the messages's symbols.

        .. versionadded:: 1.2.0
        """
        return [Symbol(data) for data in self.__entities.get("symbols")]

    @property
    def mentions(self) -> Optional[List[UserMention]]:
        """List[:class:`UserMention`]: Returns the messages mentioned users.

        .. versionadded:: 1.2.0
        """
        return [UserMention(data) for data in self.__entities.get("user_mentions")]

    @property
    def urls(self) -> Optional[List[Url]]:
        """List[:class:`Url`]: Returns the message's urls.

        .. versionadded:: 1.2.0
        """
        return [Url(data) for data in self.__entities.get("urls")]

    @property
    def quick_reply(self) -> Optional[QuickReply]:
        """Optional[:class:`QuickReply`]: Returns the quick reply attachment in a message, if none found it return None.

        .. versionadded:: 1.3.5
        """
        if self._quick_reply_data and self._quick_reply_data.get("options"):
            attachment = QuickReply(self._quick_reply_data.get("type"))
            for option in self._quick_reply_data.get("options"):
                attachment.add_option(**option)
            return attachment
        return None

    @property
    def quick_reply_response(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the metadata of the quick reply option that the author clicked.

        .. versionadded:: 1.5.0
        """
        return self.__message_data.get("quick_reply_response", {}).get("metadata", None)

    @property
    def cta(self) -> Optional[CTA]:
        """Optional[:class:`CTA`]: Returns the message's cta attachment.

        .. versionadded:: 1.3.5
        """
        if self._cta_data:
            attachment = CTA()
            for button in self._cta_data:
                attachment.add_button(**button)
            return attachment
        return None

    def delete(self) -> None:
        """Delete the direct message.

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


class WelcomeMessage(Message):
    """Represents a Welcome Message in a Direct Message.


    .. versionadded:: 1.3.5
    """

    __slots__ = ("_name", "_timestamp", "http_client")

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        text: str,
        id: ID,
        timestamp: str,
        http_client: HTTPClient,
    ):
        super().__init__(text, id, 2)
        self._name = name
        self._timestamp = timestamp
        self.http_client = http_client

    def __repr__(self) -> str:
        return "WelcomeMessage(text={0.text} id={0.id})".format(self)

    @property
    def name(self) -> str:
        """:class:`str`: Returns the welcome message's name.

        .. versionadded:: 1.3.5
        """
        return self._name

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the welcome message created date.

        .. versionadded:: 1.3.5
        """
        return datetime.datetime.fromtimestamp(int(self._timestamp) / 1000)

    def set_rule(self) -> WelcomeMessageRule:
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

    def update(
        self,
        *,
        text: Optional[str] = None,
        file: Optional[File] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> WelcomeMessage:
        """Updates the Welcome Message, you dont need to use set_rule again since this update your default welcome message.

        Parameters
        -----------
        text: Optional[:class:`str`]
            The welcome message main text
        file: Optional[:class:`File`]:
            Represents a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
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
        return self.http_client.update_welcome_message(
            welcome_message_id=self.id, text=text, file=file, quick_reply=quick_reply, cta=cta
        )

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


class WelcomeMessageRule(Message):
    """Represents a Welcome Message Rule in a Direct Message. This object is returns by WelcomeMessage.set_rule or client.fetch_welcome_message_rules, it determines which Welcome Message will be shown in a given conversation.


    .. versionadded:: 1.3.5
    """

    __slots__ = ("_welcome_message_id", "_timestamp", "http_client")

    def __init__(
        self,
        id: ID,
        welcome_message_id: ID,
        timestamp: ID,
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

    @property
    def welcome_message_id(self) -> ID:
        """:clasD`: Returns the welcome message's id.

        .. versionadded:: 1.3.5
        """
        return int(self._welcome_message_id)

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the WelcomeMessageRule created time.

        .. versionadded:: 1.3.5
        """
        return datetime.datetime.fromtimestamp(int(self._timestamp) / 1000)

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

    def fetch_welcome_message(self) -> Optional[WelcomeMessage]:
        """A method for fetching the welcome message rule's welcome message. An equivalent to :meth:`Client.fetch_welcome_message`.

        Returns
        ---------
        Optional[:class:`WelcomeMessage`]
            This method returns a :class:`WelcomeMessage` object.


        .. versionadded:: 1.5.0
        """
        return self.http_client.fetch_welcome_message(self.welcome_message_id)