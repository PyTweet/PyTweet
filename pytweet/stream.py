from __future__ import annotations

import requests
import json
import logging
import time
from typing import Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from .tweet import Tweet
from .errors import PytweetException, ConnectionException

if TYPE_CHECKING:
    from .http import HTTPClient

_log = logging.getLogger(__name__)

# def _check_for_errors(data, connection):
#     j = data.json()
#     if "errors" in j.keys():
#         raise ConnectionException(connection, None)
        

@dataclass
class StreamRule:
    value: str
    tag: Optional[str] = None

class Stream:
    def __init__(self, backfill_minutes: int = 0):
        self.backfill_minutes = backfill_minutes
        self.raw_rules: Optional[list] = []
        self.http_client: Optional[HTTPClient] = None
        self.connection: Optional[Any] = None

    @classmethod
    def SampleStream(cls, backfill_minutes: int = 0):
        self = cls(backfill_minutes)
        self.http_client: Optional[HTTPClient] = None
        self.connection: Optional[Any] = None

        def start():
            response = requests.get(
                "https://api.twitter.com/2/tweets/sample/stream",
                params={
                    "backfill_minutes": int(self.backfill_minutes),
                    "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
                    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
                    "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                    "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
                    "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
                    "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                },
                stream=True,
            )

            self.connection = response

            for response_line in response.iter_lines():
                if response_line:
                    json_data = json.loads(response_line.decode("UTF-8"))
                    tweet = Tweet(json_data, http_client=self.http_client)
                    self.http_client.dispatch("stream", tweet, self.connection)

        self.start = start
        return self

    @property
    def rules(self) -> dict:
        return [StreamRule(**data) for data in self.raw_rules]

    def add_rule(self, value: str, tag: Optional[str] = None) -> Stream:
        data = {"value": value}
        if tag:
            data["tag"] = tag
        self.raw_rules.append(data)
        return self

    def clear(self) -> None:
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

    def fetch_rules(self) -> Optional[list]:
        res = self.http_client.request(
            "GET",
            "2",
            "/tweets/search/stream/rules",
        )

        return [StreamRule(*data) for data in res]

    def set_rules(self):
        self.http_client.request("POST", "2", "/tweets/search/stream/rules", json={"add": self.raw_rules})

    def is_close(self) -> Optional[bool]:
        return self.connection is None

    def close(self) -> None:
        if self.is_close():
            PytweetException("Attemp to close a stream that's already closed!")

        _log.debug("Closing connection!")
        self.connection.close()
        self.connection = None

    def start(self, tries: int) -> Optional[Any]:
        errors = 0
        try:
            if not self.raw_rules:
                _log.warn("Attemp to stream without rules, This would not return anything!")
            
            self.clear()
            self.set_rules()
            response = requests.get(
                "https://api.twitter.com/2/tweets/search/stream",
                headers={"Authorization": f"Bearer {self.http_client.bearer_token}"},
                params={
                    "backfill_minutes": int(self.backfill_minutes),
                    "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
                    "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
                    "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                    "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
                    "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
                    "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                },
                stream=True,
            )
            _log.info("Client connected to stream!")
            self.connection = response

            for response_line in response.iter_lines():
                if response_line:
                    json_data = json.loads(response_line.decode("UTF-8"))
                    #TODO Detech if the data has errors.
                    tweet = Tweet(json_data, http_client=self.http_client)
                    self.http_client.dispatch("stream", tweet, self)
                    
        except Exception as e:
            if isinstance(e, AttributeError):
                return
            
            elif isinstance(e, requests.exceptions.RequestException):
                errors += 1
                if errors >= tries:
                    _log.error("Too many errors caught during streaming, closing stream!")
                    self.close()

                _log.info(f"An error caught during streaming session: {e}")
                _log.info(f"Reconnecting to stream after sleeping")
                time.sleep(5)

            else:
                raise e
                    
        _log.info("Streaming connection has been closed!")