from __future__ import annotations

import requests
import json
import logging
import time
from typing import Optional, Type, Union, Any, List, TYPE_CHECKING
from dataclasses import dataclass
from .tweet import Tweet
from .errors import PytweetException, ConnectionException
from .expansions import (
    TWEET_FIELD,
    MEDIA_FIELD,
    PLACE_FIELD,
    POLL_FIELD,
    USER_FIELD,
    TWEET_EXPANSION,
)

if TYPE_CHECKING:
    from .http import HTTPClient

_log = logging.getLogger(__name__)


def _check_for_errors(data, session):
    if "errors" in data.keys():
        raise ConnectionException(session, None)


@dataclass
class StreamRule:
    """Represent a stream rule.

    .. versionadded:: 1.3.5
    """

    value: str
    tag: Optional[str] = None
    id: Optional[Union[str, int]] = None


class StreamConnection:
    """Represent the twitter api stream connection. This will handle the stream connection.


    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        url: str,
        backfill_minutes: int = 0,
        reconnect_attempts: int = 0,
        http_client: Optional[HTTPClient] = None,
    ):
        self.url = url
        self.backfill_minutes: int = backfill_minutes
        self.reconnect_attempts: int = reconnect_attempts
        self.http_client: Optional[HTTPClient] = http_client
        self.session: Optional[Any] = None
        self.errors = 0

    @property
    def closed(self) -> Optional[bool]:
        """ "Optional[:class:`bool`]: Returns True if the connection is closed, else False.

        .. versionadded:: 1.3.5
        """
        return self.session is None

    def is_close(self) -> Optional[bool]:
        """ "An alias to :class:`StreamConnection.closed`.

        Returns
        ---------
        Optional[:class:`bool`]:
            This method returns a :class:`bool` object.

        .. versionadded:: 1.3.5
        """
        return self.closed

    def close(self) -> None:
        """ "Close the stream connection.

        Returns
        ---------
        :class:`NoneType`:
            This method returns None.


        .. versionadded:: 1.3.5
        """
        if self.is_close():
            raise PytweetException("Attempt to close a stream that's already closed!")

        _log.info("Closing connection!")
        self.session.close()
        self.session = None

    def connect(self) -> Optional[Any]:
        """ "Connect to the current stream connection.

        .. versionadded:: 1.3.5
        """
        while True:
            try:
                response = requests.get(
                    self.url,
                    headers={"Authorization": f"Bearer {self.http_client.bearer_token}"},
                    params={
                        "backfill_minutes": int(self.backfill_minutes),
                        "expansions": TWEET_EXPANSION,
                        "media.fields": MEDIA_FIELD,
                        "place.fields": PLACE_FIELD,
                        "poll.fields": POLL_FIELD,
                        "tweet.fields": TWEET_FIELD,
                        "user.fields": USER_FIELD,
                    },
                    stream=True,
                )
                _log.info("Client connected to stream!")
                self.http_client.dispatch("stream_connect", self)
                self.session = response

                for response_line in response.iter_lines():
                    if response_line:
                        json_data = json.loads(response_line.decode("UTF-8"))
                        _check_for_errors(json_data, self.session)
                        tweet = Tweet(json_data, http_client=self.http_client)
                        self.http_client.tweet_cache[tweet.id] = tweet
                        self.http_client.dispatch("stream", tweet, self)

            except Exception as e:
                if isinstance(e, AttributeError):
                    break

                elif isinstance(e, requests.exceptions.RequestException):
                    self.errors += 1
                    if self.errors > self.reconnect_attempts:
                        _log.error("Too many errors caught during streaming, closing stream!")
                        self.close()
                        self.http_client.dispatch("stream_disconnect", self)
                        break

                    _log.warning(f"An error caught during streaming session: {e}")
                    _log.info(f"Reconnecting to stream after sleeping for 5.0 seconds")
                    time.sleep(5.0)

                else:
                    raise e

        _log.info("Streaming connection has been closed!")


class Stream:
    """Represent a stream object that stream over twitter for tweets.

    Parameters
    ------------
    backfill_minutes: :class:`int`
        This feature will deliver duplicate Tweets, meaning that if you were disconnected for 90 seconds, and you requested two minutes of backfill, you will receive 30 seconds worth of duplicate Tweets. Due to this, you should make sure your system is tolerant of duplicate data. This feature is currently only available to the Academic Research product track.
    reconnect_attempts: :class:`int`
        Decide how many attempts for a reconnect to perform, if the client reconnected more then this argument, it would break the loop.


    .. versionadded:: 1.3.5
    """

    def __init__(self, backfill_minutes: int = 0, reconnect_attempts: int = 15):
        self.backfill_minutes = backfill_minutes
        self.raw_rules: Optional[list] = []
        self.http_client: Optional[HTTPClient] = None
        self.reconnect_attempts = reconnect_attempts
        self.sample = False
        self.connection: StreamConnection = StreamConnection(
            "https://api.twitter.com/2/tweets/search/stream",
            self.backfill_minutes,
            reconnect_attempts,
            self.http_client,
        )

    @classmethod
    def sample_stream(cls: Type[Stream], backfill_minutes: int = 0, reconnect_attempts: int = 15) -> Stream:
        """A class method that change the stream connection to a sample one, this would mean you dont have to set any stream rules. This would not recommended because it can make the progress of tweet cap much faster, if its out of limit you would not be able to stream.

        Parameters
        ------------
        backfill_minutes: :class:`int`
            This feature will deliver duplicate Tweets, meaning that if you were disconnected for 90 seconds, and you requested two minutes of backfill, you will receive 30 seconds worth of duplicate Tweets. Due to this, you should make sure your system is tolerant of duplicate data. This feature is currently only available to the Academic Research product track.
        reconnect_attempts: :class:`int`
            Decide how many attempts for a reconnect to perform, if the client reconnected more then this argument, it would break the loop.

        Returns
        ---------
        :class:`Stream`
            This classmethod returns your :class:`Stream` instance.


        .. versionadded:: 1.3.5
        """
        self = cls(backfill_minutes, reconnect_attempts)
        self.http_client = None
        self.sample = True
        self.connection = StreamConnection(
            "https://api.twitter.com/2/tweets/sample/stream",
            self.backfill_minutes,
            self.reconnect_attempts,
            self.http_client,
        )
        return self

    @property
    def rules(self) -> Optional[dict]:
        """:class:`dict`: Returns the stream's rules, if its a sample stream it would returns None.

        .. versionadded:: 1.3.5
        """
        if self.sample:
            return None

        return [StreamRule(**data) for data in self.raw_rules]

    def add_rule(self, value: str, tag: Optional[str] = None) -> Optional[Stream]:
        """Add a rule to your stream to match with tweets that the stream return. You can use an operator to do this, check https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query for more information about the operator.

        Parameters
        ------------
        value: :class:`str`
            The rule text. If you are using a Standard Project at the Basic access level, you can use the basic set of operators, can submit up to 25 concurrent rules, and can submit rules up to 512 characters long. If you are using an Academic Research Project at the Basic access level, you can use all available operators, can submit up to 1,000 concurrent rules, and can submit rules up to 1,024 characters long.
        tag: Optional[:class:`str`]
            The tag label. This is a free-form text you can use to identify the rules that matched a specific Tweet in the streaming response. Tags can be the same across rules.

        Returns
        ---------
        :class:`Stream`:
            Returns the stream's rules, if its a sample stream it would returns None.


        .. versionadded:: 1.3.5
        """
        if self.sample:
            return None

        data = {"value": value}
        if tag:
            data["tag"] = tag
        self.raw_rules.append(data)
        return self

    def clear(self) -> None:
        """Clear stream before attempting to connect with the stream connection, this would delete all previous rules in your stream.

        Returns
        ---------
        :class:`NoneType`:
            This method returns None.


        .. versionadded:: 1.3.5
        """
        if self.sample:
            return None

        rules = self.http_client.request(
            "GET",
            "2",
            "/tweets/search/stream/rules",
        )
        if not rules:
            return

        if rules.get("data"):
            data = {"delete": {"ids": [str(rule.get("id")) for rule in rules.get("data")]}}
            rules = self.http_client.request("POST", "2", "/tweets/search/stream/rules", json=data)

    def fetch_rules(self) -> Optional[List[StreamRule]]:
        """Fetch the stream's rules.

        Returns
        ---------
        Optional[List[:class:`StreamRule`]]
            This method returns a :class:`list` of :class:`StreamRule` objects.


        .. versionadded:: 1.3.5
        """
        if self.sample:
            return None

        res = self.http_client.request(
            "GET",
            "2",
            "/tweets/search/stream/rules",
        )

        try:
            return [StreamRule(**data) for data in res["data"]]
        except TypeError:
            return res

    def set_rules(self, dry_run: bool) -> None:
        """Create and set rules to your stream.

        Parameters
        ------------
        dry_run: :class:`bool`
            Indicates if you want to debug your rule's operator syntax.

        Returns
        ---------
        :class:`NoneType`:
            This method returns None.


        .. versionadded:: 1.3.5
        """
        if self.sample:
            return None

        if dry_run:
            try:
                self.http_client.request(
                    "POST",
                    "2",
                    "/tweets/search/stream/rules",
                    params={"dry_run": dry_run},
                    json={"add": self.raw_rules},
                )
            except PytweetException as e:
                raise e
            else:
                self.http_client.request(
                    "POST",
                    "2",
                    "/tweets/search/stream/rules",
                    json={"add": self.raw_rules},
                )
                return

        self.http_client.request("POST", "2", "/tweets/search/stream/rules", json={"add": self.raw_rules})

    def connect(self, *, dry_run: bool = False) -> None:
        """Connect with the stream connection.

        Parameters
        ------------
        dry_run: :class:`bool`
            Indicates if you want to debug your rule's operator syntax. Default to None.

        Returns
        ---------
        :class:`NoneType`:
            This method returns None.


        .. versionadded:: 1.3.5
        """
        self.clear()
        self.set_rules(dry_run)
        self.connection.connect()
