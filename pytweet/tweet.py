from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from .attachments import Poll, Geo, File, Media
from .enums import ReplySetting
from .constants import (
    TWEET_EXPANSION,
    TWEET_FIELD,
    USER_FIELD,
    PINNED_TWEET_EXPANSION,
    MEDIA_FIELD,
    PLACE_FIELD,
    POLL_FIELD,
)
from .relations import RelationHide, RelationLike, RelationRetweet, RelationDelete
from .user import User
from .utils import time_parse_todt, convert
from .message import Message
from .paginations import UserPagination, TweetPagination
from .dataclass import (
    Embed,
    EmbedImage,
    PublicTweetMetrics,
    NonPublicTweetMetrics,
    OrganicTweetMetrics,
    PromotedTweetMetrics,
)

if TYPE_CHECKING:
    from .http import HTTPClient
    from .type import ID

__all__ = ("Tweet",)


class Tweet(Message):
    """Represents a tweet message from Twitter.
    A Tweet is any message posted to Twitter which may contain photos, videos, links, and text. This class inherits :class:`Message`,

    .. describe:: x == y

        Check if one tweet id is equal to another.


    .. describe:: x != y

        Check if one tweet id is not equal to another.


    .. describe:: str(x)

        Get the Tweet's text.


    .. versionadded:: 1.0.0
    """

    __slots__ = (
        "__original_payload",
        "_payload",
        "_includes",
        "tweet_metrics",
        "http_client",
        "deleted_timestamp",
        "_public_metrics",
        "_non_public_metrics",
        "_organic_metrics",
        "_promoted_metrics",
    )

    def __init__(
        self,
        data: Dict[str, Any],
        *,
        deleted_timestamp: Optional[int] = None,
        http_client: Optional[HTTPClient] = None,
    ) -> None:
        self.__original_payload = data
        self._payload = data.get("data") or data
        self._includes = self.__original_payload.get("includes")
        self._referenced_tweets = self._payload.get("referenced_tweets")
        self._entities = self._payload.get("entities")
        self.http_client = http_client
        self.deleted_timestamp = deleted_timestamp
        self._public_metrics = PublicTweetMetrics(
            **self._payload.get("public_metrics", None) or self.__original_payload.get("public_metrics")
        )
        self._non_public_metrics = self._payload.get("non_public_metrics", None) or self.__original_payload.get(
            "non_public_metrics"
        )
        self._organic_metrics = self._payload.get("organic_metrics", None) or self.__original_payload.get(
            "organic_metrics"
        )
        self._promoted_metrics = self._payload.get("promoted_metrics", None) or self.__original_payload.get(
            "promoted_metrics"
        )
        if self._non_public_metrics:
            non_public_metrics = self.http_client.payload_parser.parse_metric_data(self._non_public_metrics)
            self._non_public_metrics = NonPublicTweetMetrics(**non_public_metrics)

        if self._organic_metrics:
            organic_metrics = self.http_client.payload_parser.parse_metric_data(self._organic_metrics)
            self._organic_metrics = OrganicTweetMetrics(**organic_metrics)

        if self._promoted_metrics:
            promoted_metrics = self.http_client.payload_parser.parse_metric_data(self._promoted_metrics)
            self._promoted_metrics = PromotedTweetMetrics(**promoted_metrics)

        if self._entities and self._entities.get("urls"):
            data = []
            for url in self._entities["urls"]:
                url = self.http_client.payload_parser.parse_embed_data(url)
                data.append(url)
            self._embeds = data
        else:
            self._embeds = None

        super().__init__(self._payload.get("text"), self._payload.get("id"), 1)

    def __repr__(self) -> str:
        return "Tweet(text={0.text} id={0.id} author={0.author!r})".format(self)

    @property
    def author(self) -> Optional[User]:
        """Optional[:class:`User`]: Returns a user (object) who posted the tweet.

        .. versionadded: 1.0.0
        """
        if self._includes and self._includes.get("users"):
            return User(self._includes.get("users")[0], http_client=self.http_client)
        return None

    @property
    def possibly_sensitive(self) -> bool:
        """:class:`bool`: Returns True if the tweet is possible sensitive to some users, else False.

        .. versionadded: 1.0.0
        """
        return self._payload.get("possibly_sensitive")

    @property
    def sensitive(self) -> bool:
        """:class:`bool`: An alias to :meth:`Tweet.possibly_sensitive`.

        .. versionadded: 1.5.0
        """
        return self.possibly_sensitive

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a :class:`datetime.datetime` object when the tweet was created.

        .. versionadded: 1.0.0
        """
        if self._payload.get("timestamp", None):
            return datetime.datetime.fromtimestamp(int(self._payload.get("timestamp", None)) / 1000)
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def deleted_at(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: Returns a :class:`datetime.datetime` object when the tweet was deleted. Returns None when the tweet is not deleted.

        .. note::
            This property can only returns :class:`datetime.datetime` object through a tweet object from `on_tweet_delete` event.

        .. versionadded: 1.5.0
        """
        if not self.deleted_timestamp:
            return None
        return datetime.datetime.fromtimestamp(self.deleted_timestamp / 1000)

    @property
    def source(self) -> str:
        """:class:`str`: Returns the source of the tweet. e.g if you post a tweet from a website, the source is gonna be 'Twitter Web App'

        .. versionadded: 1.0.0
        """
        return self._payload.get("source")

    @property
    def reply_setting(self) -> ReplySetting:
        """:class:`ReplySetting`: Returns a :class:`ReplySetting` object with the tweet's reply setting. If everyone can reply, this method return :class:`ReplySetting.everyone`.

        .. versionadded: 1.3.5
        """
        return ReplySetting(self._payload.get("reply_settings"))

    @property
    def raw_reply_setting(self) -> str:
        """:class:`str`: Returns the raw reply setting value. If everyone can replied, this method return 'Everyone'.

        .. versionadded: 1.0.0
        """
        return self._payload.get("reply_settings")

    @property
    def lang(self) -> str:
        """:class:`str`: Returns the tweet's lang, if its english it return en.

        .. versionadded: 1.0.0
        """
        return self._payload.get("lang")

    @property
    def conversation_id(self) -> Optional[int]:
        """Optional[:class:`int`]: All replies are bind to the original tweet, this property returns the tweet's id if the tweet is a reply tweet else it returns None.

        .. versionadded: 1.0.0
        """
        try:
            return int(self._payload.get("conversation_id"))
        except ValueError:
            return None

    @property
    def url(self) -> Optional[str]:
        """Optional[:class:`str`]: Get the tweet's url.

        .. versionadded:: 1.1.0

        .. versionchanged:: 1.5.0

            Returns None if the author is invalid or the tweet doesn't have id.
        """
        try:
            return f"https://twitter.com/{self.author.username}/status/{self.id}"
        except TypeError:
            return None

    @property
    def mentions(self) -> Optional[List[User]]:
        """Optional[List[:class:`User`]]: Returns a list of :class:`User` objects that were mentioned in the tweet or an empty list / `[]` if no users were mentioned.

        .. versionadded:: 1.1.3

        .. versionchanged:: 1.5.0

            Now returns a list of :class:`User` objects rather then a list of :class:`str` objects.
        """
        users = []
        for user in self._includes.get("users", {}):
            for mention in self._entities.get("mentions", {}):
                if user["id"] == mention["id"]:
                    users.append(User(user, http_client=self.http_client))
        return users

    @property
    def poll(self) -> Optional[Poll]:
        """:class:`Poll`: Returns a Poll object with the tweet's poll.

        .. versionadded:: 1.1.0
        """
        if self._includes:
            if self._includes.get("polls"):
                data = self._includes.get("polls")[0]
                poll = Poll(
                    duration=data.get("duration_minutes"),
                    id=data.get("id"),
                    voting_status=data.get("voting_status"),
                    end_date=data.get("end_datetime"),
                )
                for option in data.get("options"):
                    poll.add_option(**option)
                return poll
        return None

    @property
    def medias(self) -> Optional[List[Media]]:
        """Optional[List[:class:`Media`]]: Returns a list of media(s) in a tweet.

        .. versionadded:: 1.1.0
        """
        if self._includes and self._includes.get("media"):
            return [Media(img, http_client=self.http_client) for img in self._includes.get("media")]
        return None

    @property
    def reference_user(self) -> Optional[User]:
        """Optional[:class:`User`]: Returns the referenced user. This can means:

        The tweet is a retweet, which means the method returns the retweeted tweet's author.
        The tweet is a quote tweet(retweet with comments), which means the method returns the quoted tweet's author.
        The tweet is a reply tweet, which means the method returns the replied tweet's author.

        .. versionadded:: 1.5.0
        """
        if not self._includes or not self._includes.get("users") or not self._referenced_tweets:
            return None

        type = self._referenced_tweets[0].get("type", " ")
        for user in self._includes["users"]:
            if type == "replied_to" and user["id"] == self._payload.get("in_reply_to_user_id", 0):
                # If the tweet count as a reply tweet,
                # it would returns a user data that match the user's id with 'in_reply_to_user_id' data.
                return User(user, http_client=self.http_client)

            elif type == "quoted":
                # If the tweet count as a quote tweet,
                # it would returns a user data if the url contains the user's id. Every quote tweets have at least 1 url, the quoted tweet's url that contain the quoted tweet's author's id and the tweet id itself.
                for embed in self.embeds:
                    if (
                        embed.expanded_url.startswith("https://twitter.com/")
                        and embed.expanded_url.split("/")[3] == user["id"]
                    ):
                        return User(user, http_client=self.http_client)

            elif type == "retweeted":
                # If the tweet count as a retweet,
                # it would returns a user data if the user are mention with a specific format, that is: 'RT @Mention: {The retweeted tweet's content}'
                # The code only checks characters before the colon with the colon includes (i.e 'RT @Mention:').
                for mentioned_user in self.mentions:
                    if self.text.startswith(f"RT {mentioned_user.mention}:"):
                        return mentioned_user
        return None

    @property
    def reference_tweet(self) -> Optional[Tweet]:
        """Optional[:class:`Tweet`]: Returns the tweet's parent tweet or the  referenced tweet. This can mean the parent tweet of the requested tweet is:

        A retweeted tweet (The child Tweet is a Retweet),
        A quoted tweet (The child Tweet is a Retweet with comment, also known as Quoted Tweet),
        A replied tweet (The child Tweet is a reply tweet).

        .. versionadded:: 1.5.0
        """
        tweets = self._includes.get("tweets")
        if not self._includes or not tweets or not self._referenced_tweets:
            return None

        for tweet in tweets:
            if tweet["id"] == self._referenced_tweets[0]["id"]:
                self.http_client.payload_parser.insert_object_author(tweet, self.reference_user)
                return Tweet(tweet, http_client=self.http_client)
        return None

    @property
    def embeds(self) -> Optional[List[Embed]]:
        """List[:class:`Embed`]: Returns a list of Embedded urls from the tweet

        .. versionadded:: 1.1.3
        """
        for embed in self._embeds:
            if embed.get("images"):
                for index, image in enumerate(embed["images"]):
                    if isinstance(image, EmbedImage):
                        break
                    embed["images"][index] = EmbedImage(**image)
        return [Embed(**data) for data in self._embeds]

    @property
    def like_count(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the total of likes in the tweet.

        .. versionadded: 1.1.0
        """
        return convert(self._metrics.like_count, int)

    @property
    def retweet_count(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the total of retweetes in the tweet.

        .. versionadded: 1.1.0
        """
        return convert(self._metrics.retweet_count, int)

    @property
    def reply_count(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the total of replies in the tweet.

        .. versionadded: 1.1.0
        """
        return convert(self._metrics.reply_count, int)

    @property
    def quote_count(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the total of quotes in the tweet.

        .. versionadded: 1.1.0
        """
        return convert(self._metrics.quote_count, int)

    @property
    def non_public_metrics(self) -> Optional[OrganicTweetMetrics]:
        """Optional[:class:`OrganicTweetMetrics`]: The tweet's metrics that are not available for anyone to view on Twitter, such as `impressions_count` and `video view quartiles`.

        .. versionadded:: 1.5.0
        """
        return self._non_public_metrics

    @property
    def organic_metrics(self) -> Optional[OrganicTweetMetrics]:
        """Optional[:class:`OrganicTweetMetrics`]: The tweet's metrics in organic context (posted and viewed in a regular manner), such as `impression_count`, `user_profile_clicks` and `url_link_clicks`.

        .. versionadded:: 1.5.0
        """
        return self._organic_metrics

    @property
    def promoted_metrics(self) -> Optional[PromotedTweetMetrics]:
        """Optional[:class:`PromotedTweetMetrics`]: The tweet's metrics in promoted context (posted or viewed as part of an Ads campaign), such as `impression_count`, `user_profile_clicks` and `url_link_clicks`.

        .. versionadded:: 1.5.0
        """
        return self._promoted_metrics

    def like(self) -> Optional[RelationLike]:
        """Like the tweet.

        Returns
        ---------
        Optional[:class:`RelationLike`]
            This method returns a :class:`RelationLike` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        res = self.http_client.request("POST", "2", f"/users/{my_id}/likes", json={"tweet_id": str(self.id)}, auth=True)
        return RelationLike(res)

    def unlike(self) -> Optional[RelationLike]:
        """Unlike the tweet.

        Returns
        ---------
        :class:`RelationLike`
            This method returns a :class:`RelationLike` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/likes/{self.id}", auth=True)

        return RelationLike(res)

    def retweet(self) -> RelationRetweet:
        """Retweet the tweet.

        Returns
        ---------
        :class:`RelationRetweet`
            This method returns a :class:`RelationRetweet` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]
        res = self.http_client.request(
            "POST",
            "2",
            f"/users/{my_id}/retweets",
            json={"tweet_id": str(self.id)},
            auth=True,
        )

        return RelationRetweet(res)

    def unretweet(self) -> RelationRetweet:
        """Unretweet the tweet.

        Returns
        ---------
        :class:`RelationRetweet`
            This method returns a :class:`RelationRetweet` object.


        .. versionadded:: 1.2.0
        """
        my_id = self.http_client.access_token.partition("-")[0]

        res = self.http_client.request("DELETE", "2", f"/users/{my_id}/retweets/{self.id}", auth=True)

        return RelationRetweet(res)

    def delete(self) -> RelationDelete:
        """Delete the client's tweet.

        .. note::
            You can only delete the client's tweet.

        .. versionadded:: 1.2.0
        """
        res = self.http_client.request("DELETE", "2", f"/tweets/{self.id}", auth=True)

        try:
            self.http_client.tweet_cache.pop(self.id)
        except KeyError:
            pass

        return RelationDelete(res)

    def reply(
        self,
        text: str = None,
        *,
        file: Optional[File] = None,
        files: Optional[List[File]] = None,
        geo: Optional[Union[Geo, str]] = None,
        direct_message_deep_link: Optional[str] = None,
        reply_setting: Optional[Union[ReplySetting, str]] = None,
        exclude_reply_users: Optional[List[User, ID]] = None,
        media_tagged_users: Optional[List[User, ID]] = None,
    ) -> Optional[Tweet]:
        """Post a tweet to reply to the tweet present by the tweet's id. Returns a :class:`Tweet` object or :class:`Message` if the tweet is not found in the cache.

        .. note::
            Note that if the tweet is a retweet you cannot reply to that tweet, it might not raise an error but it will post the tweet has a normal tweet rather then a reply tweet and it ping the :class:`Tweet.author`.

        Parameters
        ------------
        text: :class:`str`
            The tweet's text, it will show up as the main text in a tweet.
        file: Optional[:class:`File`]
            Represents a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
        files: Optional[List[:class:`File`]]
            Represents multiple file attachments in a list. It could be an image, gif, or video. the item in the list must also be an instance of pytweet.File
        geo: Optional[Union[:class:`Geo`, :class:`str`]]
            The geo attachment, you can put an object that is an instance of :class:`Geo` or the place ID in a string.
        direct_message_deep_link: Optional[:class:`str`]
            The direct message deep link, It will showup as a CTA(call-to-action) with button attachment. Example of direct message deep link:
        reply_setting: Optional[Union[:class:`ReplySetting`, :class:`str`]]
            The reply setting that you can set to minimize users that can reply. If None is specified, the default is set to 'everyone' can reply.
        exclude_reply_users: Optional[List[:class:`User`]]
            A list of users or user ids to be excluded from the reply :class:`Tweet` thus removing a user from a thread, if you dont want to mention a reply with 3 mentions, You can use this argument and provide the user id you don't want to mention.
        media_tagged_users: Optional[List[:class:`User`]]
            A list of users or user ids being tagged in the Tweet with Media. If the user you're tagging doesn't have photo-tagging enabled, their names won't show up in the list of tagged users even though the Tweet is successfully created.

        Returns
        ---------
        Union[:class:`Tweet`, :class:`Message`]
            Returns a :class:`Tweet` object or :class:`Message` object if the tweet is not found in the cache.


        .. versionadded:: 1.2.5
        """
        return self.http_client.post_tweet(
            text,
            file=file,
            files=files,
            geo=geo,
            direct_message_deep_link=direct_message_deep_link,
            reply_setting=reply_setting,
            reply_tweet=self.id,
            exclude_reply_users=exclude_reply_users,
            media_tagged_users=media_tagged_users,
        )

    def hide(self) -> RelationHide:
        """Hide a reply tweet.

        Returns
        ---------
        :class:`RelationHide`
            This method returns a :class:`RelationHide` object.


        .. versionadded:: 1.2.5
        """
        res = self.http_client.request("PUT", "2", f"/tweets/{self.id}/hidden", json={"hidden": False}, auth=True)
        return RelationHide(res)

    def unhide(self) -> RelationHide:
        """Unhide a hide reply.

        Returns
        ---------
        :class:`RelationHide`
            This method returns a :class:`RelationHide` object.


        .. versionadded:: 1.2.5
        """
        res = self.http_client.request("PUT", "2", f"/tweets/{self.id}/hidden", json={"hidden": False}, auth=True)
        return RelationHide(res)

    def fetch_retweeters(self) -> Optional[UserPagination]:
        """Returns a pagination object with the users that retweeted the tweet.

        Returns
        ---------
        Optional[:class:`UserPagination`]
            This method returns a :class:`UserPagination` object.


        .. versionadded:: 1.1.3
        """
        res = self.http_client.request(
            "GET",
            "2",
            f"/tweets/{self.id}/retweeted_by",
            params={
                "expansions": PINNED_TWEET_EXPANSION,
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
            },
        )
        if not res:
            return []

        return UserPagination(
            res,
            endpoint_request=f"/tweets/{self.id}/retweeted_by",
            http_client=self.http_client,
            params={
                "expansions": PINNED_TWEET_EXPANSION,
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
            },
        )

    def fetch_likers(self) -> Optional[UserPagination]:
        """Returns a pagination object with the users that liked the tweet.

        Returns
        ---------
        Optional[:class:`UserPagination`]
            This method returns a :class:`UserPagination` object.


        .. versionadded:: 1.1.3
        """
        res = self.http_client.request(
            "GET",
            "2",
            f"/tweets/{self.id}/liking_users",
            params={
                "expansions": PINNED_TWEET_EXPANSION,
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
            },
        )

        if not res:
            return []

        return UserPagination(
            res,
            endpoint_request=f"/tweets/{self.id}/liking_users",
            http_client=self.http_client,
            params={
                "expansions": PINNED_TWEET_EXPANSION,
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
            },
        )

    def fetch_quoted_tweets(self) -> Optional[TweetPagination]:
        """Returns a pagination object for tweets that quoted the tweet

        Returns
        ---------
        Optional[:class:`TweetPagination`]
            This method returns :class:`TweetPagination` or an empty list if the tweet does not contain any quoted tweets.


        .. versionadded:: 1.5.0
        """
        params = {
            "expansions": TWEET_EXPANSION,
            "user.fields": USER_FIELD,
            "tweet.fields": TWEET_FIELD,
            "media.fields": MEDIA_FIELD,
            "place.fields": PLACE_FIELD,
            "poll.fields": POLL_FIELD,
            "max_results": 100,
        }

        res = self.http_client.request("GET", "2", f"/tweets/{self.id}/quote_tweets", params=params)

        if not res:
            return []

        return TweetPagination(
            res,
            endpoint_request=f"/tweets/{self.id}/quote_tweets",
            http_client=self.http_client,
            params=params,
        )
