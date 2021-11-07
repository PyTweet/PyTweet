from typing import Any, Optional, Union

from .http import HTTPClient
from .tweet import Tweet
from .user import User
from .message import DirectMessage

__all__ = ("Client",)


class Client:
    """Represent a client that connected to Twitter!

    Parameters
    ------------
    bearer_token: Optional[:class:`str`]
        The Bearer Token of the app. The most important one, because this make most of the requests for twitter's api version 2.
    consumer_key: Optional[:class:`str`]
        The Consumer Key of the app.
    consumer_key_secret: Optional[:class:`str`]
        The Consumer Key Secret of the app.
    access_token: Optional[:class:`str`]
        The Access Token of the app.
    access_token_secret: Optional[:class:`str`]
        The Access Token Secret of the app.

    Attributes
    ------------
    http: Optional[:class:`HTTPClient`]
        Return the HTTPClient, HTTPClient is responsible for making most of the Requests.


    .. versionadded:: 1.0.0
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
        me = self.fetch_user(my_id)
        return me

    def fetch_user(self, user_id: Union[str, int]) -> User:
        """:class:`User`: A function for HTTPClient.fetch_user().

            .. warning::
                This method uses api call and might cause ratelimit if used often!

            Parameters
            ------------
            user_id: Union[:class:`str`, :class:`int`]
                Represent the user id that you wish to get info to, If you dont have it you may use `fetch_user_byusername` because it only required the user's username.

            Returns
            ---------
            :class:`User`
                This method returns a :class:`User` object.

        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user(user_id, http_client=self.http)

    def fetch_user_by_username(self, username: str) -> User:
        """:class:`User`: A function for HTTPClient.fetch_user_byusername().

            .. warning::
                This method uses api call and might cause ratelimit if used often!

            Parameters
            ------------
            username: :class:`str`
                Represent the user's username that you wish to get info. A Username usually start with '@' before any letters. If a username named @Jack,then the username argument must be 'Jack'.

            Returns
            ---------
            :class:`User`
                This method returns a :class:`User` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user_byusername(username, http_client=self.http)

    def fetch_tweet(self, tweet_id: Union[str, int]) -> Tweet:
        """:class:`Tweet`: A function for HTTPClient.fetch_tweet().

            .. warning::
            This method uses api call and might cause ratelimit if used often! More recommended to use get_tweet to get the client's tweet.

            Parameters
            ------------
            tweet_id: Union[:class:`str`, :class:`int`]
            Represent the tweet id that you wish to get info to.

            Returns
            ---------
            :class:`Tweet`
                This method returns a :class:`Tweet` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_tweet(tweet_id, http_client=self.http)

    def fetch_message(self, event_id: Union[str, int]) -> DirectMessage:
        """:class:`DirectMessage`: A function for HTTPClient.fetch_message().

            .. warning::
                This method uses api call and might cause ratelimit if used often! Recommended to use `get_message()` method, it only retrieves the client's message only.

            Parameters
            ------------
            event_id: Union[:class:`str`, :class:`int`]
                Represent the tweet id that you wish to fetch.

            Returns
            ---------
            :class:`DirectMessage`
                This method returns a :class:`DirectMessage` object.

        .. versionadded:: 1.2.0
        """
        return self.http.fetch_message(event_id, http_client=self.http)

    def tweet(self, text: str, **kwargs: Any) -> Tweet:
        """:class:`Tweet`: Post a tweet directly to twitter from the given parameters.

            Parameters
            ------------
            text: :class:`str`
                The tweets text, it will showup as the main text in a tweet.

            Returns
            ---------
            :class:`Tweet`
                This method returns a :class:`Tweet` object.

        .. versionadded:: 1.1.0
        """
        http_client = kwargs.get("http_client", None)
        res = self.http.post_tweet(text, http_client=http_client if http_client else self.http, **kwargs)
        return res

    def get_message(self, event_id: Union[str, int]) -> Optional[DirectMessage]:
        """Optional[:class:`DirectMessage`]: Get a direct message through the client message cache. Return None if the message is not in the cache.

            .. note::
                Note that, only the client's message stored in the cache!

            Parameters
            ------------
            event_id: Union[:class:`str`, :class:`int`]
                The event id of the Direct Message event that you want to get.

            Returns
            ---------
            :class:`DirectMessage`
                This method returns a :class:`DirectMessage` object.

        .. versionadded:: 1.2.0
        """
        try:
            event_id = int(event_id)
        except ValueError:
            raise ValueError("Event id must be an integer or a :class:`str`ing of digits.")

        return self.http.message_cache.get(event_id)

    def get_tweet(self, tweet_id: Union[str, int]) -> Optional[Tweet]:
        """Optional[:class:`Tweet`]: Get a tweet through the client tweet cache. Return None if the tweet is not in the cache.

            .. note::
                Note that, only the client's tweet is going to be stored.

            Parameters
            ------------
            event_id: Union[:class:`str`, :class:`int`]
                The id of a tweet that you want to get.

            Raises
            --------
            ValueError:
                Raise when the tweet_id argument is not an integer or a string of digits.

            Returns
            ---------
            :class:`Tweet`
                This method returns a :class:`Tweet` object or None if the tweet was not found.

        .. versionadded:: 1.2.0
        """
        try:
            tweet_id = int(tweet_id)
        except ValueError:
            raise ValueError("tweet_id must be an integer or a :class:`str`ing of digits.")

        return self.http.message_cache.get(tweet_id)
