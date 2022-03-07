from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import time
import threading
import datetime
from urllib.parse import urlparse
from asyncio import iscoroutinefunction
from http import HTTPStatus
from typing import Callable, List, Optional, Union, Any
from flask import Flask, request

from .paginations import MessagePagination
from .attachments import CTA, CustomProfile, File, Geo, Poll, QuickReply
from .enums import ReplySetting, SpaceState, Granularity
from .constants import TWEET_EXPANSION, USER_FIELD, MEDIA_FIELD, PLACE_FIELD, POLL_FIELD, TWEET_FIELD
from .errors import PytweetException, UnKnownSpaceState
from .http import HTTPClient
from .message import DirectMessage, WelcomeMessage, WelcomeMessageRule
from .space import Space
from .stream import Stream
from .tweet import Tweet
from .user import User, ClientAccount
from .environment import Environment, Webhook
from .dataclass import Location, Trend
from .list import List as TwitterList
from .type import ID

__all__ = ("Client",)

_log = logging.getLogger(__name__)


class Client:
    """Represents a twitter-api client for twitter api version 1.1 and 2 interface.

    Parameters
    ------------
    bearer_token: Optional[:class:`str`]
        The Bearer Token of the app. Uses for twitter version 2 endpoints.
    consumer_key: Optional[:class:`str`]
        The Consumer Key of the app. Users for twitter version 1.1 endpoints.
    consumer_secret: Optional[:class:`str`]
        The Consumer Key Secret of the app. Users for twitter version 1.1 endpoints.
    access_token: Optional[:class:`str`]
        The Access Token of the app. Users for twitter version 1.1 endpoints.
    access_token_secret: Optional[:class:`str`]
        The Access Token Secret of the app. Users for twitter version 1.1 endpoints.
    stream: Optional[Stream]
        The client's stream. Must be an instance of :class:`Stream`.
    callback_url: Optional[:class:`str`]
        The oauth callback url, default to None. Makes sure the callback url is the same as the one in your application auth-settings or else it can't create and interact with oauth related methods.
    client_id: Optional[:class:`str`]
        The client's OAuth 2.0 Client ID from keys and tokens page.
    client_secret: Optional[:class:`str`]
        The client's OAuth 2.0 Client Secret from keys and tokens page.
    use_bearer_only: bool
        Indicates to only use bearer token for all methods. This mean the client is now a twitter-api-client v2 interface. Some methods are unavailable to use such as fetching trends and location, environment fetching methods, and features such as events. Some methods can be recover with OAuth 2 authorization code flow with PKCE with the correct scopes or permissions. Like users.read scope for reading users info which some methods provide a way like :meth:`Client.fetch_user`.
    sleep_after_ratelimit: :class:`bool`
        Indicates to sleep when your client is ratelimited, If set to True it won't raise :class:`TooManyRequests` error but it would print a message indicating to sleep, then it sleeps for how many seconds it needs to sleep, after that it continue to restart the request.
    verify_credentials: :class:`bool`
        Indicates to verify the credentials you specified, this includes consumer_key, consumer_secret, access_token, access_token_secret. make sure to specified all of them in your client, you cannot specified only one of them.

    Attributes
    ------------
    webhook: Optional[:class:`Webhook`]
        Returns the client's main webhook, Returns None if not found.
    environment: Optional[:class:`Environment`]
        Returns the client's main Environment, Returns None if not found.
    webhook_url_path: Optional[:class:`str`]
        Returns the webhook url path, Returns None if not found.


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
        client_secret: Optional[str] = None,
        use_bearer_only: bool = False,
        sleep_after_ratelimit: bool = False,
        verify_credentials: bool = False,
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
            client_secret=client_secret,
            use_bearer_only=use_bearer_only,
            sleep_after_ratelimit=sleep_after_ratelimit,
        )
        self._account_user: Optional[User] = None  # set in account property.
        self.webhook: Optional[Webhook] = None
        self.environment: Optional[Environment] = None
        self.webhook_url_path: Optional[str] = None
        self.executor = self.http.thread_manager.create_new_executor(thread_name="main-executor")
        self.verify_credentials = verify_credentials
        if self.verify_credentials:
            self.http.oauth_session.verify_credentials(raise_error=True)

    def __repr__(self) -> str:
        return "Client({0.account!r})".format(self)

    def account(self, *, update: bool = False) -> Optional[ClientAccount]:
        """An alias to :meth:`Client.account`.

        Parameters
        ------------
        update: :class:`bool`
            Indicates to update the client's account information, setting update to True would make a request to the api and returns a new and updated data everytime. If sets to False, it will either make a request (if used the first time) or use the previous data stored in an instance variable.

        Returns
        ---------
        Optional[:class:`ClientAccount`]
            This method returns a :class:`ClientAccount` object.


        .. versionadded:: 1.2.0


        .. versionchanged:: 1.5.0


            Added an update argument and made as a function rather then a property.
        """
        account_user = self._account_user
        if account_user is None or update:
            self._set_account_user()
            return self._account_user  # type: ignore
            # The account_user does not change when the function is called. That is why we are returning this.
        return account_user

    def me(self, *, update: bool = False) -> Optional[ClientAccount]:
        """An alias to :meth:`Client.account`.

        Parameters
        ------------
        update: :class:`bool`
            Indicates to update the client's account information, setting update to True would make a request to the api and returns a new and updated data everytime. If sets to False, it will either make a request (if used the first time) or use the previous data stored in an instance variable.

        Returns
        ---------
        Optional[:class:`ClientAccount`]
            This method returns a :class:`ClientAccount` object.


        .. versionadded:: 1.2.0


        .. versionchanged:: 1.5.0


            Added an update argument and made as a function rather then a property.
        """
        return self.account(update=update)

    def _set_account_user(self) -> None:
        if not self.http.access_token:
            return None

        data = self.http.fetch_me()._User__original_payload
        self._account_user = ClientAccount(data, http_client=self.http)

    def event(self, func: Callable) -> None:
        """A decorator for making an event, the event will be register in the client's internal cache.

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

    def fetch_user(self, user_id: ID) -> Optional[User]:
        """Fetches a twitter user.

        .. warning::
            This method uses API call and might cause ratelimits if used often! There is always an alternative like :meth:`Client.get_user` from the client's internal cache.

        Parameters
        ------------
        user_id: :class:`ID`
            Represents the user ID that you wish to get info for. If you don't have it you may use `fetch_user_by_username` because it only requires the user's username.

        Returns
        ---------
        :class:`User`
            This method returns a :class:`User` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_user(user_id)

    def fetch_user_by_username(self, username: str) -> Optional[User]:
        """Fetches a twitter user by the user's username.

        .. warning::
            This method uses API call and might cause ratelimits if used often! There is always an alternative like :meth:`Client.get_user` from the client's internal cache.

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
        return self.http.fetch_user_by_username(username)

    def fetch_tweet(self, tweet_id: ID) -> Tweet:
        """Fetches a tweet.

        .. warning::
            This method uses API call and might cause ratelimits if used often! There is always an alternative like :meth:`Client.get_tweet` from the client's internal cache.

        Parameters
        ------------
        tweet_id: :class:`ID`
            Represents the tweet id that you wish to get info about.

        Returns
        ---------
        :class:`Tweet`
            This method returns a :class:`Tweet` object.


        .. versionadded:: 1.0.0
        """
        return self.http.fetch_tweet(tweet_id)

    def fetch_direct_message(self, event_id: ID) -> DirectMessage:
        """Fetches a direct message.

        .. warning::
            This method uses API call and might cause ratelimits if used often! There is always an alternative like :meth:`Client.fetch_direct_message` from the client's internal cache.

        Parameters
        ------------
        event_id: :class:`ID`
            Represents the event's ID that you wish to fetch with.

        Returns
        ---------
        :class:`DirectMessage`
            This method returns a :class:`DirectMessage` object.


        .. versionadded:: 1.2.0
        """
        return self.http.fetch_direct_message(event_id)

    def fetch_welcome_message(self, welcome_message_id: ID) -> WelcomeMessage:
        """Fetches a welcome message.

        Parameters
        ------------
        welcome_message_id: :class:`ID`
            Represents the welcome message ID that you wish to fetch with.

        Returns
        ---------
        :class:`WelcomeMessage`
            This method returns :class:`WelcomeMessage` object.


        .. versionadded:: 1.3.5
        """
        return self.http.fetch_welcome_message(welcome_message_id)

    def fetch_welcome_message_rule(self, welcome_message_rule_id: ID) -> WelcomeMessageRule:
        """Fetches a welcome message rule.

        Parameters
        ------------
        welcome_message_rule_id: :class:`ID`
            Represents the welcome message rule ID that you wish to fetch with.

        Returns
        ---------
        :class:`WelcomeMessageRule`
            This method returns :class:`WelcomeMessageRule` object.


        .. versionadded:: 1.3.5
        """
        return self.http.fetch_welcome_message_rule(welcome_message_rule_id)

    def fetch_space(self, space_id: ID, *, space_host: bool = False) -> Space:
        """Fetches a space.

        Parameters
        ------------
        space_id: :class:`ID`
            Represents the space ID that you wish to fetch with.
        space_host: :class:`bool`
            Indicates if the client is the host of the requested space. This is very useful to returns a :class:`Space` object with the 'subscriber_count' data, if sets to False the 'subscriber_count' will returns None. Default to False.

        Returns
        ---------
        :class:`Space`
            This method returns a :class:`Space` object.


        .. versionadded:: 1.3.5


        .. versionchanged:: 1.5.0

            Added `space_host` argument.
        """
        return self.http.fetch_space(space_id, space_host=space_host)

    def fetch_spaces_by_title(
        self, title: str, state: SpaceState = SpaceState.live, *, space_host: bool = False
    ) -> Optional[List[Space]]:
        """Fetches spaces using its title.

        Parameters
        ------------
        title: :class:`ID`
            The space title that you are going use for fetching the space.
        state: :class:`SpaceState`
            The type of state the space has. There are only 2 types: SpaceState.live indicates that the space is live and SpaceState.scheduled indicates the space is not live and scheduled by the host. Default to SpaceState.live,
        space_host: :class:`bool`
            Indicates if the client is the host of the requested space. This is very useful to returns a space with the 'subscriber_count' data, if sets to False the 'subscriber_count' will returns None. Default to False.

        Returns
        ---------
        Optional[List[:class:`Space`]]
            This method returns a list of :class:`Space` objects.


        .. versionadded:: 1.3.5

        .. versionchanged:: 1.5.0

            Added `space_host` argument and returns a list of spaces.
        """
        if state == SpaceState.live or state == SpaceState.scheduled:
            return self.http.fetch_spaces_bytitle(title, state, space_host=space_host)
        else:
            raise UnKnownSpaceState(given_state=state)

    def fetch_list(self, id: ID) -> TwitterList:
        """Fetches a list using its id

        Returns
        ---------
        :class:`List`
            This method returns a :class:`List` object.


        .. versionadded:: 1.5.0
        """
        return self.http.fetch_list(id)

    def fetch_all_environments(self) -> Optional[List[Environment]]:
        """Fetches all the client's environments.

        Returns
        ---------
        Optional[List[:class:`Environment`]]
            Returns a list of :class:`Environment` objects.


        .. versionadded:: 1.5.0
        """
        res = self.http.request("GET", "1.1", "/account_activity/all/webhooks.json")

        return [Environment(data, client=self) for data in res.get("environments")]

    def fetch_message_history(self) -> Optional[MessagePagination]:
        """Returns all Direct Messages (both sent and received) within the last 30 days. Sorted in chronological order.

        Returns
        ---------
        Optional[:class:`MessagePagination`]
            This method returns a :class:`MessagePagination` object.


        .. versionadded:: 1.5.0
        """
        params = {"count": 50}

        res = self.http.request("GET", "1.1", "/direct_messages/events/list.json", auth=True, params=params)

        if not res or not res.get("events"):
            return []

        res = self.http.payload_parser.parse_message_to_pagination_data(res)
        return MessagePagination(
            res, endpoint_request=f"/direct_messages/events/list.jsons", http_client=self.http, params=params
        )

    def tweet(
        self,
        text: str = None,
        *,
        file: Optional[File] = None,
        files: Optional[List[File]] = None,
        poll: Optional[Poll] = None,
        geo: Optional[Union[Geo, str]] = None,
        direct_message_deep_link: Optional[str] = None,
        reply_setting: Optional[Union[ReplySetting, str]] = None,
        quote_tweet: Optional[Union[Tweet, ID]] = None,
        reply_tweet: Optional[Union[Tweet, ID]] = None,
        exclude_reply_users: Optional[List[User, ID]] = None,
        media_tagged_users: Optional[List[User, ID]] = None,
        super_followers_only: bool = False,
    ) -> Optional[Tweet]:
        """Posts a tweet directly to twitter from the given parameters.

        Parameters
        ------------
        text: :class:`str`
            The tweet's text, it will show up as the main text in a tweet.
        file: Optional[:class:`File`]
            Represents a single file attachment. It could be an image, gif, or video. Must be an instance of pytweet.File
        files: Optional[List[:class:`File`]]
            Represents multiple file attachments in a list. It could be an image, gif, or video. the item in the list must also be an instance of pytweet.File
        poll: Optional[:class:`Poll`]
            The poll attachment.
        geo: Optional[Union[:class:`Geo`, :class:`str`]]
            The geo attachment, you can put an object that is an instance of :class:`Geo` or the place ID in a string.
        direct_message_deep_link: Optional[:class:`str`]
            The direct message deep link, It will showup as a CTA(call-to-action) with button attachment.
        reply_setting: Optional[Union[:class:`ReplySetting`, :class:`str`]]
            The reply setting that you can set to minimize users that can reply. If None is specified, the default is set to 'everyone' can reply.
        quote_tweet: Optional[:class:`ID`]
            The tweet or tweet ID you want to quote.
        reply_tweet: Optional[:class:`Tweet`, :class:`ID`]
            The tweet or tweet ID you want to reply. If you have an instance of :class:`Tweet`, you can use the :meth:`Tweet.reply` method rather then using this method.
        exclude_reply_users: Optional[List[:class:`User`, :class:`ID`]]
            A list of users or user ids to be excluded from the reply :class:`Tweet` thus removing a user from a thread, if you dont want to mention a reply with 3 mentions, You can use this argument and provide the user id you don't want to mention.
        media_tagged_users: Optional[List[:class:`User`, :class:`ID`]]
            A list of users or user ids being tagged in the Tweet with Media. If the user you're tagging doesn't have photo-tagging enabled, their names won't show up in the list of tagged users even though the Tweet is successfully created.
        super_followers_only: :class:`bool`
            Allows you to tweet exclusively for super followers.

        Returns
        ---------
        :class:`Tweet`
            This method returns a :class:`Tweet` object.


        .. versionadded:: 1.1.0


        .. versionchaned:: 1.5.0

            Added `files` and `media_tagged_users` arguments.
        """
        return self.http.post_tweet(
            text,
            file=file,
            files=files,
            poll=poll,
            geo=geo,
            quote_tweet=quote_tweet,
            direct_message_deep_link=direct_message_deep_link,
            reply_setting=reply_setting,
            reply_tweet=reply_tweet,
            exclude_reply_users=exclude_reply_users,
            media_tagged_users=media_tagged_users,
            super_followers_only=super_followers_only,
        )

    def create_welcome_message(
        self,
        *,
        name: Optional[str] = None,
        text: Optional[str] = None,
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
            Represents a single file attachment. It could be an image, gif, or video. It also have to be an instance of pytweet.File
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
        return self.http.create_welcome_message(name=name, text=text, file=file, quick_reply=quick_reply, cta=cta)

    def create_list(self, name: str, *, description: str = "", private: bool = False) -> Optional[TwitterList]:
        """Create a new list.

        Parameters
        ------------
        name: :class:`str`
            The name of the List you wish to create.
        description: :class:`str`
            Description of the List.
        private: :class:`bool`
            Determine whether the List should be private, default to False.

        Returns
        ---------
        Optional[:class:`List`]
            This method returns a :class:`List` object.


        .. versionadded:: 1.5.0
        """
        twitter_list = self.http.create_list(name, description=description, private=private)
        return self.http.fetch_list(twitter_list.id)

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

    def search_geos(
        self,
        query: str,
        max_result: Optional[ID] = None,
        *,
        lat: Optional[int] = None,
        long: Optional[int] = None,
        ip: Optional[ID] = None,
        granularity: Granularity = Granularity.neighborhood,
    ) -> Geo:
        """Search geo-locations with the given arguments.

        Parameters
        ------------
        query: :class:`str`
            Free-form text to match against while executing a geo-based query, best suited for finding nearby locations by name. Remember to URL encode the query.
        max_results: Optional[:class:`ID`]
            A hint as to the number of results to return. This does not guarantee that the number of results returned will equal max_results, but instead informs how many "nearby" results to return. Ideally, only pass in the number of places you intend to display to the user here.
        lat: :class:`int`
            The latitude to search around. This parameter will be ignored unless it is inside the range -90.0 to +90.0 (North is positive) inclusive. It will also be ignored if there isn't a corresponding long parameter.
        long: :class:`int`
            The longitude to search around. The valid ranges for longitude are -180.0 to +180.0 (East is positive) inclusive. This parameter will be ignored if outside that range, if it is not a number, if geo_enabled is turned off, or if there is not a corresponding lat parameter.
        ip: :class:`ID`
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

    def search_trend_with_place(self, woeid: ID, exclude: Optional[str] = None) -> Optional[List[Trend]]:
        """Search trends with woeid.

        .. note::
            You can find woeid information through :meth:`Location.woeid` with :meth:`Client.search_trend_locations` or :meth:`Client.search_trend_closest`.

        Parameters
        ------------
        woeid: :class:`ID`
            "where on earth identifier" or WOEID, which is a legacy identifier created by Yahoo and has been deprecated. Twitter API v1.1 still uses the numeric value to identify town and country trend locations. Example WOEID locations include: Worldwide: 1 UK: 23424975 Brazil: 23424768 Germany: 23424829 Mexico: 23424900 Canada: 23424775 United States: 23424977 New York: 2459115.
        exclude: Optional[:class:`str`]
            Setting this equal to hashtags will remove all hashtags from the trends list.

        Returns
        ---------
        Optional[List[:class:`Trend`]]
            This method returns a list of :class:`Trend` objects.


        .. versionadded:: 1.5.0
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/trends/place.json",
            params={"id": str(woeid), "exclude": exclude},
            auth=True,
        )

        return [Trend(**data) for data in res[0].get("trends")]

    def search_trend_locations(self) -> Optional[List[Location]]:
        """Search locations that Twitter has trending topic information.

        Returns
        ---------
        Optional[List[:class:`Location`]]
            This method returns a list of :class:`Location` objects.


        .. versionadded:: 1.5.0
        """
        res = self.http.request("GET", "1.1", "/trends/available.json", auth=True)
        for index, data in enumerate(res):
            res[index] = self.http.payload_parser.parse_trend_location_payload(data)

        return [Location(**data) for data in res]

    def search_trend_closest(self, lat: int, long: int) -> Optional[List[Location]]:
        """Search the rend closest to the lat and long.

        parameters
        ------------
        lat: :class:`int`
            If provided with a long parameter the available trend locations will be sorted by distance, nearest to furthest, to the coordinate pair. The valid ranges for longitude is -180.0 to +180.0 (West is negative, East is positive) inclusive.
        long: :class:`int`
            If provided with a lat parameter the available trend locations will be sorted by distance, nearest to furthest, to the coordinate pair. The valid ranges for longitude is -180.0 to +180.0 (West is negative, East is positive) inclusive -122.400612831116

        Returns
        ---------
        Optional[List[:class:`Location`]]
            This method returns a list of :class:`Location` objects.


        .. versionadded:: 1.5.0
        """
        res = self.http.request(
            "GET",
            "1.1",
            "/trends/available.json",
            params={"lat": lat, "long": long},
            auth=True,
        )

        return [Location(**data) for data in res]

    def search_recent_tweet(
        self,
        query: str,
        *,
        max_results: int = 10,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        since_id: Optional[ID] = None,
        until_id: Optional[ID] = None,
        sort_by_relevancy: bool = False,
    ) -> List[Tweet]:
        """Searches tweet from the last seven days that match a search query.

        Parameters
        ------------
        query: :class:`str`
            One query for matching Tweets.
        max_results: :class:`int`
            The maximum number of search results to be returned by a request. A number between 10 and 100. By default, the method will returns 10 results.
        start_time: Optional[:class:`datetime.datetime`]
            This will make sure the tweets created datetime is after that specific time.
        end_time: Optional[:class:`datetime.datetime`]
            This will make sure the tweets created datetime is before that specific time.
        since_id: Optional[`ID`]
            Returns results with a Tweet ID greater than (that is, more recent than) the specified 'since' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the since_id. If the limit of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.
        until_id: Optional[`ID`]
            Returns results with a Tweet ID less less than (that is, older than) the specified 'until' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the until_id. If the limit of Tweets has occurred since the until_id, the until_id will be forced to the most recent ID available.
        sort_by_relevancy: :class:`bool`
            This parameter is used to specify the order in which you want the Tweets returned. If sets to True, tweets will be order by relevancy, else it sets to recency. Default to False.

        Returns
        ---------
        Union[:class:`TweetPagination`, :class:`list`]
            This method returns a list of :class:`Tweet` objects.


        .. versionadded:: 1.5.0
        """
        if (
            not isinstance(start_time, datetime.datetime)
            and start_time
            or not isinstance(end_time, datetime.datetime)
            and end_time
        ):
            raise ValueError("start_time or end_time must be a datetime object!")

        params = {
            "expansions": TWEET_EXPANSION,
            "user.fields": USER_FIELD,
            "media.fields": MEDIA_FIELD,
            "place.fields": PLACE_FIELD,
            "poll.fields": POLL_FIELD,
            "tweet.fields": TWEET_FIELD,
            "query": query,
            "max_results": max_results,
        }

        if start_time:
            params["start_time"] = start_time.isoformat()
        if end_time:
            params["end_time"] = end_time.isoformat()
        if since_id:
            params["since_id"] = str(since_id)
        if until_id:
            params["until_id"] = str(until_id)
        if sort_by_relevancy:
            params["sort_order"] = "relevancy"

        res = self.http.request("GET", "2", "/tweets/search/recent", params=params)

        return [Tweet(data, http_client=self.http) for data in res.get("data")]

    def search_all_tweet(
        self,
        query: str,
        *,
        max_results: int = 10,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        since_id: Optional[ID] = None,
        until_id: Optional[ID] = None,
        sort_by_relevancy: bool = False,
    ) -> List[Tweet]:
        """Searches all tweet from the complete history of public Tweets matching a search query; since the first Tweet was created March 26, 2006. Only available to those users who have been approved for Academic Research access.

        Parameters
        ------------
        query: :class:`str`
            One query for matching Tweets.
        max_results: :class:`int`
            The maximum number of search results to be returned by a request. A number between 10 and 100. By default, the method will returns 10 results.
        start_time: Optional[:class:`datetime.datetime`]
            This will make sure the tweets created datetime is after that specific time.
        end_time: Optional[:class:`datetime.datetime`]
            This will make sure the tweets created datetime is before that specific time.
        since_id: Optional[`ID`]
            Returns results with a Tweet ID greater than (that is, more recent than) the specified 'since' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the since_id. If the limit of Tweets has occurred since the since_id, the since_id will be forced to the oldest ID available.
        until_id: Optional[`ID`]
            Returns results with a Tweet ID less less than (that is, older than) the specified 'until' Tweet ID. Only the 3200 most recent Tweets are available. The result will exclude the until_id. If the limit of Tweets has occurred since the until_id, the until_id will be forced to the most recent ID available.
        sort_by_relevancy: :class:`bool`
            This parameter is used to specify the order in which you want the Tweets returned. If sets to True, tweets will be order by relevancy, else it sets to recency. Default to False.

        Returns
        ---------
        Union[:class:`TweetPagination`, :class:`list`]
            This method returns a list of :class:`Tweet` objects.


        .. versionadded:: 1.5.0
        """
        if (
            not isinstance(start_time, datetime.datetime)
            and start_time
            or not isinstance(end_time, datetime.datetime)
            and end_time
        ):
            raise ValueError("start_time or end_time must be a datetime object!")

        params = {
            "expansions": TWEET_EXPANSION,
            "user.fields": USER_FIELD,
            "media.fields": MEDIA_FIELD,
            "place.fields": PLACE_FIELD,
            "poll.fields": POLL_FIELD,
            "tweet.fields": TWEET_FIELD,
            "query": query,
            "max_results": max_results,
        }

        if start_time:
            params["start_time"] = start_time.isoformat()
        if end_time:
            params["end_time"] = end_time.isoformat()
        if since_id:
            params["since_id"] = str(since_id)
        if until_id:
            params["until_id"] = str(until_id)
        if sort_by_relevancy:
            params["sort_order"] = "relevancy"

        res = self.http.request("GET", "2", "/tweets/search/all", params=params)

        return [Tweet(data, http_client=self.http) for data in res.get("data")]

    def get_user(self, user_id: ID) -> Optional[User]:
        """Gets a user through the client internal user cache. Return None if the user is not in the cache.

        .. note::
            Users will get cache with several conditions:
                * Users return from a method such as :meth:`Client.fetch_user`.
                * The client interacts with other users such as sending a message to another user through :meth:`User.send` and many more
                * The subscription users interact with other users such as sending message from the subscription user to another user (This condition only applies if you use :meth:`Client.listen` at the very end of the file)

        Parameters
        ------------
        user_id: :class:`ID`
            The ID of a user that you want to get.

        Raises
        --------
        ValueError:
            Raised when the user_id argument is not an integer or a string of digits.

        Returns
        ---------
        :class:`User`
            This method returns a :class:`User` object or None if the user was not found.


        .. versionadded:: 1.5.0
        """
        try:
            user_id = int(user_id)
        except ValueError:
            raise ValueError("user_id must be an integer or a string of digits.")

        return self.http.user_cache.get(user_id)

    def get_tweet(self, tweet_id: ID) -> Optional[Tweet]:
        """Gets a tweet through the client internal tweet cache. Return None if the tweet is not in the cache.

        .. note::
            Tweets will get cache with several conditions:
                * Tweets send by the client.
                * Tweets send by the subscription users (This condition only applies if you use :meth:`Client.listen` at the very end of the file).
                * Tweets return from a method such as: :meth:`Client.fetch_tweet`

        Parameters
        ------------
        tweet_id: :class:`ID`
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

    def get_direct_message(self, event_id: ID) -> Optional[DirectMessage]:
        """Get a direct message through the client message cache. Returns None if the message is not in the cache.

        .. note::
            Messages will get cache with several conditions:
                * Messages send by the client.
                * Messages return from a method such as: :meth:`Client.fetch_direct_message`
                * The subscription users interact with other users such as sending message from the subscription user to another user (This condition only applies if you use :meth:`Client.listen` at the very end of the file).

        Parameters
        ------------
        event_id: :class:`ID`
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

    def listen(
        self,
        app: Flask,
        *,
        url: str,
        env_label: str,
        sleep_for: Union[int, float] = 0.50,
        ngrok: bool = False,
        **kwargs: Any,
    ):
        """Listen to upcoming account activity events send by twitter to your flask's url. You can use the rest of Flask arguments like port or host via the kwargs argument.

        .. note::
            For the time being, we only support Flask for the app argument! If you want to use your own web application url, consider using :meth:`Client.listen_to`.

        Parameters
        ------------
        app: :class:`flask.Flask`
            Your flask application.
        url: :class:`str`
            a kwarg that the webhook url aka your flask's web application url. This completely up to you, e.g https://your-website.domain/webhook/twitter.
        env_label: :class:`str`
            a kwarg that the environment's label.
        sleep_for: Union[:class:`int`, :class:`float`]
            a kwarg that ensure the flask application is running before triggering a CRC by sleeping after starting a thread. Default to 0.50.
        ngrok: :class:`bool`
            a kwarg that indicates to use ngrok for tunneling your localhost. This usually uses for users that use localhost url.
        disabled_log: :class:`bool`
            A kwarg that indicates to disable flask's log so it does not print the request process in your terminal, this also will disable `werkzeug` log.
        make_new: :class:`bool`
            A kwarg indicates to make a new webhook url when the api can't find the url passed. Default to True.


        .. versionadded:: 1.5.0
        """
        if not isinstance(app, Flask):
            raise PytweetException("App argument must be an instance of flask.Flask!")

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
            thread = threading.Thread(
                target=app.run,
                name="client-listen-method:thread_session=LISTEN-SESSION",
                kwargs=kwargs,
            )

            if not self.webhook and not ngrok:
                self.webhook_url_path = urlparse(url).path

            elif self.webhook and ngrok:
                ...  # TODO add ngrok support

            @app.route(self.webhook_url_path, methods=["POST", "GET"])
            def webhook_receive():
                if request.method == "GET":
                    _log.info("Attempting to respond a CRC.")
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
                _log.debug(f"An event triggered! {json_data}")
                self.executor.submit(self.http.handle_events, payload=json_data)
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
                    f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\n In Environment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
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
                    f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\n In Environment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
                )
            thread.join()
        except Exception as e:
            _log.warn(f"An error was caught during listening: {e}")
            raise e

        finally:
            _log.debug(f"Stop listening due to internal/external problem!")

    def listen_to(self, url: str, *, env_label: str, ngrok: bool = False, make_new: bool = True):
        """Listen to upcoming account activity events send by twitter to a web application url. This method differ from :meth:`Client.listen`, this method doesn't use the flask's web application url, rather your web application url. This is good for people that want to implement their web application outside flask.

        .. warning::
            With this method, you have to make your own CRC and event handlers in your web application. For the time being, the documentation doesn't provides information for the handlers, either go to twitter documentation about account activity api or wait until we write the documentation.

        Parameters
        ------------
        url: :class:`str`
            The webhook url. This completely up to you, e.g https://your-website.domain/webhook/twitter.
        env_label: :class:`str`
            The environment's label.
        ngrok: :class:`bool`
            indicates to use ngrok for tunneling your localhost. This usually uses for users that use localhost url.
        make_new: :class:`bool`
            A kwarg indicates to make a new webhook url when the api can't find the url passed. Default to True.


        .. versionadded:: 1.5.0
        """
        environments = self.fetch_all_environments()

        for env in environments:
            if env.label == env_label:
                self.environment = env

            for webhook in env.webhooks:
                if url == webhook.url:
                    self.webhook_url_path = urlparse(webhook.url).path
                    self.webhook = webhook
                    self.environment = env
                    break

        if not self.webhook and not ngrok:
            self.webhook_url_path = urlparse(webhook.url).path

        elif self.webhook and ngrok:
            ...  # TODO add ngrok support

        check = not self.webhook and self.webhook_url_path
        if check and make_new:
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
                f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\n In Environment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
            )

        elif check and not make_new:
            raise PytweetException(
                f"Cannot find url passed: {url} Invalid url passed, please check the spelling of your url"
            )

        else:
            self.webhook.trigger_crc()
            ids = self.environment.fetch_all_subscriptions()
            users = self.http.fetch_users(ids)
            for user in users:
                self.http.user_cache[user.id] = user

            _log.debug(
                f"Listening for events! user cache filled at {len(self.http.user_cache)} users! flask application is running with url: {url}({self.webhook_url_path}).\n Ngrok: {ngrok}\nMake a new webhook when not found: {make_new}\n In Environment: {repr(self.environment)} with webhook: {repr(self.webhook)}."
            )
