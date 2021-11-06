import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    NoReturn,
    Optional,
    TypeVar,
    Union,
)


from .metrics import UserPublicMetrics
from .relations import RelationFollow
from .utils import time_parse_todt
from .attachments import QuickReply

if TYPE_CHECKING:
    from .http import HTTPClient

U = TypeVar("U", bound="User")


class Messageable:
    """Represent an object that can send and receive a message through DM.

    .. versionadded: 1.0.0
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any):
        self._payload: Dict[str, Any] = data
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client", None)

    def send(self, text: str = None, *, quick_reply: QuickReply = None):
        """:class:`DirectMessage`: Send a message to a specific Messageable object.

        Parameters:
        -----------
        text: str
            The text that will be send to that user.

        This function return a :class:`DirectMessage` object

        .. versionadded:: 1.1.0
        """
        res = self.http_client.send_message(
            self._payload.get("id"),
            text,
            quick_reply=quick_reply,
            http_client=self.http_client,
        )
        return res

    def fetch_message(self, event_id: Union[str, int]) -> object:
        """Get a message from a Messageable object.
        
        .. warning::
            This method use api call and might cause ratelimit if use often! You can instead use :class:`Client().get_message()` which get the message through the client message cache. As of right now, only the client's message thats going to be store in the cache!

        Parameters:
        -----------
        event_id: int
            The event id. Every time a Direct Message is created, its going to return a unique ID called event id.


        .. versionadded:: 1.2.0
        """
        res = self.http_client.get_message(event_id)
        return res

    def follow(self) -> RelationFollow:
        """:class:`RelationFollow`: Follow a Messageable object.

        This function return a :class:`RelationFollow` object.

        .. versionadded:: 1.1.0
        """
        follow = self.http_client.follow_user(self._payload.get("id"))
        return follow

    def unfollow(self) -> RelationFollow:
        """:class:`RelationFollow`: Unfollow a Messageable object.

        .. versionadded: 1.1.0

        This function return a :class:`RelationFollow` object.

        .. versionadded:: 1.1.0
        """
        unfollow = self.http_client.unfollow_user(self._payload.get("id"))
        return unfollow

    def block(self) -> None:
        """Block a Messageable object.

        .. versionadded:: 1.1.0
        """
        self.http_client.block_user(self._payload.get("id"))

    def unblock(self) -> None:
        """Unblock a Messageable object.

        .. versionadded:: 1.1.0
        """
        self.http_client.unblock_user(self._payload.get("id"))


class User(Messageable):
    """Represent a user in Twitter.
    User is an identity in twitter, its very interactive. Can send message, post a tweet, and even send messages to other user through Dms.

    .. describe:: x == y
        Check if one user id is equal to another.


    .. describe:: x != y
        Check if one user id is not equal to another.


    .. describe:: str(x)
        Get the user's name.

    .. versionadded: 1.0.0
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(data, **kwargs)
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = (
            self.original_payload.get("data") if self.original_payload.get("data") != None else self.original_payload
        )
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None
        self._metrics = UserPublicMetrics(self._payload) if self._payload != None else self.original_payload

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return "User(name={0.name} username={0.username} id={0.id})".format(self)

    def __eq__(self, other: U) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid User object")
        return self.id == other.id

    def __ne__(self, other: U) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid User object")
        return self.id != other.id

    @property
    def name(self) -> str:
        """str: Return the user's name.

        .. versionadded: 1.0.0
        """
        return self._payload.get("name")

    @property
    def username(self) -> str:
        """str: Return the user's username, this usually start with '@' follow by their username.

        .. versionadded: 1.0.0
        """
        return "@" + self._payload.get("username")

    @property
    def id(self) -> int:
        """int: Return the user's id.

        .. versionadded: 1.0.0
        """
        return int(self._payload.get("id"))

    @property
    def bio(self) -> str:
        """str: Return the user's bio.

        .. versionadded: 1.0.0
        """
        return self._payload.get("description")

    @property
    def description(self) -> str:
        """str: an alias to User.bio.

        .. versionadded: 1.0.0
        """
        return self._payload.get("description")

    @property
    def profile_link(self) -> str:
        """str: Return the user's profile link

        .. versionadded: 1.0.0
        """
        return f"https://twitter.com/{self.username.replace('@', '', 1)}"

    @property
    def link(self) -> str:
        """str: Return url where the user put links, return an empty string if there isn't a url

        .. versionadded: 1.0.0
        """
        return self._payload.get("url")

    @property
    def verified(self) -> bool:
        """bool: Return True if the user is verified account, else False.

        .. versionadded: 1.0.0
        """
        return self._payload.get("verified")

    @property
    def protected(self) -> bool:
        """bool: Return True if the user is protected, else False.

        .. versionadded: 1.0.0
        """
        return self._payload.get("protected")

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[str]: Return the user profile image.

        .. versionadded: 1.0.0
        """
        return self._payload.get("profile_image_url")

    @property
    def location(self) -> Optional[str]:
        """str: Return the user's location

        .. versionadded: 1.0.0
        """
        return self._payload.get("location")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:datetime.datetime: Return datetime.datetime object with the user's account date.

        .. versionadded: 1.0.0
        """
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def pinned_tweet(self) -> Optional[object]:
        """Optional[object]: Returns the user's pinned tweet.

        .. versionadded: 1.1.3
        """
        id = self._payload.get("pinned_tweet_id")
        return None if not id else self.http_client.fetch_tweet(int(id), http_client=self.http_client)

    @property
    def followers(self) -> Union[List[U], List]:
        """:class:`List[User]`: Returns a list of users who are followers of the specified user ID. Maximum users is 100 users.

        .. versionadded: 1.1.0
        """
        return self._payload.get("followers")

    @property
    def following(self) -> Union[List[U], List]:
        """:class:`List[User]`: Returns a list of users that's followed by the specified user ID. Maximum users is 100 users.

        .. versionadded: 1.1.0
        """
        return self._payload.get("following")

    @property
    def follower_count(self) -> int:
        """int: Return total of followers that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.follower_count

    @property
    def following_count(self) -> int:
        """int: Return total of following that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.following_count

    @property
    def tweet_count(self) -> int:
        """int: Return total of tweet that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.tweet_count

    @property
    def listed_count(self) -> int:
        """int: Return total of listed that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.listed_count
