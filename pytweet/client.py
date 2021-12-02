from typing import List, Optional, Union, Callable
from asyncio import iscoroutinefunction

from .attachments import Geo, Poll, QuickReply, File, CustomProfile, CTA
from .errors import PytweetException, UnKnownSpaceState
from .enums import ReplySetting, SpaceState
from .http import HTTPClient
from .message import DirectMessage, WelcomeMessage, WelcomeMessageRule, Message
from .space import Space
from .tweet import Tweet
from .user import User
from .stream import Stream

__all__ = ("Client",)


class Client:
    """Represent a client that connected to Twitter!

    Parameters
    ------------
    bearer_token: Optional[:class:`str`]
        The Bearer Token of the app. The most important one, because this makes most of the requests for Twitter's api version 2.
    consumer_key: Optional[:class:`str`]
        The Consumer Key of the app.
    consumer_key_secret: Optional[:class:`str`]
        The Consumer Key Secret of the app.
    access_token: Optional[:class:`str`]
        The Access Token of the app.
    access_token_secret: Optional[:class:`str`]
        The Access Token Secret of the app.
    stream: Optional[Stream]
        The client's stream. Must be an instance of :class:`Stream`.

    Attributes
    ------------
    http: Optional[:class:`HTTPClient`]
        Returns the HTTPClient,  the HTTPClient is responsible for making most of the Requests.


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
        stream: Optional[Stream] = None,
    ) -> None:
        self.http = HTTPClient(
            bearer_token,
            consumer_key=consumer_key,
            consumer_key_secret=consumer_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            stream=stream,
        )

    def __repr__(self) -> str:
        return "Client(bearer_token=SECRET consumer_key=SECRET consumer_key_secret=SECRET access_token=SECRET access_token_secret=SECRET)"

    @property
    def account(self) -> Optional[User]:
        """Optional[:class:`User`]: Returns the client's account information. The callback is a User object.

        .. versionadded:: 1.2.0
        """
        attr = getattr(self, "_account_user", None)
        if not attr:
            self._set_account_user()
            return getattr(self, "_account_user", None)
        return attr

    def event(self, func: Callable) -> None:
        """
        A decorator for making an event, the event will be register in the client's internal cache.

        Parameters
        ------------
        func: :class:`typing.Callable`
            The function that execute when the event is trigger. The event must be a synchronous function. You must also put the right event name in the function's name, See event reference for full events name.


        .. seealso::
            Event Reference
                See the `Event Reference`.


        .. versionadded:: 1.3.5
        """
        if iscoroutinefunction(func):
            raise TypeError("Event must be a synchronous function!")
        self.http.events[func.__name__[3:]] = func

    def _set_account_user(self) -> None:
        if not self.http.access_token:
            return None

        self._account_user = self.fetch_user(self.http.access_token.partition("-")[0])

    def fetch_user(self, user_id: Union[str, int] = None) -> Optional[User]:
        """A method for fetching the user with the user's id.

        .. warning::
            This method uses API call and might cause ratelimits if used often!

        Parameters
        ------------
        user_id: Union[:class:`str`, :class:`int`]
            Represents the user ID that you wish to get info for. If you don't have it you may use `fetch_user_by_name` because it only requires the user's username.

        Returns
        ---------
        :class:`User`
            This method returns a :class:`User` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user(user_id)

    def fetch_user_by_name(self, username: str) -> Optional[User]:
        """A method for fetching the user with the user's username.

        .. warning::
            This method uses API call and might cause ratelimits if used often!

        Parameters
        ------------
        username: :class:`str`
            Represents the user's username that you wish to get info. A Username usually starts with '@' before any letters. If a username named @Jack, then the username argument must be 'Jack'.

        Returns
        ---------
        :class:`User`
            This method returns a :class:`User` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user_byname(username)

    def fetch_tweet(self, tweet_id: Union[str, int] = None) -> Tweet:
        """A method for fetching tweet with the tweet's id.

        .. warning::
            This method uses API call and might cause ratelimits if used often! More recommended is to use get_tweet to get the client's tweet.

        Parameters
        ------------
        tweet_id: Union[:class:`str`, :class:`int`]
            Represents the tweet id that you wish to get info about.

        Returns
        ---------
        :class:`Tweet`
            This method returns a :class:`Tweet` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_tweet(tweet_id)

    def fetch_message(self, event_id: Union[str, int] = None) -> DirectMessage:
        """A method for fetching the message with the message's event ID.

        .. warning::
            This method uses API call and might cause ratelimit if used often! It is more ecommended to use `get_message()` method, as it only retrieves the client's message only.

        Parameters
        ------------
        event_id: Union[:class:`str`, :class:`int`]
            Represents the event's ID that you wish to fetch with.

        Returns
        ---------
        :class:`DirectMessage`
            This method returns a :class:`DirectMessage` object.


        .. versionadded:: 1.2.0
        """
        return self.http.fetch_message(event_id)

    def tweet(
        self,
        text: str = None,
        *,
        file: Optional[File] = None,
        poll: Optional[Poll] = None,
        geo: Optional[Union[Geo, str]] = None,
        quote_tweet: Optional[Union[str, int]] = None,
        direct_message_deep_link: Optional[str] = None,
        reply_setting: Optional[Union[ReplySetting, str]] = None,
        reply_tweet: Optional[Union[str, int]] = None,
        exclude_reply_users: Optional[List[Union[str, int]]] = None,
        super_followers_only: bool = False,
    ) -> Message:
        """Posts a tweet directly to twitter from the given parameters.

        Parameters
        ------------
        text: :class:`str`
            The tweet's text, it will show up as the main text in a tweet.
        file: Optional[:class:`File`]
            Represent a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
        poll: Optional[:class:`Poll`]
            The poll attachment.
        geo: Optional[Union[:class:`Geo`, :class:`str`]]
            The geo attachment, you can put an object that is an instance of :class:`Geo` or the place ID in a string.
        quote_tweet: Optional[Union[:class:`str`, :class:`int`]]
            The tweet ID you want to quote.
        direct_message_deep_link: Optional[:class:`str`]
            The direct message deep link, It will showup as a CTA(call-to-action) with button attachment. Example of direct message deep link:
        reply_setting: Optional[Union[:class:`ReplySetting`, :class:`str`]]
            The reply setting that you can set to minimize users that can reply. If None is specified, the default is set to 'everyone' can reply.
        reply_tweet: Optional[Union[:class:`str`, :class:`int`]]
            The tweet ID you want to reply to. If you have an instance of :class:`Tweet`, you can use the reply() method rather then using this method.
        exclude_reply_users: Optional[List[Union[:class:`str`, :class:`int`]]]
            Exclude the users when replying to a tweet, if you dont want to mention a reply with 3 mentions, You can use this argument and provide the user id you don't want to mention.
        super_followers_only: :class:`bool`
            Allows you to tweet exclusively for super followers.

        Returns
        ---------
        :class:`Message`
            This method returns a :class:`Message` object.


        .. versionadded:: 1.1.0
        """
        return self.http.post_tweet(
            text,
            file=file,
            poll=poll,
            geo=geo,
            quote_tweet=quote_tweet,
            direct_message_deep_link=direct_message_deep_link,
            reply_setting=reply_setting,
            reply_tweet=reply_tweet,
            exclude_reply_users=exclude_reply_users,
            super_followers_only=super_followers_only,
        )

    def create_welcome_message(
        self,
        name: Optional[str] = None,
        text: Optional[str] = None,
        *,
        file: Optional[File] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> WelcomeMessage:
        """Create a welcome message which you can set with :class:`WelcomeMessage.set_rule()`.

        Parameters
        ------------
        name: Optional[:class:`str`]
            A human readable name for the Welcome Message
        text: Optional[:class:`str`]
            The welcome message's text. Please do not make this empty if you don't want the text to be blank.
        file: Optional[:class:`File`]:
            Represent a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
        quick_reply: Optional[:class:`QuickReply`]
            The message's :class:`QuickReply` attachments.
        cta: Optional[:class:`CTA`]
            The message's :class:`CTA` attachment.

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

        if file:
            media_id = self.http.upload(file, "INIT")
            self.http.upload(file, "APPEND", media_id=media_id)
            self.http.upload(file, "FINALIZE", media_id=media_id)
            message_data["attachment"] = {}
            message_data["attachment"]["type"] = "media"
            message_data["attachment"]["media"] = {}
            message_data["attachment"]["media"]["id"] = str(media_id)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

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
            id=id,
            timestamp=timestamp,
            http_client=self.http,
        )

    def fetch_welcome_message(self, welcome_message_id: Union[str, int]) -> WelcomeMessage:
        """Fetches the welcome message with the given welcome message ID argument.

        Parameters
        ------------
        welcome_message_id: Union[:class:`str`, :class:`int`]
            Represents the welcome message ID that you wish to fetch with.

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
        return WelcomeMessage(text=text, id=id, timestamp=timestamp, http_client=self.http)

    def fetch_welcome_message_rules(self, welcome_message_rules_id: Union[str, int]) -> WelcomeMessageRule:
        """A method for fetching a welcome message rules.

        Parameters
        ------------
        welcome_message_rules_id: Union[:class:`str`, :class:`int`]
            Represents the welcome message rule ID that you wish to fetch with.

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
        return WelcomeMessageRule(id, welcome_message_id, timestamp, http_client=self.http)

    def fetch_space(self, space_id: Union[str, int]) -> Space:
        """A method for fetching a space.

        Parameters
        ------------
        space_id: Union[:class:`str`, :class:`int`]
            Represents the space ID that you wish to fetch with.

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
            The type of state the space has. There are only 2 types: SpaceState.live indicates that the space is live and SpaceState.scheduled indicates the space is not live and scheduled by the host. Default to SpaceState.live

        Returns
        ---------
        :class:`Space`
            This method returns a :class:`Space` object.


        .. versionadded:: 1.3.5
        """
        if state == SpaceState.live or state == SpaceState.scheduled:
            return self.http.fetch_space_bytitle(title, state)
        else:
            raise UnKnownSpaceState(given_state=state)

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
            The longitude to search around. The valid ranges for longitude are -180.0 to +180.0 (East is positive) inclusive. This parameter will be ignored if outside that range, if it is not a number, if geo_enabled is turned off, or if there is not a corresponding lat parameter.
        ip: Union[:class:`str`, :class:`int`]
            An IP address. Used when attempting to fix geolocation based off of the user's IP address.
        granularity: :class:`str`
            This is the minimal granularity of place types to return and must be one of: neighborhood ,ity ,admin or country. If no granularity is provided for the request neighborhood is assumed. Setting this to city, for example, will find places which have a type of city, admin or country
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

    def get_message(self, event_id: Union[str, int] = None) -> Optional[DirectMessage]:
        """Get a direct message through the client message cache. Returns None if the message is not in the cache.

        .. note::
            Note that only the client's tweet is going to be stored in the cache which means you can't get someone's message other then the client itself from the cache.

        Parameters
        ------------
        event_id: Union[:class:`str`, :class:`int`]
            The event ID of the Direct Message event that you want to get.

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
        """Gets a tweet through the client internal tweet cache. Return None if the tweet is not in the cache.

        .. note::
            Note that, only the client's tweet is going to be stored in the cache which mean you can't get someone's tweet other then the client itself from the cache.

        Parameters
        ------------
        event_id: Union[:class:`str`, :class:`int`]
            The ID of a tweet that you want to get.

        Raises
        --------
        ValueError:
            Raised when the tweet_id argument is not an integer or a string of digits.

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

    def create_custom_profile(self, name: str, file: File) -> CustomProfile:
        """Create a custom profile

        Parameters
        ------------
        name: :class:`str`
            The author's custom name.
        file: :class:`File`
            The media file that's associate with the profile.

        Returns
        ---------
        :class:`CustomProfile`
            This method returns a :class:`CustomProfile` object.
        """
        if not isinstance(file, File):
            raise PytweetException("'file' argument must be an instance of pytweet.File")

        media_id = self.http.upload(file, "INIT")
        self.http.upload(file, "APPEND", media_id=media_id)
        self.http.upload(file, "FINALIZE", media_id=media_id)

        data = {"custom_profile": {"name": name, "avatar": {"media": {"id": media_id}}}}

        res = self.http.request("POST", "1.1", "/custom_profiles/new.json", json=data, auth=True)
        data = res.get("custom_profile")

        return CustomProfile(
            data.get("name"),
            data.get("id"),
            data.get("created_timestamp"),
            data.get("avatar"),
        )

    def register_webhook_url(self, url: str, env_label: str):
        return 0

        json = self.http.request(
            "POST", "1.1", f"/account_activity/all/{env_label}/webhooks.json", auth=True, params={"url": url}
        )
        return json

    def stream(self, *, dry_run: bool = False) -> None:
        """Stream realtime in twitter! Make sure to put stream kwarg in client. If you want the tweet data make sure to make an `on_stream` event. example:

        .. code-block:: py

            @client.event
            def on_stream(tweet, connection):
                ... #Do what you want with tweet and connection you got.


        Parameters
        ------------
        dry_run: :class:`bool`
            Indicates if you want to debug your rule's operator syntax.


        .. versionadded:: 1.3.5
        """
        if not self.http.stream:
            raise TypeError("'stream' argument is missing in client!")

        try:
            self.http.stream.connect(dry_run=dry_run)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt: Exit stream.")
