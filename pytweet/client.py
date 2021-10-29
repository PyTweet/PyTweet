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

from typing import Optional, Union
from .http import HTTPClient, Route
from .user import User
from .tweet import Tweet


class Client:
    """Represent a client that connected to Twitter!
    This client will interact with other through twitter's api version 2!
    Version Added: 1.0.0

    Parameters:
    -----------
    bearer_token: str
        The Bearer Token of the app. The most important one, because this make most of the requests for twitter's api version 2.

    consumer_key: Optional[str]
        The Consumer Key of the app.

    consumer_key_secret: Optional[str]
        The Consumer Key Secret of the app.

    access_token: Optional[str]
        The Access Token of the app.

    access_token_secret: Optional[str]
        The Access Token Secret of the app.

    Attributes:
    -----------
    http: Optional[HTTPClient]
        Return a :class: HTTPClient, HTTPClient is responsible for making most of the Requests to twitter's api.
    """

    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: str = None,
        consumer_key_secret: str = None,
        access_token: str = None,
        access_token_secret: str = None,
    ):
        self.http = HTTPClient(
            bearer_token,
            consumer_key = consumer_key,
            consumer_key_secret = consumer_key_secret,
            access_token = access_token,
            access_token_secret = access_token_secret,
        )

    def __repr__(self) -> str:
        return "Client(bearer_token=SECRET consumer_key=SECRET consumer_key_secret=SECRET access_token=SECRET access_token_secret=SECRET)"

    @property
    def user(self) -> Optional[User]:
        """:class:User: Return the client in user object, return None if access token isnt specified.
        Version Added: 1.2.0
        """
        if not self.http.access_token:
            return None
            
        my_id = self.http.access_token.partition("-")[0]
        me=self.get_user(my_id)
        return me

    def get_user(self, user_id: Union[str, int]) -> User:
        """A function for HTTPClient.fetch_user().
        Version Added: 1.0.0

        This function return a :class: User object.
        """
        return self.http.fetch_user(user_id, self.http)

    def get_user_by_username(self, username: str) -> User:
        """A function for HTTPClient.fetch_user_byusername().
        Version Added: 1.0.0

        This function return a :class: User object.
        """
        return self.http.fetch_user_byusername(username, self.http)

    def get_tweet(self, tweet_id: Union[str, int]) -> Tweet:
        """A function for HTTPClient.fetch_tweet().
        Version Added: 1.0.0

        This function return a :class: Tweet.
        """
        return self.http.fetch_tweet(tweet_id, self.http)

    def tweet(self, text: str, **kwargs):
        """Post a tweet directly to twitter from the given paramaters.
        Version Added: 1.1.0

        text: str
            The tweets text, it will showup as the main text in a tweet.
        """
        self.http.post_tweet(text, **kwargs)

    def stream(self):
        """Stream in real-time, roughly a 1% sample of all public Tweets.
        Version Added: 1.1.0
        """
        self.http.request(
            Route("GET", "2", "/tweets/sample/stream"),
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
        )
