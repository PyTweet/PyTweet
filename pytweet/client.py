from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import threading
import time

from urllib.parse import urlparse
from asyncio import iscoroutinefunction
from http import HTTPStatus
from typing import Callable, List, Optional, Union, Any
from flask import Flask, request

from .attachments import CTA, CustomProfile, File, Geo, Poll, QuickReply
from .enums import ReplySetting, SpaceState
from .errors import PytweetException, UnKnownSpaceState
from .http import HTTPClient
from .message import DirectMessage, Message, WelcomeMessage, WelcomeMessageRule
from .space import Space
from .stream import Stream
from .tweet import Tweet
from .user import User, ClientAccount
from .environment import Environment, Webhook
from .dataclass import Location, Trend

__all__ = ("Client",)

_log = logging.getLogger(__name__)


class Client:
    """Represents a twitter-api client for twitter api version 1.1 and 2 interface.

    Parameters
    ------------
    bearer_token: Optional[:class:`str`]
        The Bearer Token of the app. The most important one, because this makes most of the requests for Twitter's api version 2.
    consumer_key: Optional[:class:`str`]
        The Consumer Key of the app.
    consumer_secret: Optional[:class:`str`]
        The Consumer Key Secret of the app.
    access_token: Optional[:class:`str`]
        The Access Token of the app.
    access_token_secret: Optional[:class:`str`]
        The Access Token Secret of the app.
    stream: Optional[Stream]
        The client's stream. Must be an instance of :class:`Stream`.
    callback: Optional[:class:`str`]
        The oauth callback url, default to None.

    Attributes
    ------------
    http: Optional[:class:`HTTPClient`]
        Returns the HTTPClient,  the HTTPClient is responsible for making most of the Requests.
    webhook: Optional[:class:`Webhook`]
        Returns the client's main webhook, if there is None it returns None
    environment: Optional[:class:`Environment`]
        Returns the client's main Environment, if there is None it returns None
    webhook_url_path: Optional[:class:`str`]
        Returns the webhook url path, if there is None it returns None


    .. versionadded:: 1.0.0
    """

    def __init__(
        self,
        bearer_token: Optional[str],
        *,
        consumer_key: Optional[str] = None,
        consumer_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        access_token_secret: Optional[str] = None,
        stream: Optional[Stream] = None,
        callback_url: Optional[str] = None,
        client_id: Optional[str] = None,
    ) -> None:
        self.http = HTTPClient(
            bearer_token,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            stream=stream,
            callback_url=callback_url,
            client_id=client_id,
        )
        self._account_user: Optional[User] = None  # set in account property.
        self.webhook: Optional[Webhook] = None
        self.environment: Optional[Environment] = None
        self.webhook_url_path: Optional[str] = None

    def __repr__(self) -> str:
        return "Client(bearer_token=SECRET consumer_key=SECRET consumer_secret=SECRET access_token=SECRET access_token_secret=SECRET)"

    @property
    def account(self) -> Optional[User]:
        """Optional[:class:`User`]: Returns the client's account information. The callback is a User object.

        .. versionadded:: 1.2.0
        """

        account_user = self._account_user
        if account_user is None:
            self._set_account_user()
            return self._account_user  # type: ignore
            # The account_user does not change when the function is called. That is why we are returning this.
        return account_user

    def _set_account_user(self) -> None:
        if not self.http.access_token:
            return None

        data = self.fetch_user(self.http.access_token.partition("-")[0])._User__original_payload
        self._account_user = ClientAccount(data, http_client=self.http)

    def event(self, func: Callable) -> None:
        """
        A decorator for making an event, the event will be register in the client's internal cache.

        See the :ref:`Event Reference <twitter-api-events>` for the currently documented events.

        Parameters
        ------------
        func: :class:`typing.Callable`
            The function that execute when the event is trigger. The event must be a synchronous function. You must also put the right event name in the function's name, See event reference for full events name.


        Raises
        --------
        TypeError
            The function passed is a coroutine function.


        .. versionadded:: 1.3.5
        """
        if iscoroutinefunction(func):
            raise TypeError("Function passed in event() must NOT be a coroutine function.")
        self.http.events[func.__name__[3:]] = func

    def fetch_user(self, user_id: Union[str, int]) -> Optional[User]:
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

    def fetch_tweet(self, tweet_id: Union[str, int]) -> Tweet:
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

    def fetch_direct_message(self, event_id: Union[str, int]) -> DirectMessage:
        """A method for fetching a direct message with the direct message's event ID.

        .. warning::
            This method uses API call and might cause ratelimit if used often! It is more recommended to use `get_message()` method, as it get the message from the client's internal cache.

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
        return self.http.fetch_direct_message(event_id)

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
    ) -> Optional[WelcomeMessage]:
        """Create a welcome message which you can set with :meth:`WelcomeMessage.set_rule()`.

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
        return self.http.create_welcome_message(name, text, file=file, quick_reply=quick_reply, cta=cta)

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
        return self.http.fetch_welcome_message(welcome_message_id)

    def fetch_welcome_message_rule(self, welcome_message_rule_id: Union[str, int]) -> WelcomeMessageRule:
        """A method for fetching a welcome message rule.

        Parameters
        ------------
        welcome_message_rule_id: Union[:class:`str`, :class:`int`]
            Represents the welcome message rule ID that you wish to fetch with.

        Returns
        ---------
        :class:`WelcomeMessageRule`
            This method returns :class:`WelcomeMessageRule` object.


        .. versionadded:: 1.3.5
        """
        return self.http.fetch_welcome_message_rule(welcome_message_rule_id)

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
        max_result: Optional[Union[str, int]] = None,
        *,
        lat: Optional[int] = None,
        long: Optional[int] = None,
        ip: Optional[Union[str, int]] = None,
        granularity: str = "neighborhood",
    ) -> Geo:  # TODO make enums for granularity
        """Search a geo with the given arguments.

        Parameters
        ------------
        query: :class:`str`
            Free-form text to match against while executing a geo-based query, best suited for finding nearby locations by name. Remember to URL encode the query.
        max_results: Optional[Union[:class:`str`, :class:`int`]]
            A hint as to the number of results to return. This does not guarantee that the number of results returned will equal max_results, but instead informs how many "nearby" results to return. Ideally, only pass in the number of places you intend to display to the user here.
        lat: :class:`int`
            The latitude to search around. This parameter will be ignored unless it is inside the range -90.0 to +90.0 (North is positive) inclusive. It will also be ignored if there isn't a corresponding long parameter.
        long: :class:`int`
            The longitude to search around. The valid ranges for longitude are -180.0 to +180.0 (East is positive) inclusive. This parameter will be ignored if outside that range, if it is not a number, if geo_enabled is turned off, or if there is not a corresponding lat parameter.
        ip: Union[:class:`str`, :class:`int`]
            An IP address. Used when attempting to fix geolocation based off of the user's IP address.
        granularity: :class:`str`
            This is the minimal granularity of place types to return and must be one of: neighborhood, city, admin or country. If no granularity is provided for the request neighborhood is assumed. Setting this to city, for example, will find places which have a type of city, admin or country.

        Returns
        ---------
        List[:class:`Geo`]
            This method return a list of :class:`Geo` objects.


        .. versionadded:: 1.5.3
        """
        return self.http.search_geo(query, max_result, lat=lat, long=long, ip=ip, granularity=granularity)

    def search_trend_with_place(self, woeid: Union[str, int], exclude: Optional[str] = None):
        """Search trends with woeid.

        .. note::
            You can find woeid information through :class:`Location` with :meth:`Client.search_trend_locations` or :meth:`Client.search_trend_closest`.

        Parameters
        ------------
        woeid: Union[:class:`str`, :class:`int`]
            "where on earth identifier" or WOEID, which is a legacy identifier created by Yahoo and has been deprecated. Twitter API v1.1 still uses the numeric value to identify town and country trend locations. Example WOEID locations include: Worldwide: 1 UK: 23424975 Brazil: 23424768 Germany: 23424829 Mexico: 23424900 Canada: 23424775 United States: 23424977 New York: 2459115.
        exclude: Optional[:class:`str`]
            Setting this equal to hashtags will remove all hashtags from the trends list.


        .. versionadded:: 1.5.0
        """
        res = self.http.request(
            "GET", "1.1", "/trends/place.json", params={"id": str(woeid), "exclude": exclude}, auth=True
        )

        return [Trend(**data) for data in res[0].get("trends")]

    def search_trend_locations(self):
        """Search locations that Twitter has trending topic information.


        .. versionadded:: 1.5.0
        """
        res = self.http.request("GET", "1.1", "/trends/available.json", auth=True)
        for data in res:
            data["parent_id"] = data["parentid"]
            data.pop("parentid")

        return [Location(**data) for data in res]

    def search_trend_closest(self, lat: int, long: int):
        """Search the rend closest to the lat and long.

        parameters
        ------------
        lat: :class:`int`
            If provided with a long parameter the available trend locations will be sorted by distance, nearest to furthest, to the co-ordinate pair. The valid ranges for longitude is -180.0 to +180.0 (West is negative, East is positive) inclusive.
        long: :class:`int`
            If provided with a lat parameter the available trend locations will be sorted by distance, nearest to furthest, to the co-ordinate pair. The valid ranges for longitude is -180.0 to +180.0 (West is negative, East is positive) inclusive.        -122.400612831116


        .. versionadded:: 1.5.0
        """
        res = self.http.request("GET", "1.1", "/trends/available.json", params={"lat": lat, "long": long}, auth=True)

        return [Location(**data) for data in res]

    def get_message(self, event_id: Union[str, int]) -> Optional[DirectMessage]:
        """Get a direct message through the client message cache. Returns None if the message is not in the cache.

        .. note::
            Note that you can only get the client and the subscriptions users's message.

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

    def get_tweet(self, tweet_id: Union[str, int]) -> Optional[Tweet]:
        """Gets a tweet through the client internal tweet cache. Return None if the tweet is not in the cache.

        .. note::
            Note that you can only get the client and the subscriptions users's tweet.

        Parameters
        ------------
        tweet_id: Union[:class:`str`, :class:`int`]
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

        return self.http.tweet_cache.get(tweet_id)

    def create_custom_profile(self, name: str, file: File) -> Optional[CustomProfile]:
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
        return self.http.create_custom_profile(name, file)

    def stream(self, *, dry_run: bool = False) -> None:
        """Stream realtime in twitter for tweets! This method use the stream argument in :meth:`request.get` for streaming in one of the stream endpoint that twitter api provides. If you want to use this method, make sure to provides the stream kwarg in your :class:`Client` instance and make an on_stream event to get the stream's tweet data and connection,
        example:

        .. code-block:: py

            import pytweet

            stream = pytweet.Stream()
            stream.add_rule("pytweet") #this make sure to only return tweets that has pytweet keyword in it.

            client = pytweet.Client(
                ...
                stream=stream
            )

            @client.event
            def on_stream(tweet, connection):
                ... #Do what you want with tweet and stream connection you got.

            client.stream()

        You can also add rules and specified which tweets must be retrieve via the tweet's characteristic features.

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

    def fetch_all_environments(self) -> Optional[List[Environment]]:
        """A method for fetching all the client's envirouments.

        Returns
        ---------
        Optional[List[:class:`Environment`]]
            Returns a list of :class:`Environment` objects.


        .. versionadded:: 1.5.0
        """
        res = self.http.request("GET", "1.1", "/account_activity/all/webhooks.json")

        return [Environment(data, client=self) for data in res.get("environments")]

    def listen(
        self,
        app: Flask,
        url: str,
        env_label: str,
        sleep_for: Union[int, float] = 0.50,
        ngrok: bool = False,
        **kwargs: Any,
    ):
        """Listen to upcoming account activity events send by twitter to your webhook url. You can use the rest of Flask arguments like port or host via the kwargs argument.

        Parameters
        ------------
        app: :class:`flask.Flask`
            Your flask application.
        url: :class:`str`
            The webhook url. This completely up to you, e.g https://your-domain.com/webhook/twitter etc.
        env_label: :class:`str`
            The environment's label.
        sleep_for: Union[:class:`int`, :class:`float`]
            Ensure the flask application is running before triggering a CRC by sleeping after starting a thread. Default to 0.50.
        ngrok: :class:`bool`
            indicates to use ngrok for tunneling your localhost. This usually uses for users that use localhost url.
        disabled_log: :class:`bool`
            A kwarg that indicates to disable flask's log so it does not print the request process in your terminal, this also will disable `werkzeug` log.
        make_new: :class:`bool`
            A kwarg indicates to make a new webhook url when the api cant find the url passed. Default to True.


        .. versionadded:: 1.5.0
        """
        disabled_log: bool = kwargs.pop("disabled_log", False)
        make_new: bool = kwargs.pop("make_new", True)
        environments = self.fetch_all_environments()

        if disabled_log:
            app.logger.disabled = True
            log = logging.getLogger("werkzeug")
            log.disabled = True

        for env in environments:
            if env.label == env_label:
                self.environment = env

            for webhook in env.webhooks:
                if url == webhook.url:
                    self.webhook_url_path = urlparse(webhook.url).path
                    self.webhook = webhook
                    self.environment = env
                    break

        try:
            thread = threading.Thread(target=app.run, name="PyTweet: Flask App Thread", kwargs=kwargs)

            if not self.webhook and not ngrok:
                self.webhook_url_path = urlparse(webhook.url).path

            elif self.webhook and ngrok:
                self.webhook_url_path = "THE URL PATH PASSSED BY NGROK"  # TODO add ngrok support

            @app.route(self.webhook_url_path, methods=["POST", "GET"])
            def webhook_receive():
                if request.method == "GET":
                    _log.info("Attempting to respond to a CRC.")
                    crc = request.args["crc_token"]

                    validation = hmac.new(
                        key=bytes(self.http.consumer_secret, "UTF-8"),
                        msg=bytes(crc, "UTF-8"),
                        digestmod=hashlib.sha256,
                    )
                    digested = base64.b64encode(validation.digest())

                    response = {"response_token": "sha256=" + format(str(digested)[2:-1])}

                    return json.dumps(response)

                json_data = request.get_json()
                self.http.handle_events(json_data)
                return ("", HTTPStatus.OK)

            check = not self.webhook and self.webhook_url_path
            if check and make_new:
                thread.start()
                time.sleep(sleep_for)
                webhook = self.environment.register_webhook(
                    url
                )  # Register a new webhook url if no webhook found also if make_new is True.
                self.webhook = webhook
                self.environment = env
                self.environment.add_my_subscription()
                ids = self.environment.fetch_all_subscriptions()
                users = self.http.fetch_users(ids)
                for user in users:
                    self.http.user_cache[user.id] = user

                _log.debug(
                    f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\n In Envinronment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
                )

            elif check and not make_new:
                raise PytweetException(
                    f"Cannot find url passed: {url} Invalid url passed, please check the spelling of your url"
                )

            else:
                thread.start()
                time.sleep(sleep_for)
                self.webhook.trigger_crc()
                ids = self.environment.fetch_all_subscriptions()
                users = self.http.fetch_users(ids)
                for user in users:
                    self.http.user_cache[user.id] = user

                _log.debug(
                    f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\nIn Envinronment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
                )
            thread.join()
        except Exception as e:
            _log.warn(f"An error was caught during listening: {e}")
            raise e

        finally:
            _log.debug(f"Stop listening due to internal/external problem!")
