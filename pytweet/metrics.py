from typing import Any, Dict

__all__ = (
    "UserPublicMetrics",
    "TweetPublicMetrics",
)


class UserPublicMetrics:
    __slots__ = ("__original_payload", "_public")

    def __init__(self, data: Dict[str, Any] = {}):
        self.__original_payload = data
        self._public = self.__original_payload.get("public_metrics")

    def __repr__(self) -> str:
        return f"UserPublicMetrics(user={self.__original_payload.get('username')} follower_count={self.follower_count} following_count={self.following_count} tweet_count={self.tweet_count})"

    @property
    def follower_count(self) -> int:
        return int(self._public.get("followers_count"))

    @property
    def following_count(self) -> int:
        return int(self._public.get("following_count"))

    @property
    def tweet_count(self) -> int:
        return int(self._public.get("tweet_count"))

    @property
    def listed_count(self) -> int:
        return int(self._public.get("listed_count"))


class TweetPublicMetrics:
    __slots__ = ("__original_payload", "_public")

    def __init__(self, data: Dict[str, Any] = {}) -> None:
        self.__original_payload = data
        self._public = self.__original_payload.get("public_metrics")

    def __repr__(self) -> str:
        return f"TweetPublicMetrics(like_count={self.like_count} retweet_count={self.retweet_count} reply_count={self.reply_count}> quote_count={self.quote_count})"

    @property
    def like_count(self) -> int:
        return int(self._public.get("like_count"))

    @property
    def retweet_count(self) -> int:
        return int(self._public.get("retweet_count"))

    @property
    def reply_count(self) -> int:
        return int(self._public.get("reply_count"))

    @property
    def quote_count(self) -> int:
        return int(self._public.get("quote_count"))