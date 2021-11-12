from typing import Any, Optional, Union

from .http import HTTPClient
from .tweet import Tweet
from .user import User
from .message import DirectMessage, WelcomeMessage, WelcomeMessageRule
from .attachments import Geo, QuickReply

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

    def fetch_user(self, user_id: Union[str, int] = None) -> User:
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

    def fetch_tweet(self, tweet_id: Union[str, int] = None) -> Tweet:
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

    def fetch_message(self, event_id: Union[str, int] = None) -> DirectMessage:
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

    def create_welcome_message(self, name: str = None, text: str = None, *,quick_reply: QuickReply = None):
        """Make a default welcome message for the client. 
        
        Parameters
        ------------
        name: :class:`str`
            A human readable name for the Welcome Message
        text: :class:`str`
            The welcome message's text. Please do not make this empty if you want to showup the text.
        quick_reply: :class:`QuickReply`
            The message QuickReply attachments.

        .. versionadded:: 1.3.5
        """
        data={
            "welcome_message": {
                "message_data": {

                }
            }
        }

        message_data = data["welcome_message"]["message_data"]
        data["welcome_message"]["name"] = str(name)
        message_data['text'] = str(text)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.options,
            }

        
        res = self.http.request(
            "POST",
            "1.1",
            "/direct_messages/welcome_messages/new.json",
            json=data,
            auth=True
        )
        print(res)

        data = res.get("welcome_message")
        id = data.get("id")
        name = res.get("name")
        timestamp = data.get('created_timestamp')
        text = data.get("message_data").get("text")

        return WelcomeMessage(name, text = text, welcome_message_id = id, timestamp = timestamp, http_client=self.http)

    def fetch_welcome_message(self, welcome_message_id: Union[str, int]) -> WelcomeMessage:
        """Fetch the welcome message with the given welcome message id argument.

        Parameters
        ------------
        welcome_message_id: Union[:class:`str`, :class:`int`]
            The welcome message id you want to delete.

        .. versionadded:: 1.3.5
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/direct_messages/welcome_messages/show.json",
            params={
                "id": str(welcome_message_id)
            },
            auth=True
        )
        data = res.get("welcome_message")
        message_data = data.get("message_data")
        id = data.get('id')
        timestamp = data.get('created_timestamp')
        text = message_data.get("text")
        return WelcomeMessage(text = text, welcome_message_id = id, timestamp = timestamp, http_client=self.http)

    def fetch_welcome_message_rules(self, welcome_message_rules_id: Union[str, int]) -> WelcomeMessageRule:
        """Fetch the welcome message rules with the given welcome message rules id argument.

        Parameters
        ------------
        welcome_message_rules_id: Union[:class:`str`, :class:`int`]
            The welcome message rules id you want to delete.

        .. versionadded:: 1.3.5
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/direct_messages/welcome_messages/rules/show.json",
            params={
                "id": str(welcome_message_rules_id)
            },
            auth=True
        )
        data = res.get("welcome_message_rule")
        id = data.get("id")
        timestamp = data.get("created_timestamp")
        welcome_message_id = data.get("welcome_message_id")
        return WelcomeMessageRule(id, welcome_message_id, timestamp, http_client = self)

    def get_message(self, event_id: Union[str, int] = None) -> Optional[DirectMessage]:
        """Get a direct message through the client message cache. Return None if the message is not in the cache.

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

    def get_tweet(self, tweet_id: Union[str, int] = None) -> Optional[Tweet]:
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

    def search_geo(
        self,
        query: str,
        used_type: str = "shared_place",
        *,
        lat: int = None,
        long: int = None,
        ip: Union[str, int] = None,
        granularity: str = "neighborhood",
        max_results: Union[str, int] = None,
    ) -> Geo:
        """:class:`Geo`: Get a location information from the given parameters.

        Parameters
        ------------
        query: :class:`str`
            Free-form text to match against while executing a geo-based query, best suited for finding nearby locations by name. Remember to URL encode the query.
        lat: :class:`int`
            The latitude to search around. This parameter will be ignored unless it is inside the range -90.0 to +90.0 (North is positive) inclusive. It will also be ignored if there isn't a corresponding long parameter.
        long: :class:`int`
            The longitude to search around. The valid ranges for longitude are -180.0 to +180.0 (East is positive) inclusive. This parameter will be ignored if outside that range, if it is not a number, if geo_enabled is turned off, or if there not a corresponding lat parameter.
        ip: Union[:class:`str`, :class:`int`]
            An IP address. Used when attempting to fix geolocation based off of the user's IP address.
        granularity: :class:`str`
            This is the minimal granularity of place types to return and must be one of: neighborhood , city , admin or country. If no granularity is provided for the request neighborhood is assumed. Setting this to city, for example, will find places which have a type of city, admin or country
        max_results:
            A hint as to the number of results to return. This does not guarantee that the number of results returned will equal max_results, but instead informs how many "nearby" results to return. Ideally, only pass in the number of places you intend to display to the user here

        Returns
        ---------
        :class:`Geo`
            This method return a :class:`Geo` objects.
        """

        if query:
            query = query.replace(" ", "%20")

        data = self.http.request(
            "GET",
            "1.1",
            "/geo/search.json",
            params={
                "query": query,
                "lat": lat,
                "long": long,
                "ip": ip,
                "granularity": granularity,
                "max_results": max_results,
            },
            auth=True,
        )

        return [Geo(data, used_type=used_type) for data in data.get("result").get("places")] 
