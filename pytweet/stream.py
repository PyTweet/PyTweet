from __future__ import annotations

import requests
import json
from typing import Optional, TYPE_CHECKING
from dataclasses import dataclass
from .tweet import Tweet

if TYPE_CHECKING:
    from .http import HTTPClient
    
@dataclass
class StreamRule:
    value: str
    tag: Optional[str] = None

class Stream:
    def __init__(self, backfill_minutes: int = 0):
        self.backfill_minutes = backfill_minutes
        self.raw_rules: Optional[list] = []
        self.http_client: Optional[HTTPClient] = None

    @classmethod
    def SampleStream(cls, backfill_minutes: int = 0):
        self = cls(backfill_minutes)
        self.http_client: Optional[HTTPClient] = None
        def start():
            response = requests.get(
            "https://api.twitter.com/2/tweets/sample/stream",
            headers={"Authorization": f"Bearer {self.http_client.bearer_token}"},
            params={
                "backfill_minutes": int(self.backfill_minutes),
                "expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
                "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics,alt_text",
                "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
                "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
                },
                stream = True
            )

            for response_line in response.iter_lines():
                if response_line:
                    json_data = json.loads(response_line.decode('UTF-8'))
                    tweet = Tweet(json_data, http_client = self.http_client)
                    self.http_client.dispatch("stream", tweet)
            
        self.start = start
        return self

    @property
    def rules(self) -> dict:
        return [StreamRule(**data) for data in self.raw_rules]
        
    def add_rule(self, value: str, tag: Optional[str] = None) -> Stream:
        data = {"value":value}
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
            rules = self.http_client.request(
                "POST",
                "2",
                "/tweets/search/stream/rules",
                json = data
            )

    def set_rules(self):
        self.http_client.request(
            "POST",
            "2",
            "/tweets/search/stream/rules",
            json = {"add": self.raw_rules}
        )

    def start(self):
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
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            stream = True
        )

        for response_line in response.iter_lines():
            if response_line:
                json_data = json.loads(response_line.decode('UTF-8'))
                tweet = Tweet(json_data, http_client = self.http_client)
                self.http_client.dispatch("stream", tweet)
        