from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, NoReturn, Optional, List, Union

from .attachments import CTA, QuickReply, File, CustomProfile
from .metrics import UserPublicMetrics
from .relations import RelationFollow
from .utils import time_parse_todt
from .expansions import (
    USER_FIELD,
    TWEET_EXPANSION,
    MEDIA_FIELD,
    PLACE_FIELD,
    POLL_FIELD,
    TWEET_FIELD,
)

if TYPE_CHECKING:
    from .http import HTTPClient
    from .message import DirectMessage


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

    def __init__(self, data: Dict[str, Any], http_client: Optional[HTTPClient] = None) -> None:
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = self.original_payload.get("data") or self.original_payload
        self.http_client = http_client
        self._metrics = UserPublicMetrics(self._payload) or self.original_payload

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return "User(name={0.name} username={0.username} id={0.id})".format(self)

    def __eq__(self, other: User) -> Union[bool, NoReturn]:
        if not isinstance(other, User):
            raise ValueError("== operation cannot be done with one of the element not a valid User object")
        return self.id == other.id

    def __ne__(self, other: User) -> Union[bool, NoReturn]:
        if not isinstance(other, User):
            raise ValueError("!= operation cannot be done with one of the element not a valid User object")
        return self.id != other.id

    def send(
        self,
        text: str,
        *,
        file: Optional[File] = None,
        custom_profile: Optional[CustomProfile] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> DirectMessage:
        """Send a message to the user.

        Parameters
        ------------
        text: :class:`str`
            The text that will be send to that user.
        file: Optional[:class:`File`]
            Represent a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
        custom_profile: Optional[:class:`custom_profile`]
            The custom profile attachment.
        quick_reply: Optional[:class:`QuickReply`]
            The QuickReply attachment that will be send to a user.
        cta: Optional[:class:`CTA`]
            cta or call-to-actions is use to make an action whenever a user 'call' something, a quick example is buttons.

        Returns
        ---------
        :class:`DirectMessage`
            This method return a :class:`DirectMessage` object.


        .. versionadded:: 1.1.0
        """
        return self.http_client.send_message(
            self.id,
            text,
            file=file,
            custom_profile=custom_profile,
            quick_reply=quick_reply,
            cta=cta,
        )

    def follow(self) -> RelationFollow:
        """Make a Request to follow a User.

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
            The user's id that you wish to follow.

        Returns
        ---------
        :class:`RelationFollow`
            This method return a :class:`RelationFollow` object.


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
        user_id: Union[:class:`str`, :class:`int`]
            The user's id that you wish to unfollow.

        Returns
        ---------
        :class:`RelationFollow`
            This method return a :class:`RelationFollow` object.


        .. versionadded:: 1.1.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/following/{self.id}", auth=True)
        return RelationFollow(res)

    def block(self) -> None:
        """Make a POST Request to Block a User.

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
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

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
            The user's id that you wish to unblock.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request("DELETE", "2", f"/users/{my_id}/blocking/{self.id}", auth=True)

    def mute(self) -> None:
        """Make a POST Request to mute a User.

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
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
        user_id: Union[:class:`str`, :class:`int`]
            The user's id that you wish to unmute.


        .. versionadded:: 1.2.5
        """
        my_id = self.http_client.access_token.partition("-")[0]
        self.http_client.request("DELETE", "2", f"/users/{my_id}/muting/{self.id}", auth=True)

    def trigger_typing(self):
        """Indicates that the client is typing in a user Dm.

        .. versionadded:: 1.3.5
        """
        self.http_client.request(
            "POST",
            "1.1",
            "/direct_messages/indicate_typing.json",
            params={"recipient_id": str(self.id)},
            auth=True,
        )

    def report(self, block: bool = True):
        """Report the user as a spam account to twitter.

        Parameters
        -----------
        block:
            Indicates that the client perform a block action to the user if set to True. Default to True.


        .. versionadded:: 1.3.5
        """
        self.http_client.request(
            "POST",
            "1.1",
            "/users/report_spam.json",
            params={"user_id": str(self.id), "perform_block": block},
        )

    def fetch_followers(self) -> Optional[List[User]]:
        """Fetch the user's followers.

        .. note::
            This method will only returns 100 users unless you have an academic research access. Then it can returns more then 100 users.


        .. versionadded:: 1.3.5
        """
        followers = self.http_client.request(
            "GET",
            "2",
            f"/users/{self.id}/followers",
            params={"user.fields": USER_FIELD},
        )
        return [User(data, http_client=self.http_client) for data in followers["data"]]

    def fetch_following(self) -> Optional[List[User]]:
        """Fetch the user's following.

        .. note::
            This method will only returns 100 users unless you have an academic research access. Then it can returns more then 100 users.


        .. versionadded:: 1.3.5
        """
        following = self.http_client.request(
            "GET",
            "2",
            f"/users/{self.id}/following",
            params={"user.fields": USER_FIELD},
        )

        try:
            return [User(data, http_client=self.http_client) for data in following["data"]]
        except TypeError:
            return following

    def fetch_pinned_tweet(self) -> Optional[Any]:
        """Returns the user's pinned tweet.

        Returns
        ---------
        Optional[:class:`int`]
            This method returns a :class:`Tweet` object.


        .. versionadded: 1.1.3
        """
        id = self._payload.get("pinned_tweet_id")
        return self.http_client.fetch_tweet(int(id)) if id else None

    def fetch_timelines(
        self,
        max_results: int = 10,
        *,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        since_id: Optional[Union[str, int]] = None,
        until_id: Optional[Union[str, int]] = None,
        mentioned: bool = False,
        exclude: Optional[str] = None,
    ) -> Union[List[object], List]:
        """Fetch the user timelines, this can be timelines where the user got mention or a normal tweet timelines.

        Parameters
        ------------
        max_results: :class:`int`
            Specified how many tweets should be return.
        start_time: Optional[:class:`datetime.datetime`]:
            This will make sure the tweets created datetime is after that specific time.
        end_time: Optional[:class:`datetime.datetime`]:
            This will make sure the tweets created datetime is before that specific time.
        since_id: Optional[Union[:class:`str`, :class:`int`]]
            Returns results with a Tweet ID greater than (that is, more recent than) the specified 'since' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the since_id. If the limit of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.
        until_id: Optional[Union[:class:`str`, :class:`int`]]
            Returns results with a Tweet ID less less than (that is, older than) the specified 'until' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the until_id. If the limit of Tweets has occurred since the until_id, the until_id will be forced to the most recent ID available.
        mentioned: :class:`bool`
            Indicates if only mentioned timelines return if set to True, else it will returns a normal tweet timelines. Default to False.
        exclude: :class:`str`
            Specified which tweet type should not be returns, you can set it to:'retweets,replies' or 'retweets' or 'replies'.

        Returns
        ---------
        Union[List[:class:`Tweet`], List]
            This method returns a list of :class:`Tweet` objects or an empty list if none founded.


        .. versionadded:: 1.3.5
        """
        if (
            not isinstance(start_time, datetime.datetime)
            and start_time
            or not isinstance(end_time, datetime.datetime)
            and end_time
        ):
            raise ValueError("start_time or end_time must be a datetime object!")

        params = {
            "expansions": TWEET_EXPANSION,
            "user.fields": USER_FIELD,
            "media.fields": MEDIA_FIELD,
            "place.fields": PLACE_FIELD,
            "poll.fields": POLL_FIELD,
            "tweet.fields": TWEET_FIELD,
        }

        params["max_results"] = max_results
        if start_time:
            params["start_time"] = start_time.isoformat()
        if end_time:
            params["end_time"] = end_time.isoformat()
        if since_id:
            params["since_id"] = str(since_id)
        if until_id:
            params["until_id"] = str(until_id)
        if exclude:
            params["exclude"] = exclude

        res = self.http_client.request(
            "GET",
            "2",
            f"/users/{self.id}/tweets" if not mentioned else f"/users/{self.id}/mentions",
            params=params,
        )

        Tweet = self.http_client.build_object("Tweet")
        try:
            return [Tweet(data, http_client=self.http_client) for data in res["data"]]
        except (TypeError, KeyError):
            return []

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
        return self._payload.get("description", "")

    @property
    def description(self) -> str:
        """:class:`str`: an alias to User.bio

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
        return self._payload.get("url", "")

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
    def private(self) -> bool:
        """:class:`bool`: An alias to :class:`User.protected`.

        .. versionadded: 1.3.5
        """
        return self.protected

    @property
    def profile_url(self) -> Optional[str]:
        """Optional[:class:`str`]: Return the user profile image.

        .. versionadded: 1.0.0
        """
        return self._payload.get("profile_image_url", "")

    @property
    def location(self) -> Optional[str]:
        """:class:`str`: Return the user's location

        .. versionadded: 1.0.0
        """
        return self._payload.get("location", "")

    @property
    def created_at(self) -> datetime.datetime:
        """Optional[:class:`datetime.datetime`]: Return datetime.datetime object with the user's account date.

        .. versionadded: 1.0.0
        """
        return time_parse_todt(self._payload.get("created_at"))

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
