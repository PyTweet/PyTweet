from __future__ import annotations

import io
import logging
import sys
import time
import requests
import threading
import random
import string
from json import JSONDecodeError
from typing import Dict, List, NoReturn, Optional, Union, TYPE_CHECKING

from .attachments import CTA, CustomProfile, File, Geo, Poll, QuickReply
from .auth import OauthSession
from .enums import ReplySetting, SpaceState
from .errors import (
    BadRequests,
    Conflict,
    Forbidden,
    NotFound,
    NotFoundError,
    PytweetException,
    Unauthorized,
    FieldsTooLarge,
)
from .expansions import (
    MEDIA_FIELD,
    PLACE_FIELD,
    POLL_FIELD,
    SPACE_FIELD,
    TWEET_EXPANSION,
    SPACE_EXPANSION,
    TWEET_FIELD,
    USER_FIELD,
    TOPIC_FIELD,
)
from .message import DirectMessage, Message, WelcomeMessage, WelcomeMessageRule
from .parsers import EventParser
from .space import Space
from .tweet import Tweet
from .user import User, ClientAccount
from .mixins import EventMixin

if TYPE_CHECKING:
    from .type import ID, Payload, ResponsePayload
    from .stream import Stream

_log = logging.getLogger(__name__)
get_kwargs = lambda **kwargs: kwargs


class HTTPClient(EventMixin):
    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: Optional[str],
        consumer_secret: Optional[str],
        access_token: Optional[str],
        access_token_secret: Optional[str],
        stream: Optional[Stream] = None,
        callback_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        use_bearer_only: bool = False,
    ) -> Union[None, NoReturn]:
        self.credentials: Dict[str, Optional[str]] = {
            "bearer_token": bearer_token,
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
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

        self.__session = requests.Session()
        self.bearer_token: Optional[str] = bearer_token
        self.consumer_key: Optional[str] = consumer_key
        self.consumer_secret: Optional[str] = consumer_secret
        self.access_token: Optional[str] = access_token
        self.access_token_secret: Optional[str] = access_token_secret
        self.stream = stream
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_bearer_only = use_bearer_only
        self.event_parser = EventParser(self)
        self.payload_parser = self.event_parser.payload_parser
        self.threading = threading
        self.base_url = "https://api.twitter.com/"
        self.upload_url = "https://upload.twitter.com/"
        self._auth = OauthSession(
            self.consumer_key,
            self.consumer_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret,
            http_client=self,
            callback_url=self.callback_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )
        self.current_header: Optional[Payload] = None
        self.client_id = client_id
        self.message_cache = {}
        self.tweet_cache = {}
        self.user_cache = {}
        if self.stream:
            self.stream.http_client = self
            self.stream.connection.http_client = self

    @property
    def access_levels(self) -> Optional[list]:
        return self.current_header.get("x-access-levels").split("-") if self.current_header else None

    @property
    def oauth_session(self) -> OauthSession:
        return self._auth

    def generate_thread_session(self):
        return "".join((random.sample(string.ascii_lowercase, 10)))

    def request(
        self,
        method: str,
        version: str,
        path: str,
        *,
        headers: Payload = {},
        params: Payload = {},
        json: Payload = {},
        data: Payload = {},
        files: Payload = {},
        auth: bool = False,
        basic_auth: bool = False,
        thread_name: bool = False,
        use_base_url: bool = True,
        is_json: bool = True,
    ) -> ResponsePayload:
        if use_base_url:
            url = self.base_url + version + path
        else:
            url = self.upload_url + version + path

        user_agent = "Py-Tweet (https://github.com/PyTweet/PyTweet/) Python/{0[0]}.{0[1]}.{0[2]} requests/{1}"
        if "Authorization" not in headers.keys():
            headers["Authorization"] = f"Bearer {self.bearer_token}"

        headers["User-Agent"] = user_agent.format(sys.version_info, requests.__version__)

        if not self.use_bearer_only:
            if auth:
                auth = self.oauth_session.oauth1
                for k, v in self.credentials.items():
                    if v is None:
                        raise PytweetException(f"{k} is a required credential for authorization.")

            if basic_auth:
                headers["Authorization"] = f"Basic {self.oauth_session.basic_auth}"

        else:
            auth = None
            basic_auth = None

        if data:
            json = None

        if json:
            data = None

        method = method.upper()
        if thread_name:
            thread = self.threading.Thread(
                name=thread_name,
                target=self.request,
                args=(method, version, path),
                kwargs=get_kwargs(headers=headers, params=params, data=data, json=json, files=files, auth=auth),
            )
            thread.start()
            return thread

        else:
            response = self.__session.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                files=files,
                auth=auth,
            )
            code = response.status_code
            self.current_header = response.headers
            res = None
            _log.debug(
                f"{method} {url} has returned: "
                f"{response.status_code} {response.reason}\n"
                f"Headers: {response.headers}\n"
                f"Content: {response.content}\n"
                f"Json-payload: {json}\n"
            )

            if code in (201, 202, 204):
                if is_json:
                    try:
                        res = response.json()
                    except JSONDecodeError:
                        return response.text
                else:
                    return response.text
                return res

            elif code == 400:
                raise BadRequests(response)

            elif code == 401:
                raise Unauthorized(response)

            elif code == 403:
                raise Forbidden(response)

            elif code == 404:
                raise NotFound(response)

            elif code == 409:
                raise Conflict(response)

            elif code in (420, 429):
                remaining = int(response.headers["x-rate-limit-reset"])
                sleep_for = (remaining - int(time.time())) + 1
                _log.warn(f"Client has been ratelimited. Sleeping for {sleep_for}")
                time.sleep(sleep_for)

            elif code == 431:
                raise FieldsTooLarge(response)

            if is_json:
                try:
                    res = response.json()
                except JSONDecodeError:
                    return response.text
            else:
                return response.text

            if isinstance(res, dict):
                if "meta" in res.keys():
                    try:
                        if res["meta"]["result_count"] == 0:
                            return []
                    except KeyError:
                        pass

            return res

    def upload(self, file: File, command: str):
        assert command.upper() in ("INIT", "APPEND", "FINALIZE", "STATUS")
        thread_session = self.generate_thread_session()

        def check_status(processing_info, media_id):
            if not processing_info:
                return

            state = processing_info["state"]
            seconds = processing_info.get("check_after_secs")
            if seconds is None:
                return None

            if state == "succeeded":
                return

            if state == "failed":
                raise PytweetException(f"Failed to finalize Media!\n{processing_info}")

            time.sleep(seconds)

            res = self.request(
                "GET",
                version="1.1",
                path="/media/upload.json",
                params={"command": "STATUS", "media_id": media_id},
                auth=True,
                use_base_url=False,
            )

            processing_info = res.get("processing_info", None)
            check_status(processing_info, media_id)

        if command.upper() == "INIT":
            data = {
                "command": "INIT",
                "media_type": file.mimetype,
                "total_bytes": file.total_bytes,
                "media_category": file.media_category,
                "shared": file.dm_only,
            }

            res = self.request(
                "POST",
                "1.1",
                "/media/upload.json",
                data=data,
                auth=True,
                use_base_url=False,
            )

            file._File__media_id = res["media_id"]
            return res["media_id"]

        elif command.upper() == "APPEND":
            segment_id = 0
            bytes_sent = 0
            path = file.path
            if isinstance(path, io.IOBase):
                open_file = path
            else:
                open_file = open(path, "rb")

            if not file.media_id:
                raise ValueError("'media_id' is None! Please specified it.")

            while bytes_sent < file.total_bytes:
                self.request(
                    "POST",
                    version="1.1",
                    path="/media/upload.json",
                    data={
                        "command": "APPEND",
                        "media_id": file.media_id,
                        "segment_index": segment_id,
                    },
                    files={"media": open_file.read(4 * 1024 * 1024)},
                    auth=True,
                    use_base_url=False,
                )

                bytes_sent = open_file.tell()
                segment_id += 1

        elif command.upper() == "FINALIZE":
            res = self.request(
                "POST",
                version="1.1",
                path="/media/upload.json",
                data={"command": "FINALIZE", "media_id": file.media_id},
                auth=True,
                use_base_url=False,
            )

            check_status(res.get("processing_info", None), file.media_id)
            if file.alt_text:
                self.request(
                    "POST",
                    "1.1",
                    "/media/metadata/create.json",
                    json={"media_id": str(file.media_id), "alt_text": {"text": str(file.alt_text)}},
                    auth=True,
                    use_base_url=False,
                    thread_name=f"alt-text-request:FILE-MEDIA-ID={file.media_id}:thread_session={thread_session}",
                )

            if file.subfile:
                self.threading.Thread(
                    target=self.quick_upload,
                    name=f"upload-subfile-request:FILE-MEDIA-ID={file.media_id}:SUBFILE-MEDIA-ID={file.subfile.media_id}:thread_session={thread_session}",
                    args=(file.subfile,),
                ).start()

                for thread in self.threading.enumerate():
                    if "upload-subfile-request" in thread.name:
                        thread.join()

                subtitle_data = {
                    "media_id": str(file.media_id),
                    "media_category": file.media_category,
                    "subtitle_info": {
                        "subtitles": [
                            {
                                "media_id": str(file.subfile.media_id),
                                "display_name": file.subfile.language,
                                "language_code": file.subfile.language_code,
                            }
                        ]
                    },
                }

                self.request(
                    "POST",
                    version="1.1",
                    path="/media/subtitles/create.json",
                    json=subtitle_data,
                    auth=True,
                    use_base_url=False,
                    thread_name=f"subfile-request:FILE-MEDIA-ID={file.media_id}:SUBFILE-MEDIA-ID={file.subfile.media_id}:thread_session={thread_session}",
                )

            for thread in self.threading.enumerate():
                if thread_session in thread.name:
                    thread.join()

    def quick_upload(self, file: File) -> File:
        self.upload(file, "INIT")
        self.upload(file, "APPEND")
        self.upload(file, "FINALIZE")
        return file

    def fetch_me(self):
        data = self.request(
            "GET",
            "2",
            f"/users/me",
            params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
            auth=True,
        )

        return User(data, http_client=self)

    def fetch_user(self, user_id: ID) -> Optional[User]:
        try:
            int(user_id)
        except ValueError:
            raise ValueError("user_id must be an int, or a string of digits!")

        try:
            data = self.request(
                "GET",
                "2",
                f"/users/{user_id}",
                params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
                auth=True,
            )

            return User(data, http_client=self)
        except NotFoundError:
            return None

    def fetch_users(self, ids: List[ID]) -> List[User]:
        str_ids = []
        for id in ids:
            try:
                int(id)
            except ValueError as e:
                raise e
            else:
                str_ids.append(str(id))

        ids = ",".join(str_ids)
        res = self.request(
            "GET",
            "2",
            f"/users?ids={ids}",
            params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
            auth=True,
        )

        return [User(data, http_client=self) for data in res["data"]]

    def fetch_user_by_username(self, username: str) -> Optional[User]:
        if username.startswith("@"):
            username = username.replace("@", "", 1)

        try:
            data = self.request(
                "GET",
                "2",
                f"/users/by/username/{username}",
                params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
                auth=True,
            )
            return User(data, http_client=self)
        except NotFoundError:
            return None

    def fetch_tweet(self, tweet_id: ID) -> Optional[Tweet]:
        try:
            res = self.request(
                "GET",
                "2",
                f"/tweets/{tweet_id}",
                params={
                    "tweet.fields": TWEET_FIELD,
                    "user.fields": USER_FIELD,
                    "expansions": TWEET_EXPANSION,
                    "media.fields": MEDIA_FIELD,
                    "place.fields": PLACE_FIELD,
                    "poll.fields": POLL_FIELD,
                },
                auth=True,
            )

            return Tweet(res, http_client=self)
        except NotFoundError:
            return None

    def fetch_space(self, space_id: str) -> Space:
        res = self.request(
            "GET",
            "2",
            f"/spaces/{str(space_id)}",
            params={
                "expansions": SPACE_EXPANSION,
                "space.fields": SPACE_FIELD,
                "topic.fields": TOPIC_FIELD,
                "user.fields": USER_FIELD,
            },
        )
        return Space(res, http_client=self)

    def fetch_space_bytitle(self, title: str, state: SpaceState = SpaceState.live) -> Space:
        res = self.request(
            "GET",
            "2",
            "/spaces/search",
            params={
                "query": title,
                "state": state.value,
                "expansions": SPACE_EXPANSION,
                "space.fields": SPACE_FIELD,
                "topic.fields": TOPIC_FIELD,
            },
        )
        return Space(res, http_client=self)

    def handle_events(self, payload: Payload):
        if payload.get("direct_message_events"):
            self.event_parser.parse_direct_message_create(payload)

        elif payload.get("direct_message_indicate_typing_events"):
            self.event_parser.parse_direct_message_typing(payload)

        elif payload.get("direct_message_mark_read_events"):
            self.event_parser.parse_direct_message_read(payload)

        elif payload.get("favorite_events"):
            self.event_parser.parse_favorite_tweet(payload)

        elif payload.get("follow_events"):
            self.event_parser.parse_user_action(payload, "follow_events")

        elif payload.get("block_events"):
            self.event_parser.parse_user_action(payload, "block_events")

        elif payload.get("mute_events"):
            self.event_parser.parse_user_action(payload, "mute_events")

        elif payload.get("tweet_create_events"):
            self.event_parser.parse_tweet_create(payload)

        elif payload.get("tweet_delete_events"):
            self.event_parser.parse_tweet_delete(payload)

    def fetch_direct_message(self, event_id: ID) -> Optional[DirectMessage]:
        try:
            event_id = str(event_id)
        except ValueError:
            raise ValueError("event_id must be an integer or a string of digits.")

        res = self.request("GET", "1.1", f"/direct_messages/events/show.json?id={event_id}", auth=True)

        message_create = res.get("event").get("message_create")
        user_id = message_create.get("target").get("recipient_id")
        user = self.fetch_user(user_id)
        res["event"]["message_create"]["target"]["recipient"] = user

        return DirectMessage(res, http_client=self)

    def fetch_welcome_message(self, welcome_message_id: ID) -> Optional[WelcomeMessage]:
        try:
            welcome_message_id = str(welcome_message_id)
        except ValueError:
            raise ValueError("welcome_message_id must be an integer or a string of digits.")

        res = self.request(
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
        return WelcomeMessage(text=text, id=id, timestamp=timestamp, http_client=self)

    def fetch_welcome_message_rule(self, welcome_message_rule_id) -> Optional[WelcomeMessageRule]:
        res = self.request(
            "GET",
            "1.1",
            "/direct_messages/welcome_messages/rules/show.json",
            params={"id": str(welcome_message_rule_id)},
            auth=True,
        )
        data = res.get("welcome_message_rule")
        id = data.get("id")
        timestamp = data.get("created_timestamp")
        welcome_message_id = data.get("welcome_message_id")
        return WelcomeMessageRule(id, welcome_message_id, timestamp, http_client=self)

    def search_geo(
        self,
        query: str,
        max_result: Optional[ID] = None,
        *,
        lat: Optional[int] = None,
        long: Optional[int] = None,
        ip: Optional[ID] = None,
        granularity: str = "neighborhood",
    ) -> Optional[Geo]:
        if query:
            query = query.replace(" ", "%20")

        data = self.request(
            "GET",
            "1.1",
            "/geo/search.json",
            params={
                "query": query,
                "lat": lat,
                "long": long,
                "ip": ip,
                "granularity": granularity,
                "max_results": max_result,
            },
            auth=True,
        )

        return [Geo(data) for data in data.get("result").get("places")]

    def send_message(
        self,
        recipient_id: ID,
        text: str,
        *,
        file: Optional[File] = None,
        custom_profile: Optional[CustomProfile] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ) -> Optional[NoReturn]:
        thread_session = self.generate_thread_session()
        data = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {"recipient_id": str(recipient_id)},
                    "message_data": {},
                },
            }
        }

        message_data = data["event"]["message_create"]["message_data"]
        message_data["text"] = str(text)

        if file:
            self.threading.Thread(
                name=f"post-tweet-file-request:thread_session={thread_session}",
                target=self.quick_upload,
                args=(file,),
            ).start()

        if custom_profile:
            message_data["custom_profile_id"] = str(custom_profile.id)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        for thread in self.threading.enumerate():
            if thread_session in thread.name:
                thread.join()
                message_data["attachment"] = {}
                message_data["attachment"]["type"] = "media"
                message_data["attachment"]["media"] = {}
                message_data["attachment"]["media"]["id"] = str(file.media_id)

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

        msg = DirectMessage(res, http_client=self)
        self.message_cache[msg.id] = msg
        return msg

    def post_tweet(
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
    ) -> Optional[Message]:
        payload = {}
        thread_session = self.generate_thread_session()
        if text:
            payload["text"] = text

        if file:
            payload["media"] = {}
            payload["media"]["media_ids"] = []
            self.threading.Thread(
                name=f"post-tweet-file-request:thread_session={thread_session}",
                target=self.quick_upload,
                args=(file,),
            ).start()

        if files:
            payload["media"] = {}
            payload["media"]["media_ids"] = []
            for file in files:
                if payload.get("media", None):
                    self.threading.Thread(
                        name=f"post-tweet-files-request:thread_session={thread_session}",
                        target=self.quick_upload,
                        args=(file,),
                    ).start()

                else:
                    self.threading.Thread(
                        name=f"post-tweet-files-request:thread_session={thread_session}",
                        target=self.quick_upload,
                        args=(file,),
                    ).start()

        if poll:
            payload["poll"] = {}
            payload["poll"]["duration_minutes"] = int(poll.duration)
            payload["poll"]["options"] = [option.label for option in poll.options]

        if geo:
            payload["geo"] = {}
            payload["geo"]["place_id"] = geo.id if isinstance(geo, Geo) else geo

        if direct_message_deep_link:
            payload["direct_message_deep_link"] = direct_message_deep_link

        if reply_setting:
            payload["reply_settings"] = (
                reply_setting.value if isinstance(reply_setting, ReplySetting) else reply_setting
            )

        if reply_tweet:
            payload["reply"] = {}
            payload["reply"]["in_reply_to_tweet_id"] = (
                reply_tweet.id if isinstance(reply_tweet, Tweet) else str(reply_tweet)
            )

        if quote_tweet:
            payload["quote_tweet_id"] = quote_tweet.id if isinstance(quote_tweet, Tweet) else str(quote_tweet)

        if exclude_reply_users:
            ids = [str(user.id) if isinstance(user, User) else str(user) for user in exclude_reply_users]

            if "reply" in payload.keys():
                payload["reply"]["exclude_reply_user_ids"] = ids
            else:
                payload["reply"] = {}
                payload["reply"]["exclude_reply_user_ids"] = ids

        if media_tagged_users:
            if not payload.get("media"):
                raise PytweetException("Cannot tag users without any file!")
            payload["media"]["tagged_user_ids"] = [
                str(user.id) if isinstance(user, (User, ClientAccount)) else str(user) for user in media_tagged_users
            ]

        if super_followers_only:
            payload["for_super_followers_only"] = True

        for thread in self.threading.enumerate():
            if thread_session in thread.name:
                thread.join()
                if "file-request" in thread.name:
                    payload["media"]["media_ids"] = [str(file.media_id)]

                elif "files-request" in thread.name:
                    if payload.get("media", None):
                        payload["media"]["media_ids"].append(str(file.media_id))
                    else:
                        payload["media"] = {}
                        payload["media"]["media_ids"] = [str(file.media_id)]

        res = self.request("POST", "2", "/tweets", json=payload, auth=True)
        data = res.get("data")
        return Message(data.get("text"), data.get("id"), 1)

    def create_custom_profile(self, name: str, file: File) -> Optional[CustomProfile]:
        thread_session = self.create_thread_session()
        self.threading.Thread(
            name=f"create-custom-profile-file-request:thread_session={thread_session}",
            target=self.quick_upload,
            args=(file,),
        ).start()

        for thread in self.threading.enumerate():
            if thread_session in thread.name:
                thread.join()

        data = {"custom_profile": {"name": name, "avatar": {"media": {"id": file.media_id}}}}

        res = self.request("POST", "1.1", "/custom_profiles/new.json", json=data, auth=True)
        data = res.get("custom_profile")

        return CustomProfile(
            data.get("name"),
            data.get("id"),
            data.get("created_timestamp"),
            data.get("avatar"),
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
        thread_session = self.generate_thread_session()
        data = {"welcome_message": {"message_data": {}}}
        message_data = data["welcome_message"]["message_data"]
        data["welcome_message"]["name"] = str(name)
        message_data["text"] = str(text)

        if file:
            self.threading.Thread(
                name=f"update-welcome-message-file-request:FILE-MEDIA-ID={file.media_id}:thread_session={thread_session}",
                target=self.quick_upload,
                args=(file,),
            ).start()

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        for thread in self.threading.enumerate():
            if thread_session in thread.name:
                thread.join()
                message_data["attachment"] = {}
                message_data["attachment"]["type"] = "media"
                message_data["attachment"]["media"] = {}
                message_data["attachment"]["media"]["id"] = str(file.media_id)
                break

        res = self.request(
            "POST",
            "1.1",
            "/direct_messages/welcome_messages/new.json",
            json=data,
            auth=True,
        )

        data = res.get("welcome_message")
        message_data = data.get("message_data")

        return WelcomeMessage(
            res.get("name"),
            text=message_data.get("text"),
            id=data.get("id"),
            timestamp=data.get("created_timestamp"),
            http_client=self,
        )

    def update_welcome_message(
        self,
        *,
        welcome_message_id: ID,
        text: Optional[str] = None,
        file: Optional[File] = None,
        quick_reply: Optional[QuickReply] = None,
        cta: Optional[CTA] = None,
    ):
        thread_session = self.generate_thread_session()
        data = {"message_data": {}}
        message_data = data["message_data"]
        message_data["text"] = str(text)

        if file:
            self.threading.Thread(
                name=f"update-welcome-message-file-request:FILE-MEDIA-ID={file.media_id}:thread_session={thread_session}",
                target=self.quick_upload,
                args=(file,),
            ).start()

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        for thread in self.threading.enumerate():
            if thread_session in thread.name:
                thread.join()
                message_data["attachment"] = {}
                message_data["attachment"]["type"] = "media"
                message_data["attachment"]["media"] = {}
                message_data["attachment"]["media"]["id"] = str(file.media_id)
                break

        res = self.request(
            "PUT",
            "1.1",
            "/direct_messages/welcome_messages/update.json",
            params={"id": str(welcome_message_id)},
            json=data,
            auth=True,
        )

        welcome_message = res.get("welcome_message")
        message_data = welcome_message.get("message_data")

        return WelcomeMessage(
            res.get("name"),
            text=message_data.get("text"),
            id=welcome_message.get("id"),
            timestamp=welcome_message.get("created_timestamp"),
            http_client=self,
        )
