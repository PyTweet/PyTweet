from typing import Any, Optional, Union

from .http import HTTPClient
from .tweet import Tweet
from .user import User

__all__ = ("Client",)


class Client:
    """Represent a client that connected to Twitter!
    This client will interact with other through twitter's api version 2!
    .. versionadded:: 1.1.0

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
        Return a :class:`HTTPClient`, HTTPClient is responsible for making most of the Requests.
    """

    def __init__(
        self,
        bearer_token: Optional[str],
        *,
        consumer_key: Optional[str] = None,
        consumer_key_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_token_secret: Optional[str] = None,
    ) -> None:
        self.http = HTTPClient(
            bearer_token,
            consumer_key=consumer_key,
            consumer_key_secret=consumer_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def __repr__(self) -> str:
        return "Client(bearer_token=SECRET consumer_key=SECRET consumer_key_secret=SECRET access_token=SECRET access_token_secret=SECRET)"

    @property
    def user(self) -> Optional[User]:
        """:class:`User`: Returns the client in user object, return None if access token isn't specified.
        .. versionadded:: 1.2.0
        """
        if not self.http.access_token:
            return None

        my_id = self.http.access_token.partition("-")[0]
        me = self.get_user(my_id)
        return me

    def get_user(self, user_id: Union[str, int]) -> User:
        """A function for HTTPClient.fetch_user().
        .. versionadded:: 1.1.0

        Parameters:
        -----------
        user_id: Union[str, int]
            Represent the user id that you wish to get info to, If you dont have it you may use `fetch_user_byusername` because it only required the user's username.

        This function returns a :class:`User` object.
        """
        return self.http.fetch_user(user_id, http_client=self.http)

    def get_user_by_username(self, username: str) -> User:
        """A function for HTTPClient.fetch_user_byusername().
        .. versionadded:: 1.1.0

        Parameters:
        -----------
        username: Union[str, int]
            Represent the user's username that you wish to get info. A Username usually start with '@' before any letters. If a username named @Jack,then the username argument must be 'Jack'.

        This function returns a :class:`User` object.
        """
        return self.http.fetch_user_byusername(username, http_client=self.http)

    def get_tweet(self, tweet_id: Union[str, int]) -> Tweet:
        """A function for HTTPClient.fetch_tweet().
        .. versionadded:: 1.1.0

        Parameters:
        -----------
        tweet_id: Union[str, int]
            Represent the tweet id that you wish to get info to.

        This function returns a :class:`Tweet`.
        """
        return self.http.fetch_tweet(tweet_id, http_client=self.http)

    def tweet(self, text: str, **kwargs: Any) -> None:
        """Post a tweet directly to twitter from the given parameters.
        .. versionadded:: 1.1.0

        text: str
            The tweets text, it will showup as the main text in a tweet.
        """
        self.http.post_tweet(text, **kwargs)
