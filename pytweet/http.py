from typing import Any, Dict, NoReturn, Optional, Union

import requests

from .auth import OauthSession
from .errors import (
    Forbidden,
    NotFoundError,
    PytweetException,
    TooManyRequests,
    Unauthorized,
)
from .relations import RelationFollow
from .tweet import Tweet
from .user import User
from .message import DirectMessage

def check_error(respond: requests.models.Response) -> NoReturn:
    code = respond.status_code
    if code == 200:
        res= respond.json()
        if "errors" in res.keys():
            try:
                if res["errors"][0]["detail"].startswith("Could not find"):
                    raise NotFoundError(res["errors"][0]["detail"])

                else:
                    raise PytweetException(res["errors"][0]["detail"])
            except KeyError:
                raise PytweetException(res)

    elif code == 401:
        raise Unauthorized("Invalid credentials passed!")

    elif code == 403:
        raise Forbidden("Forbidden to interact with that User!")

    elif code == 429:
        raise TooManyRequests(respond.text)


RequestModel: Union[Dict[str, Any], Any] = Any


class Route:
    def __init__(self, method: str, version: str, path: str):
        self.method: str = method
        self.path: str = path
        self.base_url = f"https://api.twitter.com/{version}"
        self.url: str = self.base_url + self.path


class HTTPClient:
    """Represent the http/base client for :class:`Client` !
    This http/base client have methods for making requests to twitter's api!
    version Added: 1.0.0

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

    Attributes:
    -----------
    credentials
        The credentials in a dictionary.

    followed_cache
        The followed cache, will be update when the client follow someone.

    blocked_cache
        The blocked cache, will be update when the client block someone.

    Exceptions Raise:
    ----------------
    pytweet.errors.Unauthorized:
        Raise when the api return code: 401. This usually because you passed invalid credentials.
    """

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
        for k, v in self.credentials.items():
            if not isinstance(v, str) and not isinstance(v, type(None)):
                raise Unauthorized(f"Wrong authorization passed for credential: {k}.")

        self.bearer_token: Optional[str] = bearer_token
        self.consumer_key: Optional[str] = consumer_key
        self.consumer_key_secret: Optional[str] = consumer_key_secret
        self.access_token: Optional[str] = access_token
        self.access_token_secret: Optional[str] = access_token_secret
        self.followed_cache: Dict[Any, Any] = {}
        self.blocked_cache: Dict[Any, Any] = {}

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
        version Added: 1.0.0

        Parameters:
        -----------
        route: Route
            Represent the Route class, this will be use to configure the endpoint, method, and version of the api.

        headers: RequestModel
            Represent the http request headers, it usually filled with your bearer token. If this isnt specified then the default argument will be an empty dictionary. Later in the code it will update and gets your bearer token.

        params: RequestModel
            Represent the http request paramaters, If this isnt specified then the default argument will be an empty dictionary.

        json: RequestModel
            Represent the Json data. This usually use for request with POST method.

        auth: bool
           Represent a toggle, if auth is True then the request will be handler with Oauth1 particularly OauthSession.

        is_json: bool
            Represent a toggle, if its True then the return will be in a json format else its going to be a requests.models.Response object. Default to True.

        mode: str
            This mode argument usually use in a POST request, its going to specified whats the request action, then it log into a cache. For example, if a mode is 'follow' then it log the request to a follow cache.

        Exceptions Raise:
        ----------------
        pytweet.errors.Unauthorized:
            Raise when the api return code: 401. This usually because you passed invalid credentials

        pytweet.errors.Forbidden:
            Raise when the api return code: 403. Theres alot of reason why, This usually happen when the client cannot do the request due to twitter's limitation e.g trying to follow someone that you blocked etc.

        pytweet.errors.TooManyRequests:
            Raise when the api return code: 429. This usually happen when you made too much request thus the api ratelimit you. The ratelimit will ware off in a couple of minutes.

        This function make an HTTP Request with the given paramaters then return a dictionary in a json format.
        """
        if headers == {}:
            headers = {"Authorization": f"Bearer {self.bearer_token}"}

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

        if "meta" in res.keys():
            if res["meta"]["result_count"] == 0:
                return []

        if is_json:
            return res

        return respond

    

    def fetch_user(self, user_id: Union[str, int], *,http_client=None) -> User:
        """Make a Request to optain the user from the given user id.
        version Added:1.0.0

        Parameters:
        -----------
        user_id: Union[str, int]
            Represent the user id that you wish to get info to, If you dont have it you may use `fetch_user_byusername` because it only required the user's username.

        http_client:
            Represent the HTTP Client that make the request, this will be use for interaction between the client and the user. If this isnt a class or a subclass of HTTPClient, the current HTTPClient instance will be a default one.

        Exceptions Raise:
        ----------------
        pytweet.errors.NotFoundError:
            Raise when the api cant find a user with that id.

        ValueError:
            Raise when user_id is not an int and is not a string of digits.

        This function return a :class:`User` object.
        """
        try:
            int(user_id)
        except ValueError:
            raise ValueError("user_id have to be an int, or a string of digits!")

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
            {
                "followers": [
                    User(follower, http_client=http_client) for follower in followers["data"]
                ]
                if followers != 0
                else 0
            }
        )
        data["data"].update(
            {
                "following": [
                    User(following, http_client=http_client) for following in following["data"]
                ]
                if following != 0
                else 0
            }
        )

        return User(data, http_client=http_client)

    def fetch_user_byusername(self, username: str, *,http_client=None) -> User:
        """Make a Request to optain the user from their username.
        Version Added: 1.0.0

        Parameters:
        -----------
        username: str
            Represent the user's username. A Username usually start with '@' before any letters. If a username named @Jack, then the username argument must be 'Jack'.

        http_client:
            Represent the HTTP Client that make the request, this will be use for interaction between the client and the user. If this isnt a class or a subclass of HTTPClient, the current HTTPClient instance will be a default one.

        Exceptions Raise:
        ----------------
        pytweet.errors.NotFoundError:
            Raise when the api cant find a user with that username.

        This function return a :class:`User` object.
        """
        if "@" in username:
            username = username.replace("@", "", 1)

        route: Route = Route("GET", "2", f"/users/by/username/{username}")
        data = self.request(
            route,
            headers={"Authorization": f"Bearer {self.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            is_json=True,
        )

        user_payload = self.fetch_user(int(data["data"].get("id")), http_client=http_client)
        data["data"].update({"followers": user_payload.followers})
        data["data"].update({"following": user_payload.following})

        return User(data, http_client=http_client)

    def fetch_tweet(self, tweet_id: Union[str, int], *,http_client=None) -> Tweet:
        """Fetch a tweet info from the specified id. Return if consumer_key or consumer_key_secret or access_token or access_token_secret is not specified.
        version Added:1.0.0

        Parameters:
        -----------
        tweet_id: Union[str, int]
            Represent the tweet's id that you wish .

        http_client
            Represent the HTTP Client that make the request, this will be use for interaction between the client and the user. If this isnt a class or a subclass of HTTPClient, the current HTTPClient instance will be a default one.

        Exceptions Raise:
        ----------------
        pytweet.errors.NotFoundError:
            Raise when the api cant find a tweet with that id.

        This function return a :class:`Tweet`.
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
        user = self.fetch_user(int(user_id), http_client=http_client)

        res["includes"]["users"][0].update({"followers": user.followers})
        res["includes"]["users"][0].update({"following": user.following})

        try:

            res2["data"]
            res3["data"]

            res["data"].update(
                {
                    "retweeted_by": [
                        User(user, http_client=http_client) for user in res2["data"]
                    ]
                }
            )
            res["data"].update(
                {
                    "liking_users": [
                        User(user, http_client=http_client) for user in res3["data"]
                    ]
                }
            )

        except (KeyError, TypeError):
            res["data"].update({"retweeted_by": 0})
            res["data"].update({"liking_users": 0})

        return Tweet(res, http_client=http_client)

    def send_message(self, user_id: Union[str, int], text: str, **kwargs):
        """Make a post Request for sending a message to a Messageable object.
        version Added: 1.1.0
        Updated: 1.2.0

        Parameters:
        -----------
        user_id: Union[str, int]
            The user id that you wish to send message to.

        text: str
            The text that will be send to that user.

        http_client
            Represent the HTTP Client that make the request, this will be use for interaction between the client and the user. If this isnt a class or a subclass of HTTPClient, the current HTTPClient instance will be a default one.

        This function return a :class: `DirrectMessage` object.
        """
        http_client=kwargs.get('http_client', None)
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
        res=self.request(
            Route("POST", "1.1", "/direct_messages/events/new.json"),
            json=data,
            auth=True,
        )
        return DirectMessage(res, http_client=http_client if http_client else self)

    def delete_message(self, id: int, **kwargs):
        """WARNING: this function isnt finish yet!
        version Added:1.1.0

        Make a DELETE Request for deleting a certain message in a Messageable object.
        """
        raise NotImplementedError("This function is not finish yet")

    def post_tweet(self, text: str, **kwargs):
        """WARNING: this function isnt finish yet!
        version Added:1.1.0

        Make a POST Request to post a tweet to twitter from the client itself.
        """
        raise NotImplementedError("This function is not finished yet")

    def follow_user(self, user_id: Union[str, int]) -> None:
        """Make a POST Request to follow a Messageable object.
        version Added:1.1.0
        Updated: 1.2.0

        Paramaters:
        -----------

        user_id: Union[str, int]
            The user's id that you wish to follow, better to make it a string.

        This function return a :class: `RelationFollow` object.
        """
        my_id = self.access_token.partition("-")[0]
        res=self.request(
            Route("POST", "2", f"/users/{my_id}/following"),
            json={"target_user_id": str(user_id)},
            auth=True,
            mode="follow",
        )
        return RelationFollow(res)

    def unfollow_user(self, user_id: Union[str, int]) -> None:
        """Make a DELETE Request to unfollow a Messageable object.
        version Added:1.1.0
        Updated: 1.2.0

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to unfollow, better to make it a string.

        This function return a :class: `RelationFollow` object.
        """
        my_id = self.access_token.partition("-")[0]
        res=self.request(
            Route("DELETE", "2", f"/users/{my_id}/following/{user_id}"),
            auth=True,
            mode="unfollow",
        )
        return RelationFollow(res)

    def block_user(self, user_id: Union[str, int]) -> None:
        """Make a POST Request to Block a Messageable object.
        version Added: 1.2.0

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to block, better to make it a string.

        This function return a :class: `RelationBlock` object.
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
        version Added:1.2.0

        Parameters:
        -----------
        user_id: Union[str, int]
            The user's id that you wish to unblock, better to make it a string.

        This function return a :class: `RelationBlock` object.
        """
        my_id = self.access_token.partition("-")[0]
        self.request(
            Route("DELETE", "2", f"/users/{my_id}/blocking/{user_id}"),
            auth=True,
            mode="unblock",
        )
        
