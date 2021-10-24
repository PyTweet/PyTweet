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
    """Represent a PublicMetrics for a User.
    This PublicMetrics contain public info about the user.
    Version Added: 1.1.0

    Parameters:
    ===================
    data: Dict[str, Any]
        The complete data of the user's public metrics through a dictionary!

    Attributes:
    ===================
    original_payload
        Return the original payload of the user.

    _public
        Returns the user public metrics.
    """

    def __init__(self, data=Dict[str, Any], **kwargs):
        self.original_payload = data
        self._public = self.original_payload.get("public_metrics")

    def __repr__(self) -> str:
        return "UserPublicMetrics(user={0.original_payload.get('username')} followers_count={0._payload.get('followers_count')} following_count={0._payload.get('following_count')} tweet_count={0._payload.get('tweet_count')})".format(
            self
        )

    @property
    def followers_count(self) -> int:
        """int: Returns total of followers that a user has.
        Version Added: 1.1.0
        """
        return int(self._public.get("followers_count"))

    @property
    def following_count(self) -> int:
        """int: Returns total of following that a user has.
        Version Added: 1.1.0
        """
        return int(self._public.get("following_count"))

    @property
    def tweet_count(self) -> int:
        """int: Returns total of tweet that a user has.
        Version Added: 1.1.0
        """
        return int(self._public.get("tweet_count"))

    @property
    def listed_count(self) -> int:
        """int: Returns total of listed that a user has.
        Version Added: 1.1.0
        """
        return int(self._public.get("listed_count"))

class TweetPublicMetrics:
    """Represent a PublicMetrics for a tweet.
    This PublicMetrics contain public info about the tweet.
    Version Added: 1.1.0

    Parameters:
    ===================
    data: Dict[str, Any]:
        The complete data of the tweet's public metrics keep in a dictionary.

    Attributes:
    ===================
    original_payload
        Return the original payload of the tweet.

    _public
        Returns the user public metrics.
    """

    def __init__(self, data=Dict[str, Any], **kwargs):
        self.original_payload = data
        self._public = data.get("public_metrics")

    def __repr__(self) -> str:
        return "TweetPublicMetrics(like_count={0.like_count} retweeted_count={0.retweeted_count} reply_count={0.reply_count}> quote_count={0.quote_count})".format(
            self
        )

    @property
    def like_count(self) -> int:
        """int: Return total of likes that the tweet has.
        Version Added: 1.1.0
        """
        return int(self._public.get("like_count"))

    @property
    def retweeted_count(self) -> int:
        """int: Return total of retweetes that the tweet has.
        Version Added: 1.1.0
        """
        return int(self._public.get("retweeted_count"))

    @property
    def reply_count(self) -> int:
        """int: Return total of replies that the tweet has.
        Version Added: 1.1.0
        """
        return int(self._public.get("reply_count"))

    @property
    def quote_count(self) -> int:
        """int: Return total of quotes that the tweet has.
        Version Added: 1.1.0
        """
        return int(self._public.get("quote_count"))