from __future__ import annotations

import io
import logging
import sys
import time
import requests
import random
import string
from json import JSONDecodeError
from typing import Any, List, NoReturn, Optional, Union, TYPE_CHECKING

from .attachments import CTA, CustomProfile, File, Geo, Poll, QuickReply
from .auth import OauthSession
from .enums import ReplySetting, SpaceState, Granularity
from .errors import (
    BadRequests,
    Conflict,
    Forbidden,
    NotFound,
    NotFoundError,
    TooManyRequests,
    PytweetException,
    Unauthorized,
    FieldsTooLarge,
)
from .constants import (
    MEDIA_FIELD,
    PLACE_FIELD,
    POLL_FIELD,
    SPACE_FIELD,
    TWEET_EXPANSION,
    SPACE_EXPANSION,
    TWEET_FIELD,
    USER_FIELD,
    TOPIC_FIELD,
    LIST_FIELD,
    LIST_EXPANSION,
)
from .message import DirectMessage, Message, WelcomeMessage, WelcomeMessageRule
from .parsers import EventParser
from .space import Space
from .tweet import Tweet
from .user import User, ClientAccount
from .threads import ThreadManager
from .relations import RelationUpdate
from .list import List as TwitterList

if TYPE_CHECKING:
    from .type import ID, Payload, ResponsePayload
    from .stream import Stream

_log = logging.getLogger(__name__)


class HTTPClient:
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
        sleep_after_ratelimit: bool = False,
    ) -> Union[None, NoReturn]:
        self.credentials = {
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
            _log.warning(
                "Access token secret is missing this is required if you have passed in the access_token param."
            )

        for k, v in self.credentials.items():
            if not isinstance(v, (str, type(None))):
                raise Unauthorized(None, f"Wrong authorization passed for credential: {k}.")

        self.__session = requests.Session()
        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.stream = stream
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.use_bearer_only = use_bearer_only
        self.event_parser = EventParser(self)
        self.payload_parser = self.event_parser.payload_parser
        self.thread_manager = ThreadManager()
        self.sleep_after_ratelimit = sleep_after_ratelimit
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
        self.current_header = None
        self.client_id = client_id
        self.message_cache = {}
        self.tweet_cache = {}
        self.user_cache = {}
        self.events = {}
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

    def dispatch(self, event_name: str, *args: Any, **kwargs: Any) -> Any:
        event = self.events.get(event_name)
        if not event:
            return None

        _log.debug(f"Dispatching Event: on_{event_name}")
        return event(*args, **kwargs)

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
        thread_name: Optional[str] = None,
        thread_session: bool = False,
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
        if thread_session:
            executor = self.thread_manager.create_new_executor(thread_name=thread_name, session_id=thread_session)
            future = executor.submit(
                self.request,
                method,
                version,
                path,
                headers=headers,
                params=params,
                data=data,
                json=json,
                files=files,
                auth=auth,
            )
            return future

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
                if self.sleep_after_ratelimit:
                    remaining = int(response.headers["x-rate-limit-reset"])
                    sleep_for = (remaining - int(time.time())) + 1
                    _log.warn(f"Client is ratelimited. Sleeping for {sleep_for}")
                    print(f"Client is ratelimited. Sleeping for {sleep_for}")
                    time.sleep(sleep_for)
                    return self.request(
                        method,
                        version,
                        path,
                        headers=headers,
                        params=params,
                        data=data,
                        json=json,
                        files=files,
                        auth=auth,
                    )

                else:
                    raise TooManyRequests(response)

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
            executor = self.thread_manager.create_new_executor(thread_name="subfiles-upload-request")
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
                alt_text_future = self.request(
                    "POST",
                    "1.1",
                    "/media/metadata/create.json",
                    json={"media_id": str(file.media_id), "alt_text": {"text": str(file.alt_text)}},
                    auth=True,
                    use_base_url=False,
                    thread_name="alt-text-file-request",
                    thread_session=thread_session,
                )

            if file.subfile:
                executor.submit(self.quick_upload, file.subfile)

            if file.subfiles:
                for subfile in file.subfiles:
                    executor.submit(self.quick_upload, subfile)

            if file.subfiles or file.subfile:
                subtitles = []
                executor.wait_for_futures()
                if file.subfiles:
                    for subfile in file.subfiles:
                        subtitles.append(
                            {
                                "media_id": str(subfile.media_id),
                                "display_name": subfile.language,
                                "language_code": subfile.language_code,
                            }
                        )

                if file.subfile:
                    subtitles.append(
                        {
                            "media_id": str(file.subfile.media_id),
                            "display_name": file.subfile.language,
                            "language_code": file.subfile.language_code,
                        }
                    )

                subtitle_data = {
                    "media_id": str(file.media_id),
                    "media_category": file.media_category,
                    "subtitle_info": {"subtitles": subtitles},
                }

                self.request(
                    "POST",
                    version="1.1",
                    path="/media/subtitles/create.json",
                    json=subtitle_data,
                    auth=True,
                    use_base_url=False,
                    thread_name=f"subfile-request:FILE-MEDIA-ID={file.media_id}:SUBFILE-MEDIA-ID={file.subfile.media_id}",
                )

            if file.alt_text:
                alt_text_future.result()

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

        res = self.request(
            "GET",
            "2",
            f"/users?ids={','.join(str_ids)}",
            params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
            auth=True,
        )

        users = [User(data, http_client=self) for data in res["data"]]
        for user in users:
            self.user_cache[user.id] = user
        return users

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
            user = User(data, http_client=self)
            self.user_cache[user.id] = user
            return user
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

            tweet = Tweet(res, http_client=self)
            self.tweet_cache[tweet.id] = tweet
            return tweet
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

    def fetch_spaces_bytitle(self, title: str, state: SpaceState = SpaceState.live) -> Space:
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
        return [Space(data, http_client=self) for data in res]

    def fetch_list(self, id: ID) -> TwitterList:
        res = self.request(
            "GET",
            "2",
            f"/lists/{id}",
            auth=True,
            params={
                "expansions": LIST_EXPANSION,
                "list.fields": LIST_FIELD,
                "user.fields": USER_FIELD,
            },
        )
        return TwitterList(res, http_client=self)

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
        granularity: Granularity = Granularity.neighborhood,
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
                "granularity": granularity.value,
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

        executor = self.thread_manager.create_new_executor(
            thread_name="post-tweet-file-request", session_id=thread_session
        )
        message_data = data["event"]["message_create"]["message_data"]
        message_data["text"] = str(text)

        if file:
            future = executor.submit(self.quick_upload, file)

        if custom_profile:
            message_data["custom_profile_id"] = str(custom_profile.id)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        if file:
            file = future.result()
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
        thread_session = self.generate_thread_session()
        executor = self.thread_manager.create_new_executor(thread_name="post-tweet-request", session_id=thread_session)

        payload = {}
        if text:
            payload["text"] = text

        if file:
            payload["media"] = {}
            payload["media"]["media_ids"] = []
            file_future = executor.submit(self.quick_upload, file)
            executor.futures.append(file_future)

        if files:
            if len(files) + 1 if file else len(files) > 4:
                raise BadRequests(message="Cannot upload more then 4 files!")

            payload["media"] = {}
            payload["media"]["media_ids"] = []
            for file in files:
                future = executor.submit(self.quick_upload, file)
                executor.futures.append(future)

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

        executor.wait_for_futures()

        if file:
            payload["media"]["media_ids"].append(str(file.media_id))
        if files:
            for file in files:
                payload["media"]["media_ids"].append(str(file.media_id))

        res = self.request("POST", "2", "/tweets", json=payload, auth=True)
        data = res.get("data")
        return Message(data.get("text"), data.get("id"), 1)

    def create_list(self, name: str, *, description: str = "", private: bool = False) -> Optional[TwitterList]:
        res = self.request(
            "POST", "2", "/lists", auth=True, json={"name": name, "description": description, "private": private}
        )
        return TwitterList(res, http_client=self)

    def update_list(
        self, list_id: int, *, name: Optional[str] = None, description: str = "", private: Optional[bool] = None
    ) -> Optional[RelationUpdate]:
        res = self.request(
            "PUT",
            "2",
            f"/lists/{list_id}",
            auth=True,
            json={"name": name, "description": description, "private": private},
        )
        return RelationUpdate(res)

    def create_custom_profile(self, name: str, file: File) -> Optional[CustomProfile]:
        file = self.quick_upload(file)
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
        executor = self.thread_manager.create_new_executor(
            thread_name="create-welcome-message-file-request", session_id=thread_session
        )
        data = {"welcome_message": {"message_data": {}}}
        message_data = data["welcome_message"]["message_data"]
        data["welcome_message"]["name"] = str(name)
        message_data["text"] = str(text)

        if file:
            file_future = executor.submit(self.quick_upload, file)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        if file:
            message_data["attachment"] = {}
            message_data["attachment"]["type"] = "media"
            message_data["attachment"]["media"] = {}
            message_data["attachment"]["media"]["id"] = str(file_future.result().media_id)

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
        executor = self.thread_manager.create_new_executor(
            thread_name="update-welcome-message-file-request", session_id=thread_session
        )
        data = {"message_data": {}}
        message_data = data["message_data"]
        message_data["text"] = str(text)

        if file:
            file_future = executor.submit(self.quick_upload, file)

        if quick_reply:
            message_data["quick_reply"] = {
                "type": quick_reply.type,
                "options": quick_reply.raw_options,
            }

        if cta:
            message_data["ctas"] = cta.raw_buttons

        if file:
            message_data["attachment"] = {}
            message_data["attachment"]["type"] = "media"
            message_data["attachment"]["media"] = {}
            message_data["attachment"]["media"]["id"] = str(file_future.result().media_id)

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
