from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, NoReturn, Optional, Union

from .attachments import CTA, QuickReply
from .metrics import UserPublicMetrics
from .relations import RelationFollow
from .utils import time_parse_todt

if TYPE_CHECKING:
    from .http import HTTPClient


class User:
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

    def __eq__(self, other: User) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid User object")
        return self.id == other.id

    def __ne__(self, other: User) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid User object")
        return self.id != other.id

    def send(self, text: str = None, *, quick_reply: QuickReply = None, cta: CTA = None):
        """:class:`DirectMessage`: Send a message to the user.

        Parameters
        ------------
        text: :class:`str`
            The text that will be send to that user.
        quick_reply: :class:`QuickReply`
            The QuickReply attachment that will be send to a user.
        cta: :class:`CTA`
            cta or call-to-actions is use to make an action whenever a user 'call' something, a quick example is buttons.

        Returns
        ---------
        :class:`DirectMessage`
            This method return a :class:`DirectMessage` object.

        .. versionadded:: 1.1.0
        """
        res = self.http_client.send_message(
            self.id,
            text,
            quick_reply=quick_reply,
            cta=cta,
            http_client=self.http_client,
        )
        return res

    def follow(self) -> RelationFollow:
        """Make a Request to follow a User.

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to follow.

        This function return a :class: `RelationFollow` object.

        .. versionadded:: 1.1.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        res = self.http_client.request(
            "POST",
            "2",
            f"/users/{my_id}/following",
            json={"target_user_id": str(self.id)},
            auth=True,
        )
        return RelationFollow(res)

    def unfollow(self) -> RelationFollow:
        """Make a DELETE Request to unfollow a User.

        Parameters
        ------------
        user_id: Union[str, int]
            The user's id that you wish to unfollow.

        This function return a :class:`RelationFollow` object.

        .. versionadded:: 1.1.0
        """
        my_id = self.http_clientaccess_token.partition("-")[0]
        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/following/{self.id}", auth=True)
        return RelationFollow(res)

    def block(self) -> None:
        """Make a POST Request to Block a User.

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to block.

        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request(
            "POST",
            "2",
            f"/users/{my_id}/blocking",
            json={"target_user_id": str(self.id)},
            auth=True,
        )

    def unblock(self) -> None:
        """Make a DELETE Request to unblock a User.

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to unblock.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request("DELETE", "2", f"/users/{my_id}/blocking/{self.id}", auth=True)

    def mute(self) -> None:
        """Make a POST Request to mute a User.

        Parameters
        ------------
        user_id: Union[str, int]
            The user's id that you wish to mute.

        .. versionadded:: 1.2.5
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request(
            "POST",
            "2",
            f"/users/{my_id}/muting",
            json={"target_user_id": str(self.id)},
            auth=True,
        )

    def unmute(self) -> None:
        """Make a DELETE Request to unmute the User.

        Parameters
        ------------
        user_id: Union[str, int]
        The user's id that you wish to unmute.

        .. versionadded:: 1.2.5
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request("DELETE", "2", f"/users/{my_id}/muting/{self.id}", auth=True)

    def typing(self):
        """Indicates that the client is typing in a user Dm."""
        self.http_client.request(
            "POST",
            "1.1",
            "/direct_messages/indicate_typing.json",
            params={"recipient_id": str(self.id)},
            auth=True,
        )

    @property
    def name(self) -> str:
        """:class:`str`: Return the user's name.

        .. versionadded: 1.0.0
        """
        return self._payload.get("name")

    @property
    def username(self) -> str:
        """:class:`str`: Return the user's username, this usually start with '@' follow by their username.

        .. versionadded: 1.0.0
        """
        return "@" + self._payload.get("username")

    @property
    def id(self) -> int:
        """:class:`int`: Return the user's id.

        .. versionadded: 1.0.0
        """
        return int(self._payload.get("id"))

    @property
    def bio(self) -> str:
        """:class:`str`: Return the user's bio.

        .. versionadded: 1.0.0
        """
        return self._payload.get("description")

    @property
    def description(self) -> str:
        """:class:`str`: an alias to User.bio.

        .. versionadded: 1.0.0
        """
        return self._payload.get("description")

    @property
    def profile_link(self) -> str:
        """:class:`str`: Return the user's profile link

        .. versionadded: 1.0.0
        """
        return f"https://twitter.com/{self.username.replace('@', '', 1)}"

    @property
    def link(self) -> str:
        """:class:`str`: Return url where the user put links, return an empty string if there isn't a url

        .. versionadded: 1.0.0
        """
        return self._payload.get("url")

    @property
    def verified(self) -> bool:
        """:class:`bool`: Return True if the user is verified account, else False.

        .. versionadded: 1.0.0
        """
        return self._payload.get("verified")

    @property
    def protected(self) -> bool:
        """:class:`bool`: Return True if the user is protected, else False.

        .. versionadded: 1.0.0
        """
        return self._payload.get("protected")

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Return the user profile image.

        .. versionadded: 1.0.0
        """
        return self._payload.get("profile_image_url")

    @property
    def location(self) -> Optional[str]:
        """:class:`str`: Return the user's location

        .. versionadded: 1.0.0
        """
        return self._payload.get("location")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Return datetime.datetime object with the user's account date.

        .. versionadded: 1.0.0
        """
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def pinned_tweet(self) -> Optional[object]:
        """Optional[:class:`object`]: Returns the user's pinned tweet.

        .. versionadded: 1.1.3
        """
        id = self._payload.get("pinned_tweet_id")
        return None if not id else self.http_client.fetch_tweet(int(id), http_client=self.http_client)

    @property
    def followers(self) -> Union[List[User], List]:
        """List[:class:`User`]: Returns a list of users who are followers of the specified user ID. Maximum users is 100 users.

        .. versionadded: 1.1.0
        """
        return self._payload.get("followers")

    @property
    def following(self) -> Union[List[User], List]:
        """List[:class:`User`]`: Returns a list of users that's followed by the specified user ID. Maximum users is 100 users.

        .. versionadded: 1.1.0
        """
        return self._payload.get("following")

    @property
    def follower_count(self) -> int:
        """:class:`int`: Return total of followers that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.follower_count

    @property
    def following_count(self) -> int:
        """:class:`int`: Return total of following that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.following_count

    @property
    def tweet_count(self) -> int:
        """:class:`int`: Return total of tweet that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.tweet_count

    @property
    def listed_count(self) -> int:
        """:class:`int`: Return total of listed that a user has.

        .. versionadded: 1.1.0
        """
        return self._metrics.listed_count
