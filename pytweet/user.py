import datetime
from typing import TYPE_CHECKING, Any, Dict, List, NoReturn, Optional, TypeVar, Union

from .metrics import UserPublicMetrics
from .utils import time_parse_todt

if TYPE_CHECKING:
    from .http import HTTPClient


U = TypeVar("U", bound="User")


class Messageable:
    """Represent an object that can send and receive a message through DM.
    Version Added: 1.0.0

    Parameters:
    -----------
    data: Dict[str, Any]
        The complete data of a Messageable object.

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
        Version Added: 1.1.0
        """
        res = self.http_client.send_message(self._payload.get("id"), text, **kwargs)
        return res

    def delete_message(self, message_id: int, **kwargs: Any) -> None:
        """Delete a message from a Messageable object.
        Version Added: 1.1.0
        """
        self.http_client.delete_message(self._payload.get("id"), message_id, **kwargs)

    def follow(self) -> None:
        """Follow a Messageable object.
        Version Added: 1.1.0
        """
        follow = self.http_client.follow_user(self._payload.get("id"))
        return follow

    def unfollow(self) -> None:
        """Unfollow a Messageable object.
        Version Added: 1.1.0
        """
        unfollow = self.http_client.unfollow_user(self._payload.get("id"))
        return unfollow

    def block(self) -> None:
        """Block a Messageable object.
        Version Added: 1.2.0
        """
        self.http_client.block_user(self._payload.get("id"))

    def unblock(self) -> None:
        """Unblock a Messageable object.
        Version Added: 1.2.0
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


    Parameters:
    -----------
    data: Dict[str, Any]
        The complete data of the user through a dictionary in a dictionary.

    Attributes:
    -----------
    original_payload
        Represent the main data of a user.

    http_client
        Represent a :class:HTTPClient that make the request.

    user_metrics
        Represent the public metrics of the user.

    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any) -> None:
        super().__init__(data, **kwargs)
        self.original_payload = data
        self._payload = (
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
        """str: Return the user's name."""
        return self._payload.get("name")

    @property
    def username(self) -> str:
        """str: Return the user's username, this usually start with '@' follow by their username."""
        return "@" + self._payload.get("username")

    @property
    def id(self) -> int:
        """int: Return the user's id."""
        return self._payload.get("id")

    @property
    def bio(self) -> str:
        """str: Return the user's bio."""
        return self._payload.get("description")

    @property
    def description(self) -> str:
        """str: an alias to User.bio"""
        return self._payload.get("description")

    @property
    def profile_link(self) -> str:
        """str: Return the user's profile link"""
        return f"https://twitter.com/{self.username.replace('@', '', 1)}"

    @property
    def link(self) -> str:
        """str: Return url where the user put links, return an empty string if there isnt a url"""
        return self._payload.get("url")

    @property
    def verified(self) -> bool:
        """bool: Return True if the user is verified account, else False."""
        return self._payload.get("verified")

    @property
    def protected(self) -> bool:
        """bool: Return True if the user is protected, else False."""
        return self._payload.get("protected")

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[str]: Return the user profile image."""
        return self._payload.get("profile_image_url")

    @property
    def location(self) -> Optional[str]:
        """str: Return the user's location"""
        return self._payload.get("location")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:datetime.datetime: Return datetime.datetime object with the user's account date."""
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def pinned_tweet(self) -> Optional[object]:
        """Optional[object]: Returns the user's pinned tweet.
        Version Added: 1.1.3"""

        id = self._payload.get("pinned_tweet_id")
        return None if not id else self.http_client.fetch_tweet(int(id), http_client=self.http_client)

    @property
    def followers(self) -> Union[List[U], List]:
        """:class:`List[User]`: Returns a list of users who are followers of the specified user ID. Maximum users is 100 users."""
        return self._payload.get("followers")

    @property
    def following(self) -> Union[List[U], List]:
        """:class:`List[User]`: Returns a list of users thats followed by the specified user ID. Maximum users is 100 users."""
        return self._payload.get("following")

    @property
    def follower_count(self) -> int:
        """int: Return total of followers that a user has."""
        return self._metrics.follower_count

    @property
    def following_count(self) -> int:
        """int: Return total of following that a user has."""
        return self._metrics.following_count

    @property
    def tweet_count(self) -> int:
        """int: Return total of tweet that a user has."""
        return self._metrics.tweet_count

    @property
    def listed_count(self) -> int:
        """int: Return total of listed that a user has."""
        return self._metrics.listed_count
