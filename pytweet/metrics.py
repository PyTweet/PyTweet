from typing import Any, Dict

__all__ = (
    "UserPublicMetrics",
    "TweetPublicMetrics",
)


class UserPublicMetrics:
    """Represent a PublicMetrics for a User.
    This PublicMetrics contain public info about the user.

    .. versionadded:: 1.1.0
    """

    def __init__(self, data: Dict[str, Any] = {}, **kwargs: Any):
        self.original_payload: Dict[str, Any] = data
        self._public: Dict[Any, Any] = self.original_payload.get("public_metrics")

    def __repr__(self) -> str:
        return f"UserPublicMetrics(user={self.original_payload.get('username')} follower_count={self.follower_count} following_count={self.following_count} tweet_count={self.tweet_count})"

    @property
    def follower_count(self) -> int:
        """:class:`int`: Returns total of followers that a user has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("followers_count"))

    @property
    def following_count(self) -> int:
        """:class:`int`: Returns total of following that a user has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("following_count"))

    @property
    def tweet_count(self) -> int:
        """:class:`int`: Returns total of tweet that a user has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("tweet_count"))

    @property
    def listed_count(self) -> int:
        """:class:`int`: Returns total of listed that a user has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("listed_count"))


class TweetPublicMetrics:
    """Represent a PublicMetrics for a tweet.
    This PublicMetrics contain public info about the tweet.

    .. versionadded:: 1.1.0
    """

    def __init__(self, data: Dict[str, Any] = {}, **kwargs: Any) -> None:
        self.original_payload = data
        self._public = data.get("public_metrics")

    def __repr__(self) -> str:
        return f"TweetPublicMetrics(like_count={self.like_count} retweet_count={self.retweet_count} reply_count={self.reply_count}> quote_count={self.quote_count})"

    @property
    def like_count(self) -> int:
        """:class:`int`: Return total of likes that the tweet has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("like_count"))

    @property
    def retweet_count(self) -> int:
        """:class:`int`: Return total of retweetes that the tweet has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("retweet_count"))

    @property
    def reply_count(self) -> int:
        """:class:`int`: Return total of replies that the tweet has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("reply_count"))

    @property
    def quote_count(self) -> int:
        """:class:`int`: Return total of quotes that the tweet has.

        .. versionadded:: 1.1.0
        """
        return int(self._public.get("quote_count"))
