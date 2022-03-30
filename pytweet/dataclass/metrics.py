from dataclasses import dataclass
from typing import Union, Optional

# TODO: Finish adding metrics and stuff

__all__ = (
    "PublicUserMetrics",
    "PublicTweetMetrics",
    "NonPublicTweetMetrics",
    "OrganicTweetMetrics",
    "PromotedTweetMetrics",
    "NonPublicMediaMetrics",
    "OrganicMediaMetrics",
    "PromotedMediaMetrics",
)


@dataclass
class PublicUserMetrics:
    """A public metrics for :class:`User`

    The following properties return an object from the metrics.
    
    * :meth:`User.follower_count` 
    * :meth:`User.following_count`
    * :meth:`User.tweet_count`
    * :meth:`User.listed_count`


    .. versionadded:: 1.5.0
    """
    follower_count: Union[int, str]
    following_count: Union[int, str]
    tweet_count: Union[int, str]
    listed_count: Union[int, str]


@dataclass
class PublicTweetMetrics:
    """A public metrics for :class:`Tweet`

    The following properties return an object from the metrics.
    
    * :meth:`Tweet.like_count` 
    * :meth:`Tweet.retweet_count`
    * :meth:`Tweet.quote_count`
    * :meth:`Tweet.reply_count`


    .. versionadded:: 1.5.0
    """
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    quote_count: Union[int, str]
    reply_count: Union[int, str]


@dataclass
class NonPublicTweetMetrics:
    """A non public metrics for :class:`Tweet`

    To get the metrics you can use `Tweet.non_public_metrics`.


    .. versionadded:: 1.5.0
    """
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class OrganicTweetMetrics:
    """An organic metrics for :class:`Tweet`

    To get the metrics you can use `Tweet.organic_metrics`.


    .. versionadded:: 1.5.0
    """
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    reply_count: Union[int, str]
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class PromotedTweetMetrics:
    """A promoted metrics for :class:`Tweet`

    To get the metrics you can use `Tweet.promoted_metrics`.


    .. versionadded:: 1.5.0
    """
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    reply_count: Union[int, str]
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class NonPublicMediaMetrics:
    """A non public metrics for :class:`Media`

    To get the metrics you can use `Media.non_public_metrics`.


    .. versionadded:: 1.5.0
    """
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]


@dataclass
class OrganicMediaMetrics:
    """An organic metrics for :class:`Media`

    To get the metrics you can use `Media.organic_metrics`.


    .. versionadded:: 1.5.0
    """
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]
    view_count: Optional[Union[int, str]] = None


@dataclass
class PromotedMediaMetrics:
    """A promoted metrics for :class:`Media`

    To get the metrics you can use `Media.promoted_metrics`.


    .. versionadded:: 1.5.0
    """
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]
    view_count: Optional[Union[int, str]] = None
