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
    follower_count: Union[int, str]
    following_count: Union[int, str]
    tweet_count: Union[int, str]
    listed_count: Union[int, str]


@dataclass
class PublicTweetMetrics:
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    quote_count: Union[int, str]
    reply_count: Union[int, str]


@dataclass
class NonPublicTweetMetrics:
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class OrganicTweetMetrics:
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    reply_count: Union[int, str]
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class PromotedTweetMetrics:
    like_count: Union[int, str]
    retweet_count: Union[int, str]
    reply_count: Union[int, str]
    impression_count: Union[int, str]
    user_profile_clicks: Union[int, str]
    url_link_clicks: Optional[Union[int, str]] = None


@dataclass
class NonPublicMediaMetrics:
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]


@dataclass
class OrganicMediaMetrics:
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]
    view_count: Optional[Union[int, str]] = None


@dataclass
class PromotedMediaMetrics:
    playback_0_count: Union[str, int]
    playback_100_count: Union[str, int]
    playback_25_count: Union[str, int]
    playback_50_count: Union[str, int]
    playback_75_count: Union[str, int]
    view_count: Optional[Union[int, str]] = None
