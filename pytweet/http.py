from __future__ import annotations

import json as j
import logging
import sys
import time
import requests
from typing import Any, Dict, List, NoReturn, Optional, Union

from .attachments import CTA, Geo, Poll, QuickReply, File
from .auth import OauthSession
from .enums import ReplySetting, SpaceState
from .errors import BadRequests, Forbidden, NotFound, NotFoundError, PytweetException, TooManyRequests, Unauthorized
from .message import DirectMessage, Message
from .space import Space
from .tweet import Tweet
from .user import User

_log = logging.getLogger(__name__)


def check_error(response: requests.models.Response) -> NoReturn:
    code = response.status_code
    if code == 200:
        res = response.json()
        if "errors" in res.keys():
            try:
                if res["errors"][0]["detail"].startswith("Could not find"):
                    raise NotFoundError(response)

                else:
                    raise PytweetException(response, res["errors"][0]["detail"])
            except KeyError:
                raise PytweetException(res)

    elif code in (201, 202, 204):
        pass

    elif code == 400:
        raise BadRequests(response)

    elif code == 401:
        raise Unauthorized(response)

    elif code == 403:
        raise Forbidden(response)

    elif code == 404:
        raise NotFound(response)

    elif code == 429:
        text = response.text
        __check = response.headers["x-rate-limit-reset"]
        _time = time.time()
        time.sleep(_time - __check)
        raise TooManyRequests(response, text)

    else:
        raise PytweetException(
            f"Unknown exception raised (status code: {response.status_code}): Open an issue in github or go to the support server to report this unknown exception!"
        )


RequestModel: Union[Dict[str, Any], Any] = Any


class HTTPClient:
    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: Optional[str],
        consumer_key_secret: Optional[str],
        access_token: Optional[str],
        access_token_secret: Optional[str],
    ) -> Union[None, NoReturn]:
        self.credentials: Dict[str, Optional[str]] = {
            "bearer_token": bearer_token,
            "consumer_key": consumer_key,
            "consumer_key_secret": consumer_key_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }
        if not bearer_token:
            _log.error("bearer token is missing!")
        if not consumer_key:
            _log.warning("Consumer key is missing this is recommended to have!")
        if not access_token:
            _log.warning("Access token is missing this is recommended to have")
        if not access_token_secret:
            _log.warning("Access token secret is missing this is required if you have passed in the access_toke param.")

        for k, v in self.credentials.items():
            if not isinstance(v, str) and not isinstance(v, type(None)):
                raise Unauthorized(None, f"Wrong authorization passed for credential: {k}.")

        self.bearer_token: Optional[str] = bearer_token
        self.consumer_key: Optional[str] = consumer_key
        self.consumer_key_secret: Optional[str] = consumer_key_secret
        self.access_token: Optional[str] = access_token
        self.access_token_secret: Optional[str] = access_token_secret
        self.base_url = "https://api.twitter.com/"
        self.upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        self.message_cache = {}
        self.tweet_cache = {}

    def request(
        self,
        method: str,
        version: str,
        path: str,
        *,
        headers: RequestModel = {},
        params: RequestModel = {},
        json: RequestModel = {},
        auth: bool = False,
        is_json: bool = True,
    ) -> Union[str, Dict[Any, Any], NoReturn]:
        url = self.base_url + version + path
        user_agent = "Py-Tweet (https://github.com/TheFarGG/PyTweet/) Python/{0[0]}.{0[1]}.{0[2]} requests/{1}"

        if headers == {} and not "Authorization" in headers.keys():
            headers = {"Authorization": f"Bearer {self.bearer_token}"}

        headers["User-Agent"] = user_agent.format(sys.version_info, requests.__version__)

        res = getattr(requests, method.lower(), None)
        if not res:
            raise TypeError("Method isn't recognizable")

        if auth:
            auth = OauthSession(self.consumer_key, self.consumer_key_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            auth = auth.oauth1

        response = res(url, headers=headers, params=params, json=json, auth=auth)
        check_error(response)
        res = None

        try:
            res = response.json()
        except j.decoder.JSONDecodeError:
            return

        if "meta" in res.keys():
            if res["meta"]["result_count"] == 0:
                return []

        if is_json:
            return res
        return response

    def upload(self, file: File, command: str, *,media_id = None):
        assert command in ["INIT", "APPEND", "FINALIZE", "STATUS"]
        auth = OauthSession(self.consumer_key, self.consumer_key_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        auth = auth.oauth1

        def CheckStatus(processing_info, media_id):
            if not processing_info:
                return

            state = processing_info["state"]
            try:
                seconds = processing_info['check_after_secs']
            except KeyError:
                return
            
            if state == u"succeeded":
                return

            if state == u"failed":
                raise PytweetException("Failed to finalize Media!")

            time.sleep(seconds)
            params = {
                'command': 'STATUS',
                'media_id': media_id
            }

            res = requests.get(url=self.upload_url, params=params, auth=auth)
            check_error(res)
    
            processing_info = res.json().get('processing_info', None)
            CheckStatus(processing_info, media_id)
        

        if command.upper() == "INIT":
            data = {'command': "INIT", 'media_type': file.mimetype, 'total_bytes': file.total_bytes, 'media_category': file.media_category, "shared": file.dm_only}
            res = requests.post(self.upload_url, data=data, auth=auth)
            check_error(res)
            media_id = res.json()['media_id']
            return media_id

        elif command.upper() == "APPEND":
            segment_id = 0
            bytes_sent = 0
            open_file = open(file.path, 'rb')
            if not media_id:
                raise ValueError("'media_id' is None! Please specified it.")

            while bytes_sent < file.total_bytes:
                chunk = open_file.read(4*1024*1024)
                data = {
                    'command': 'APPEND',
                    'media_id': media_id,
                    'segment_index': segment_id
                }

                files = {
                    'media': chunk
                }

                res = requests.post(url=self.upload_url, data=data, files=files, auth=auth)
                bytes_sent = open_file.tell()
                segment_id = segment_id + 1

        elif command.upper() == "FINALIZE":
            data = {
                'command': 'FINALIZE',
                'media_id': media_id
            }

            res = requests.post(url=self.upload_url, data=data, auth=auth)
            check_error(res)

            processing_info = res.json().get('processing_info', None)
            CheckStatus(processing_info, media_id)

    def fetch_user(self, user_id: Union[str, int]) -> User:
        try:
            int(user_id)
        except ValueError:
            raise ValueError("user_id must be an int, or a string of digits!")

        data = self.request(
            "GET",
            "2",
            f"/users/{user_id}",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,profile_image_url,protected,public_metrics,url,username,verified,withheld,pinned_tweet_id"
            },
            is_json=True,
        )

        followers = self.request(
            "GET",
            "2",
            f"/users/{user_id}/followers",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        following = self.request(
            "GET",
            "2",
            f"/users/{user_id}/following",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        data["data"].update(
            {
                "followers": [User(follower, http_client=self) for follower in followers["data"]]
                if followers != []
                else []
            }
        )
        data["data"].update(
            {
                "following": [User(following, http_client=self) for following in following["data"]]
                if following != []
                else []
            }
        )

        return User(data, http_client=self)

    def fetch_user_byname(self, username: str) -> User:
        if "@" in username:
            username = username.replace("@", "", 1)

        data = self.request(
            "GET",
            "2",
            f"/users/by/username/{username}",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            is_json=True,
        )

        user_payload = self.fetch_user(int(data["data"].get("id")))
        data["data"].update({"followers": user_payload.followers})
        data["data"].update({"following": user_payload.following})

        return User(data, http_client=self)

    def fetch_tweet(self, tweet_id: Union[str, int]) -> Tweet:
        if not any([v for v in self.credentials.values()]):
            return None

        res = self.request(
            "GET",
            "2",
            f"/tweets/{tweet_id}",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,geo,entities,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
                "user.fields": "created_at,description,id,location,name,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                "expansions": "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                "media.fields": "duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width",
                "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
            },
            auth=True,
        )

        res2 = self.request(
            "GET",
            "2",
            f"/tweets/{tweet_id}/retweeted_by",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        res3 = self.request(
            "GET",
            "2",
            f"/tweets/{tweet_id}/liking_users",
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        user_id = res["includes"]["users"][0].get("id")
        user = self.fetch_user(int(user_id))

        res["includes"]["users"][0].update({"followers": user.followers})
        res["includes"]["users"][0].update({"following": user.following})

        try:
            res2["data"]

            res["data"].update(
                {"retweetes": [User(user, http_client=self) for user in res2["data"]]}
            )
        except (KeyError, TypeError):
            res["data"].update({"retweetes": []})

        try:
            res3["data"]

            res["data"].update(
                {"likes": [User(user, http_client=self) for user in res3["data"]]}
            )
        except (KeyError, TypeError):
            res["data"].update({"likes": []})

        return Tweet(res, http_client=self)

    def fetch_space(self, space_id: str) -> Space:
        res = self.request(
            "GET",
            "2",
            f"/spaces/{str(space_id)}",
            params={
                "space.fields": "host_ids,created_at,creator_id,id,lang,invited_user_ids,participant_count,speaker_ids,started_at,state,title,updated_at,scheduled_start,is_ticketed"
            },
        )
        return Space(res)

    def fetch_space_bytitle(self, title: str, state: SpaceState = SpaceState.live) -> Space:
        res = self.request(
            "GET",
            "2",
            "/spaces/search",
            params={
                "query": title,
                "state": state.value,
                "space.fields": "host_ids,created_at,creator_id,id,lang,invited_user_ids,participant_count,speaker_ids,started_at,state,title,updated_at,scheduled_start,is_ticketed",
            },
        )
        return Space(res)

    def send_message(
        self,
        user_id: Union[str, int],
        text: str,
        *,
        file: Optional[File] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> Optional[NoReturn]:
        data = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {"recipient_id": str(user_id)},
                    "message_data": {},
                },
            }
        }


        if quick_reply and (not isinstance(quick_reply, QuickReply)):
            raise PytweetException("'quick_reply' is not an instance of pytweet.QuickReply")

        message_data = data["event"]["message_create"]["message_data"]

        message_data["text"] = str(text)

        if file:
            media_id = self.upload(file, "INIT")
            self.upload(file, "APPEND", media_id = media_id)
            self.upload(file, "FINALIZE", media_id = media_id)

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

        res = self.request(
            "POST",
            "1.1",
            "/direct_messages/events/new.json",
            json=data,
            auth=True,
        )

        message_create = res.get("event").get("message_create")
        user_id = message_create.get("target").get("recipient_id")
        user = self.fetch_user(user_id)
        res["event"]["message_create"]["target"]["recipient"] = user

        msg = DirectMessage(res, http_client=self or self)
        self.message_cache[msg.id] = msg
        return msg

    def fetch_message(self, event_id: Union[str, int]) -> Optional[DirectMessage]:
        try:
            event_id = str(event_id)
        except ValueError:
            raise ValueError("event_id must be an integer or a :class:`str`ing of digits.")

        res = self.request("GET", "1.1", f"/direct_messages/events/show.json?id={event_id}", auth=True)

        message_create = res.get("event").get("message_create")
        user_id = message_create.get("target").get("recipient_id")
        user = self.fetch_user(user_id)
        res["event"]["message_create"]["target"]["recipient"] = user

        return DirectMessage(res, http_client=self)

    def post_tweet(
        self,
        text: str = None,
        *,
        file: Optional[File] = None,
        poll: Optional[Poll] = None,
        geo: Optional[Union[Geo, str]] = None,
        quote_tweet: Optional[Union[str, int]] = None,
        direct_message_deep_link: Optional[str] = None,
        reply_setting: Optional[str] = None,
        reply_tweet: Optional[Union[str, int]] = None,
        exclude_reply_users: Optional[List[Union[str, int]]] = None,
        super_followers_only: Optional[bool] = None,
    ) -> Union[NoReturn, Any]:
        payload = {}
        if text:
            payload["text"] = text

        if file:
            media_id = self.upload(file, "INIT")
            self.upload(file, "APPEND", media_id = media_id)
            self.upload(file, "FINALIZE", media_id = media_id)

            payload["media"] = {}
            payload["media"]["media_ids"] = [str(media_id)]

        if poll:
            payload["poll"] = {}
            payload["poll"]["options"] = [option.label for option in poll.options]
            payload["poll"]["duration_minutes"] = int(poll.duration)

        if geo:
            if not isinstance(geo, Geo) and not isinstance(geo, str):
                raise TypeError("'geo' is not an instance of Geo or str")

            payload["geo"] = {}
            payload["geo"]["place_id"] = geo.id if isinstance(geo, Geo) else geo

        if quote_tweet:
            payload["quote_tweet_id"] = str(quote_tweet)

        if direct_message_deep_link:
            payload["direct_message_deep_link"] = direct_message_deep_link

        if reply_setting:
            payload["reply_settings"] = (
                reply_setting.value if isinstance(reply_setting, ReplySetting) else reply_setting
            )

        if reply_tweet or exclude_reply_users:
            if reply_tweet:
                payload["reply"] = {}
                payload["reply"]["in_reply_to_tweet_id"] = str(reply_tweet)

            if exclude_reply_users:
                if "reply" in payload.keys():
                    payload["reply"]["exclude_reply_user_ids"] = [str(id) for id in exclude_reply_users]
                else:
                    payload["reply"] = {}
                    payload["reply"]["exclude_reply_user_ids"] = [str(id) for id in exclude_reply_users]

        if super_followers_only:
            payload["for_super_followers_only"] = True

        res = self.request("POST", "2", "/tweets", json=payload, auth=True)
        data = res.get("data")
        tweet = Message(data.get("text"), data.get("id"), 1)
        return tweet