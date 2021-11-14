from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, NoReturn, Optional, Union

from .attachments import Media, Poll
from .message import Message
from .metrics import TweetPublicMetrics
from .relations import RelationHide, RelationLike, RelationRetweet
from .user import User
from .utils import time_parse_todt
from .enums import ReplySetting

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = (
    "EmbedsImages",
    "Embed",
    "Tweet",
)


class EmbedsImages:
    """Represent the tweets embed images.

    .. versionadded: 1.1.3
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        self._payload = data

    def __repr__(self) -> str:
        return "EmbedsImages(url={0.url} width={0.width} height={0.height})".format(self)

    def __str__(self) -> str:
        return self.url

    @property
    def width(self) -> int:
        """:class:`int`: Return the image's width

        .. versionadded: 1.1.3
        """
        return int(self._payload.get("width"))

    @property
    def height(self) -> int:
        """:class:`int`: Return the image's height

        .. versionadded: 1.1.3
        """
        return int(self._payload.get("height"))

    @property
    def url(self) -> str:
        """:class:`str`: Return the image's url

        .. versionadded: 1.1.3
        """
        return self._payload.get("url")


class Embed:
    """Represent the embedded urls in a tweet.

    .. versionadded: 1.1.3
    """

    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    def __repr__(self) -> str:
        return "Embed(title={0.title} description={0.description} url={0.url})".format(self)

    def __str__(self) -> str:
        return self.url

    @property
    def title(self) -> str:
        """:class:`str`: Return the embed's title

        .. versionadded: 1.1.3
        """
        return self._payload.get("title")

    @property
    def description(self) -> str:
        """:class:`str`: Return the embed's description

        .. versionadded: 1.1.3
        """
        return self._payload.get("description")

    @property
    def start(self) -> int:
        """:class:`int`: Return the embed's url startpoint start

        .. versionadded: 1.1.3
        """
        return int(self._payload.get("start"))

    @property
    def end(self) -> int:
        """:class:`int`: Return the embed's url endpoint.

        .. versionadded: 1.1.3
        """
        return int(self._payload.get("end"))

    @property
    def url(self) -> str:
        """:class:`str`: Return the embed's url

        .. versionadded: 1.1.3
        """
        return self._payload.get("url")

    @property
    def expanded_url(self) -> str:
        """:class:`str`: Return the expanded url

        .. versionadded: 1.1.3
        """
        return self._payload.get("expanded_url")

    @property
    def display_url(self) -> str:
        """:class:`str`: Return the display url

        .. versionadded: 1.1.3
        """
        return self._payload.get("display_url")

    @property
    def unwound_url(self) -> str:
        """:class:`str`: Return the unwound url

        .. versionadded: 1.1.3
        """
        return self._payload.get("unwound_url")

    @property
    def images(self) -> Optional[List[EmbedsImages]]:
        """List[:class:`EmbedsImages`]: Return a list of Embed's Images

        .. versionadded:: 1.1.3
        """
        if self._payload.get("images"):
            return [EmbedsImages(data) for data in self._payload.get("images")]

        return None

    @property
    def status_code(self) -> int:
        """:class:`int`: Return the embed's url HTTP status code

        .. versionadded: 1.1.3
        """
        return int(self._payload.get("status"))


class Tweet(Message):
    """Represent a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text.

    .. describe:: x == y
        Check if one tweet id is equal to another.


    .. describe:: x != y
        Check if one tweet id is not equal to another.


    .. describe:: str(x)
        Get the Tweet's text.


    .. versionadded:: 1.0.0
    """

    def __init__(self, data: Dict[str, Any], **kwargs: Any) -> None:
        self.original_payload = data
        self._payload = data.get("data") or None
        self._includes = self.original_payload.get("includes")
        self.tweet_metrics: TweetPublicMetrics = TweetPublicMetrics(self._payload)

        super().__init__(self._payload.get("text"), self._payload.get("id"), 1)
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None

    def __repr__(self) -> str:
        return "Tweet(text={0.text} id={0.id} author={0.author})".format(self)

    def __str__(self) -> str:
        return self.text

    def __eq__(self, other: Tweet) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Tweet object")
        return self.id == other.id

    def __ne__(self, other: Tweet) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid User object")
        return self.id != other.id

    def like(self) -> Optional[RelationLike]:
        """A Method for liking a tweet.

        Returns
        ---------
        Returns a :class:`RelationLike` object.

        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        payload = {"tweet_id": str(self.id)}
        res = self.http_client.request("POST", "2", f"/users/{my_id}/likes", json=payload, auth=True)

        return RelationLike(res)

    def unlike(self) -> Optional[RelationLike]:
        """A Method for unliking a tweet.

        Returns
        ---------
        :class:`RelationLike`
            Returns a :class:`RelationLike` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/likes/{self.id}", auth=True)

        return RelationLike(res)

    def retweet(self) -> RelationRetweet:
        """A Method for retweet a tweet.

        Returns
        ---------
        :class:`RelationRetweet`
            Returns a :class:`RelationRetweet` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        payload = {"tweet_id": str(self.id)}
        res = self.http_client.request("POST", "2", f"/users/{my_id}/retweets", json=payload, auth=True)

        return RelationRetweet(res)

    def unretweet(self) -> RelationRetweet:
        """A Method for unretweet a tweet.

        Returns
        ---------
        :class:`RelationRetweet`
            Returns a :class:`RelationRetweet` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/retweets/{self.id}", auth=True)

        return RelationRetweet(res)

    def delete(self) -> None:
        """
        .. note::
            This function is almost complete! though you can still use and open an issue in github if it cause an error.

        Make a DELETE Request to delete a tweet through the tweet_id.

        .. versionadded:: 1.2.0
        """

        self.http_client.request("DELETE", "2", f"/tweets/{self.id}", auth=True)

        try:
            self.http_client.tweet_cache.pop(self.id)
        except KeyError:
            pass

    def reply(self, text: str) -> None:
        """Post a tweet to reply a specific tweet present by the tweet_id parameter.

        Parameters
        ------------
        text: str
            The reply's main text.

        .. versionadded:: 1.2.5
        """
        self.http_client.request(
            "POST",
            "1.1",
            f"/statuses/update.json",
            params={
                "status": self.author.username + " " + text,
                "in_reply_to_status_id": str(self.id),
            },
            auth=True,
        )

    def hide(self):
        """Make a PUT Request to hide a specific reply tweet.

        Parameters
        ------------
        tweet_id: Union[str, int]
            The tweet's id that you wish to hide to.

        .. versionadded:: 1.2.5
        """
        res = self.http_client.request("PUT", "2", f"/tweets/{self.id}/hidden", json={"hidden": False}, auth=True)
        return RelationHide(res)

    def unhide(self):
        """Make a PUT Request to unhide a specific reply tweet.

        Parameters
        ------------
        tweet_id: Union[str, int]
            The tweet's id that you wish to unhide.

        Returns
        ---------
        :class:`RelationHide`
            This method returns a :class:`RelationHide` object.

        .. versionadded:: 1.2.5
        """
        res = self.http_client.request("PUT", "2", f"/tweets/{self.id}/hidden", json={"hidden": False}, auth=True)
        return RelationHide(res)

    @property
    def author(self) -> User:
        """Optional[:class:`User`]: Return a user (object) who posted the tweet.

        .. versionadded: 1.0.0
        """
        if self._includes:
            return User(self._includes.get("users")[0], http_client=self.http_client)
        return None

    @property
    def retweetes(self) -> Union[List[User], list]:
        """Optional[List[:class:`User`, :class:`list`], :class:`int`]: Return a list of users that's retweeted the tweet's id. Maximum users is 100. Return empty list if no one retweeted.

        .. versionadded: 1.0.0
        """
        return self._payload.get("retweetes")

    @property
    def likes(self) -> Union[List[User], list]:
        """Optional[List[:class:`User`], :class:`list`]: Return a list of users that liked the tweet's id. Maximum users is 100. Return empty list if no one liked.

        .. versionadded: 1.0.0
        """
        return self._payload.get("likes")

    @property
    def sensitive(self) -> bool:
        """:class`bool`: Return True if the tweet is possible sensitive to some users, else False

        .. versionadded: 1.0.0
        """
        return self._payload.get("possibly_sensitive")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Return a datetime object with the tweet posted age.

        .. versionadded: 1.0.0
        """
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def source(self) -> str:
        """:class:`str`: Return the source of the tweet. e.g if you post a tweet from a website, the source is gonna be 'Twitter Web App'

        .. versionadded: 1.0.0
        """
        return self._payload.get("source")

    @property
    def raw_reply_setting(self) -> str:
        """:class:`str`: Return the raw reply setting value. If everyone can replied, this method return 'Everyone'.

        .. versionadded: 1.0.0
        """
        return self._payload.get("reply_settings")

    @property
    def reply_setting(self) -> ReplySetting:
        """:class:`ReplySetting`: Return a :class:`ReplySetting` object with the tweet's reply setting. If everyone can reply, this method return ReplySetting.everyone.

        .. versionadded: 1.0.0
        """
        return ReplySetting(self._payload.get("reply_settings"))

    @property
    def lang(self) -> str:
        """:class:`str`: Return the tweet's lang, if its english it return en.

        .. versionadded: 1.0.0
        """
        return self._payload.get("lang")

    @property
    def conversation_id(self) -> int:
        """:class:`int`: Return the tweet's conversation's id.

        .. versionadded: 1.0.0
        """
        return int(self._payload.get("conversation_id"))

    @property
    def link(self) -> str:
        """:class:`str`: Return the tweet's link.

        .. versionadded: 1.1.0
        """
        return f"https://twitter.com/{self.author.username.split('@', 1)[1]}/status/{self.id}"

    @property
    def reply_to(self) -> Optional[User]:
        """Optional[:class:`User`]: Return the user that you reply with the tweet, a tweet count as reply tweet if the tweet startswith @Username or mention a user.

        .. versionadded:: 1.1.3
        """
        return (
            self.http_client.fetch_user(
                int(self._payload.get("in_reply_to_user_id")),
                http_client=self.http_client,
            )
            if self._payload.get("in_reply_to_user_id")
            else None
        )

    @property
    def mentions(self) -> Optional[List[User]]:
        """Optional[List[:class:`User`]]: Return the mentioned users, if there isn't it return None.

        .. versionadded:: 1.1.3
        """
        if self._includes and self._includes.get("mentions"):
            return [
                self.http_client.fetch_user_byusername(user.get("username"), http_client=self.http_client)
                for user in self._includes.get("mentions")
            ]
        return None

    @property
    def poll(self) -> Optional[Poll]:
        """:class:`Poll`: Return a Poll object with the tweet's poll.

        .. versionadded:: 1.1.0
        """
        if self._includes:
            if self._includes.get("polls"):
                data = self._includes.get("polls")[0]
                poll = Poll(
                    data.get("id"),
                    data.get("voting_status"),
                    data.get("duration_minutes"),
                    data.get("end_datetime"),
                )
                for option in data.get("options"):
                    poll.add_option_FromRequest(option.get("position"), option.get("label"), option.get("votes"))
                return poll

        return None

    @property
    def media(self) -> Optional[Media]:
        """List[:class:`Media`]: Return a list of media(s) in a tweet.

        .. versionadded:: 1.1.0
        """
        if self._includes and self._includes.get("media"):
            return [Media(img) for img in self._includes.get("media")]
        return None

    @property
    def embeds(self) -> Optional[List[Embed]]:
        """List[:class:`Embed`]: Return a list of Embedded url from that tweet

        .. versionadded:: 1.1.3
        """
        if self._payload.get("entities") and self._payload.get("entities").get("urls"):
            return [Embed(url) for url in self._payload.get("entities").get("urls")]
        return None

    @property
    def like_count(self) -> int:
        """:class:`int`: Return the total of likes in a tweet.

        .. versionadded: 1.1.0
        """
        return self.tweet_metrics.like_count

    @property
    def retweet_count(self) -> int:
        """:class:`int`: Return the total of retweetes in a tweet.

        .. versionadded: 1.1.0
        """
        return self.tweet_metrics.retweet_count

    @property
    def reply_count(self) -> int:
        """:class:`int`: Return the total of replies in a tweet.

        .. versionadded: 1.1.0
        """
        return self.tweet_metrics.reply_count

    @property
    def quote_count(self) -> int:
        """:class:`int`: Return the total of quotes in a tweet.

        .. versionadded: 1.1.0
        """
        return self.tweet_metrics.quote_count
