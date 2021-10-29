"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests
from typing import Dict, Any, Optional, NoReturn, Union
from .errors import (
    Unauthorized,
    NotFoundError,
    TooManyRequests,
    Forbidden,
    PytweetException,
)
from .user import User
from .tweet import Tweet
from .auth import OauthSession
from .relations import RelationFollow

def check_error(respond: requests.models.Response):
    code = respond.status_code
    if code == 401:
        raise Unauthorized("Invalid credentials passed!")

    elif code == 403:
        raise Forbidden("Forbidden to interact with that User!")

    elif code == 429:
        raise TooManyRequests(respond.text)


RequestModel: Dict[str, Any] = Any


class Route:
    def __init__(self, method: str, version: str, path: str):
        self.method: str = method
        self.path: str = path
        self.base_url = f"https://api.twitter.com/{version}"
        self.url: str = self.base_url + self.path


class HTTPClient:
    """Represent the http/base client for :class: Client!
    This http/base client have methods for making requests to twitter's api!
    Verion Added: 1.0.0

    Parameters:
    -----------
    bearer_token: str
        The Bearer Token of the app. The most important one, because this make most of the requests for twitter's api version 2.

    consumer_key: Optional[str]
        The Consumer Key of the app.

    consumer_key_secret: Optional[str]
        The Consumer Key Secret of the app.

    access_token: Optional[str]
        The Access Token of the app.

    access_token_secret: Optional[str]
        The Access Token Secret of the app.

    credentials
        The credentials in a dictionary
    """

    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: Optional[str],
        consumer_key_secret: Optional[str],
        access_token: Optional[str],
        access_token_secret: Optional[str],
    ) -> None:
        self.credentials: Dict[str, Optional[str]] = {
            "bearer_token": bearer_token,
            "consumer_key": consumer_key,
            "consumer_key_secret": consumer_key_secret,
            "access_token": access_token,
            "access_token_secret": access_token_secret,
        }
        for k, v in self.credentials.items():
            if not isinstance(v, str) and not isinstance(v, type(None)):
                raise Unauthorized(f"Wrong authorization passed for credential: {k}.")

        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.followed_cache = {}
        self.blocked_cache = {}

    def request(
        self,
        route: Route,
        *,
        headers: RequestModel = {},
        params: RequestModel = {},
        json: RequestModel = {},
        auth: bool = False,
        is_json: bool = True,
        mode: str = None,
    ) -> Union[str, Dict[Any, Any], NoReturn]:
        """Make an HTTP Requests to the api.
        Verion Added: 1.0.0

        This function make an HTTP Request with the given paramaters then return a dictionary in a json format.
        """
        res = getattr(requests, route.method.lower(), None)
        if not res:
            raise TypeError("Method isnt recognizable")

        if auth:
            auth = OauthSession(self.consumer_key, self.consumer_key_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            auth = auth.oauth1

        respond = res(route.url, headers=headers, params=params, json=json, auth=auth)
        check_error(respond)
        res = respond.json()

        if "errors" in res.keys():
            try:
                if res["errors"][0]["detail"].startswith("Could not find"):
                    raise NotFoundError(res["errors"][0]["detail"])

                else:
                    raise PytweetException(res["errors"][0]["detail"])
            except KeyError:
                raise PytweetException(res)

        elif "meta" in res.keys():
            if res["meta"]["result_count"] == 0:
                return 0

        if route.method.upper() == "POST":
            if mode.lower() == "follow":
                self.followed_cache[str(json["target_user_id"])] = res

            elif mode.lower() == "block":
                self.blocked_cache[str(json["target_user_id"])] = res

        elif route.method.upper() == "DELETE":
            if mode.lower() == "unfollow":
                try:
                    self.followed_cache.pop(route.url.split("/")[3])
                except KeyError:
                    pass

            elif mode.lower() == "unblock":
                try:
                    self.blocked_cache.pop(route.url.split("/")[3])
                except KeyError:
                    pass

        if is_json:
            return res
        return respond

    def fetch_user(self, user_id: Union[str, int], http_client, pinned_tweet: bool = False) -> User:
        """Make a Request to optain the user from the given user id.
        Verion Added:1.0.0

        This function return a :class: User object.
        """
        if isinstance(id, str):
            raise ValueError("Id paramater should be an integer!")

        data = self.request(
            Route("GET", "2", f"/users/{user_id}"),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,profile_image_url,protected,public_metrics,url,username,verified,withheld,pinned_tweet_id"
            },
            is_json=True,
        )

        followers = self.request(
            Route("GET", "2", f"/users/{user_id}/followers"),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        following = self.request(
            Route("GET", "2", f"/users/{user_id}/following"),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        data["data"].update(
            {"followers": [User(follower, http_client=self) for follower in followers["data"]] if followers != 0 else 0}
        )
        data["data"].update(
            {
                "following": [User(following, http_client=self) for following in following["data"]]
                if following != 0
                else 0
            }
        )
        return User(data, http_client=http_client)

    def fetch_user_byusername(self, username: str, http_client) -> User:
        """Make a Request to optain the user from their username, A Username usually start with '@' before any letters. If a username named @Jack, then the username argument must be 'Jack'.
        Verion Added:1.0.0

        This function return a :class: User.
        """
        if "@" in username:
            username = username.replace("@", "", 1)

        route = Route("GET", "2", f"/users/by/username/{username}")
        data = self.request(
            route,
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            is_json=True,
        )

        user_payload = self.fetch_user(int(data["data"].get("id")), http_client)
        data["data"].update({"followers": user_payload.followers})
        data["data"].update({"following": user_payload.following})
        return User(data, http_client=http_client)

    def fetch_tweet(self, tweet_id: Union[str, int], http_client) -> Tweet:
        """Fetch a tweet info from the specified id. Return if consumer_key or consumer_key_secret or access_token or access_token_secret is not specified.
        Verion Added:1.0.0

        tweet_id: Union[str, int]
            The tweet id you wish to fetch it.

        http_client
            The http client that make the request.

        This function return a :class: Tweet.
        """
        if not any([v for v in self.credentials.values()]):
            return None

        res = self.request(
            Route("GET", "2", f"/tweets/{tweet_id}"),
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
            Route("GET", "2", f"/tweets/{tweet_id}/retweeted_by"),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        res3 = self.request(
            Route("GET", "2", f"/tweets/{tweet_id}/liking_users"),
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        user_id = res["includes"]["users"][0].get("id")
        user = self.fetch_user(int(user_id), http_client)

        res["includes"]["users"][0].update({"followers": user.followers})
        res["includes"]["users"][0].update({"following": user.following})

        try:
            res2["data"]
            res3["data"]

            res["data"].update({"retweeted_by": [User(user, http_client=http_client) for user in res2["data"]]})
            res["data"].update({"liking_users": [User(user, http_client=http_client) for user in res3["data"]]})
        except (KeyError, TypeError):
            res["data"].update({"retweeted_by": 0})

            res["data"].update({"liking_users": 0})

        return Tweet(res, http_client=self)

    def send_message(self, user_id: Union[str, int], text: str, **kwargs):
        """WARNING: this function isnt finish yet!
        Verion Added:1.1.0

        Make a post Request for sending a message to a Messageable object.
        """
        raise NotImplementedError("This function is not finished yet")

        data = {
            "event": {
                "type": "message_create",
                "message_create": {
                    "target": {"recipient_id": str(user_id)},
                    "message_data": {
                        "text": text,
                    },
                },
            }
        }
        self.request(
            Route("POST", "1.1", "/direct_messages/events/new"),
            headers={"content-type": "application/json"},
            json=data,
            auth=True,
        )

    def delete_message(self, id: int, **kwargs):
        """WARNING: this function isnt finish yet!
        Verion Added:1.1.0

        Make a DELETE Request for deleting a certain message in a Messageable object.
        """
        raise NotImplementedError("This function is not finish yet")

    def post_tweet(self, text: str, **kwargs):
        """WARNING: this function isnt finish yet!
        Verion Added:1.1.0

        Make a POST Request to post a tweet to twitter from the client itself.
        """
        raise NotImplementedError("This function is not finished yet")

    def follow_user(self, user_id: Union[str, int]) -> None:
        """Make a POST Request to follow a Messageable object.
        Verion Added:1.1.0
        Updated: 1.2.0

        user_id: Union[str, int]
            The user's id that you wish to follow, better to make it a string.
        """
        my_id = self.access_token.partition("-")[0]
        self.request(
            Route("POST", "2", f"/users/{my_id}/following"),
            json={"target_user_id": str(user_id)},
            auth=True,
            mode="follow",
        )

    def unfollow_user(self, user_id: Union[str, int]) -> None:
        """Make a DELETE Request to unfollow a Messageable object.
        Verion Added:1.1.0
        Updated: 1.2.0

        user_id: Union[str, int]
            The user's id that you wish to unfollow, better to make it a string.
        """
        my_id = self.access_token.partition("-")[0]
        self.request(
            Route("DELETE", "2", f"/users/{my_id}/following/{user_id}"),
            auth=True,
            mode="unfollow",
        )

    def block_user(self, user_id: Union[str, int]) -> None:
        """Make a POST Request to Block a Messageable object.
        Verion Added:1.2.0

        user_id: Union[str, int]
            The user's id that you wish to block, better to make it a string.
        """
        my_id = self.access_token.partition("-")[0]
        self.request(
            Route("POST", "2", f"/users/{my_id}/blocking"),
            json={"target_user_id": str(user_id)},
            auth=True,
            mode="block",
        )

    def unblock_user(self, user_id: Union[str, int]) -> None:
        """Make a DELETE Request to unblock a Messageable object.
        Verion Added:1.2.0

        user_id: Union[str, int]
            The user's id that you wish to unblock, better to make it a string.
        """
        my_id = self.access_token.partition("-")[0]
        self.request(
            Route("DELETE", "2", f"/users/{my_id}/blocking/{user_id}"),
            auth=True,
            mode="unblock",
        )
