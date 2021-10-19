"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Dict, Any

class UserPublicMetrics:
    """
    Represent a PublicMetrics for a User.
    This PublicMetrics contain public info about the user.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of the user's public metrics through a dictionary!

    Attributes:
    ===================
    :property: tweet_count -> Return total tweet that the user tweeted.

    :property: follower_count -> Returns total of followers that a user has.

    :property: following_count -> Returns total of following that a user has.
    """

    def __init__(self, data=Dict[str, Any], **kwargs):
        self.original_payload = data
        self._public = data.get("public_metrics")

    def __str__(self) -> str:
        return f"<UserPublicMetrics: user={self.original_payload.get('username')} followers_count={self._payload.get('followers_count')} following_count={self._payload.get('following_count')} tweet_count={self._payload.get('tweet_count')}>"

    def __repr__(self) -> str:
        return f"<UserPublicMetrics: User={self.original_payload.get('username')}>"

    @property
    def followers_count(self) -> int:
        return self._public.get("followers_count")

    @property
    def following_count(self) -> int:
        return self._public.get("following_count")

    @property
    def tweet_count(self) -> int:
        return self._public.get("tweet_count")

    @property
    def listed_count(self) -> int:
        return self._public.get("listed_count")

class TweetPublicMetrics:
    """
    Represent a PublicMetrics for a tweet.
    This PublicMetrics contain public info about the tweet.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of the tweet's public metrics through a dictionary!

    Attributes:
    ===================
    :property: like_count -> Return total of likes that the tweet has.

    :property: retweeted_count -> Return total of retweets that the tweet has.

    :property: reply_count -> Return total of replies that the tweet has.

    :property: quote_count -> Return total of quotes that the tweet has.
    """

    def __init__(self, data=Dict[str, Any], **kwargs):
        self.original_payload = data
        self._public = data.get("public_metrics")

    def __str__(self) -> str:
        return f"<TweetPublicMetrics: like_count={self.like_count} retweeted_count={self.retweeted_count} reply_count={self.reply_count}> quote_count={self.quote_count}"

    def __repr__(self) -> str:
        return f"<TweetPublicMetrics>"

    @property
    def like_count(self) -> int:
        return self._public.get("like_count")

    @property
    def retweeted_count(self) -> int:
        return self._public.get("retweeted_count")

    @property
    def reply_count(self) -> int:
        return self._public.get("reply_count")

    @property
    def quote_count(self) -> int:
        return self._public.get("quote_count")