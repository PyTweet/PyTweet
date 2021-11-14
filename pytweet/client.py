from typing import List, Optional, Union

from .attachments import Geo, Poll, QuickReply
from .enums import ReplySetting, SpaceState
from .http import HTTPClient
from .message import DirectMessage, WelcomeMessage, WelcomeMessageRule, Message
from .space import Space
from .tweet import Tweet
from .user import User

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
    def account(self) -> Optional[User]:
        """:class:`Optional[User]`: Returns the client's account information, This returns in a user object.

        .. versionadded:: 1.2.0
        """
        attr = getattr(self, "_account_user", None)
        if not attr:
            self._set_account_user()
            return getattr(self, "_account_user", None)
        return attr

    def _set_account_user(self) -> None:
        if not self.http.access_token:
            return None

        self._account_user = self.fetch_user(self.http.access_token.partition("-")[0])

    def fetch_user(self, user_id: Union[str, int] = None) -> User:
        """A method for fetching user with the user's id.

        .. warning::
            This method uses api call and might cause ratelimit if used often!

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
            Represent the user id that you wish to get info to, If you dont have it you may use `fetch_user_by_username` because it only required the user's username.

        Returns
        ---------
        :class:`User`
            This method returns a :class:`User` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user(user_id, http_client=self.http)

    def fetch_user_by_username(self, username: str) -> User:
        """A method for fetching user with the user's username.

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
        """A method for fetching tweet with the tweet's id.

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
        """A method for fetching message with the message's event id.

        .. warning::
            This method uses api call and might cause ratelimit if used often! Recommended to use `get_message()` method, it only retrieves the client's message only.

        Parameters
        ------------
        event_id: Union[:class:`str`, :class:`int`]
            Represent the event's id that you wish to fetch with.

        Returns
        ---------
        :class:`DirectMessage`
            This method returns a :class:`DirectMessage` object.


        .. versionadded:: 1.2.0
        """
        return self.http.fetch_message(event_id, http_client=self.http)

    def tweet(
        self,
        text: str = None,
        *,
        poll: Optional[Poll] = None,
        geo: Optional[Union[Geo, str]] = None,
        quote_tweet: Optional[Union[str, int]] = None,
        direct_message_deep_link: Optional[str] = None,
        reply_setting: Optional[Union[ReplySetting, str]] = None,
        reply_to_tweet: Optional[Union[str, int]] = None,
        exclude_reply_users: Optional[List[Union[str, int]]] = None,
        super_followers_only: bool = False,
    ) -> Message:
        """Post a tweet directly to twitter from the given parameters.

        Parameters
        ------------
        text: :class:`str`
            The tweets text, it will showup as the main text in a tweet.
        poll: Optional[:class:`Poll`]
            The poll attachment.
        geo: Optional[Union[:class:`Geo`, :class:`str`]]
            The geo attachment, you can put an object that is an instance of :class:`Geo` or the place id in a string.
        quote_tweet: Optional[Union[:class:`str`, :class:`int`]]
            The tweet id you want to quote.
        direct_message_deep_link: Optional[:class:`str`]
            The direct message deep link, It will showup as a CTA(call-to-action) with button attachment. Example of direct message deep link:
        reply_setting: Optional[Union[:class:`ReplySetting`, :class:`str`]]
            The reply setting that you can set to minimize users that can reply. If None specified, the defauly 'everyone' can reply.
        reply_to_tweet: Optional[Union[:class:`str`, :class:`int`]]
            The tweet id you want to reply. If you have an instance of :class:`Tweet`, you can use the reply() method rather then using this method.
        exclude_reply_users: Optional[List[Union[:class:`str`, :class:`int`]]]
            Exclude the users when replying to a tweet, if you dont want to mention a reply with 3 mentions, You can use this argument and provide the user id you dont want to mention.
        super_followers_only: :class:`bool`
            Allows you to Tweet exclusively for super followers.

        Returns
        ---------
        :class:`Message`
            This method returns a :class:`Message` object.


        .. versionadded:: 1.1.0
        """
        res = self.http.post_tweet(
            text,
            poll=poll,
            geo=geo,
            quote_tweet=quote_tweet,
            direct_message_deep_link=direct_message_deep_link,
            reply_setting=reply_setting,
            reply_to_tweet=reply_to_tweet,
            exclude_reply_users=exclude_reply_users,
            super_followers_only=super_followers_only,
            http_client=self.http,
        )
        return res

    def create_welcome_message(
        self, name: str = None, text: str = None, *, quick_reply: QuickReply = None
    ) -> WelcomeMessage:
        """Create a welcome message which you can set with :class:`WelcomeMessage.set_rule()`.

        Parameters
        ------------
        name: :class:`str`
            A human readable name for the Welcome Message
        text: :class:`str`
            The welcome message's text. Please do not make this empty if you want to showup the text.
        quick_reply: :class:`QuickReply`
            The message QuickReply attachments.

        Returns
        ---------
        :class:`WelcomeMessage`
            This method returns :class:`WelcomeMessage` object.


        .. versionadded:: 1.3.5
        """
        data = {"welcome_message": {"message_data": {}}}

        message_data = data["welcome_message"]["message_data"]
        data["welcome_message"]["name"] = str(name)
        message_data["text"] = str(text)

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
            auth=True,
        )

        data = res.get("welcome_message")
        id = data.get("id")
        name = res.get("name")
        timestamp = data.get("created_timestamp")
        text = data.get("message_data").get("text")

        return WelcomeMessage(
            name,
            text=text,
            welcome_message_id=id,
            timestamp=timestamp,
            http_client=self.http,
        )

    def fetch_welcome_message(self, welcome_message_id: Union[str, int]) -> WelcomeMessage:
        """Fetch the welcome message with the given welcome message id argument.

        Parameters
        ------------
        welcome_message_id: Union[:class:`str`, :class:`int`]
            Represent the welcome message id that you wish to fetch with.

        Returns
        ---------
        :class:`WelcomeMessage`
            This method returns :class:`WelcomeMessage` object.


        .. versionadded:: 1.3.5
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/direct_messages/welcome_messages/show.json",
            params={"id": str(welcome_message_id)},
            auth=True,
        )
        data = res.get("welcome_message")
        message_data = data.get("message_data")
        id = data.get("id")
        timestamp = data.get("created_timestamp")
        text = message_data.get("text")
        return WelcomeMessage(text=text, welcome_message_id=id, timestamp=timestamp, http_client=self.http)

    def fetch_welcome_message_rules(self, welcome_message_rules_id: Union[str, int]) -> WelcomeMessageRule:
        """A method for fetching a welcome message rules.

        Parameters
        ------------
        welcome_message_rules_id: Union[:class:`str`, :class:`int`]
            Represent the welcome message rule id that you wish to fetch with.

        Returns
        ---------
        :class:`WelcomeMessageRule`
            This method returns :class:`WelcomeMessageRule` object.


        .. versionadded:: 1.3.5
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/direct_messages/welcome_messages/rules/show.json",
            params={"id": str(welcome_message_rules_id)},
            auth=True,
        )
        data = res.get("welcome_message_rule")
        id = data.get("id")
        timestamp = data.get("created_timestamp")
        welcome_message_id = data.get("welcome_message_id")
        return WelcomeMessageRule(id, welcome_message_id, timestamp, http_client=self)

    def fetch_space(self, space_id: Union[str, int]) -> Space:
        """A method for fetching a space.

        Parameters
        ------------
        space_id: Union[:class:`str`, :class:`int`]
            Represent the space id that you wish to fetch with.

        Returns
        ---------
        :class:`Space`
            This method returns a :class:`Space` object.


        .. versionadded:: 1.3.5
        """
        return self.http.fetch_space(space_id)

    def fetch_space_by_title(self, title: str, state: SpaceState = SpaceState.live) -> Space:
        """Fetch a space using its title.

        Parameters
        ------------
        title: Union[:class:`str`, :class:`int`]
            The space title that you are going use for fetching the space.
        state: :class:`SpaceState`
            The type of state the space has. There's only 2 type: SpaceState.live indicates that the space is live and SpaceState.scheduled indicates the space is not live and scheduled by the host. Default to SpaceState.live

        Returns
        ---------
        :class:`Space`
            This method returns a :class:`Space` object.


        .. versionadded:: 1.3.5
        """
        Space = self.http.fetch_space_bytitle(title, state)
        return Space

    def get_message(self, event_id: Union[str, int] = None) -> Optional[DirectMessage]:
        """Get a direct message through the client message cache. Return None if the message is not in the cache.

        .. note::
            Note that, only the client's tweet is going to be stored in the cache which mean you can't get someone's message other then the client itself from the cache.

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
        """Get a tweet through the client internal tweet cache. Return None if the tweet is not in the cache.

        .. note::
            Note that, only the client's tweet is going to be stored in the cache which mean you can't get someone's tweet other then the client itself from the cache.

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
            raise ValueError("tweet_id must be an integer or a string of digits.")

        return self.http.message_cache.get(tweet_id)

    def search_geo(
        self,
        query: str,
        *,
        lat: Optional[int] = None,
        long: Optional[int] = None,
        ip: Optional[Union[str, int]] = None,
        granularity: str = "neighborhood",
        max_results: Optional[Union[str, int]] = None,
    ) -> Geo:
        """Search a location with the given arguments.

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
        max_results: Optional[Union[:class:`str`, :class:`int`]]
            A hint as to the number of results to return. This does not guarantee that the number of results returned will equal max_results, but instead informs how many "nearby" results to return. Ideally, only pass in the number of places you intend to display to the user here

        Returns
        ---------
        :class:`Geo`
            This method return a :class:`Geo` object.


        .. versionadded:: 1.5.3
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

        return [Geo(data) for data in data.get("result").get("places")]
