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
from typing import Dict, Any, Optional
from .errors import Unauthorized, NotFoundError, UnfinishFunctionError, TooManyRequests


def is_error(respond: requests.models.Response):
    code = respond.status_code
    if code == 401:
        raise Unauthorized("Invalid credentials passed!")

    elif code == 429:
        raise TooManyRequests(respond.text)


class Route:
    def __init__(self, method: str, version: str, path: str):
        self.method: str = method
        self.path: str = path
        self.base_url = f"https://api.twitter.com/{version}"
        self.url: str = self.base_url + self.path


class HTTPClient:
    """
    Represent the http/base client for :class: Client!
    This http/base client have methods for making requests to twitter's api!

    Parameters:
    ===================
    bearer_token: str -> The Bearer Token of the app. The most important one, because this make most of the requests for twitter's api version 2.

    consumer_key: Optional[str] -> The Consumer Key of the app.

    consumer_key_secret: Optional[str] -> The Consumer Key Secret of the app.

    access_token: Optional[str] -> The Access Token of the app.

    access_token_secret: Optional[str] -> The Access Token Secret of the app.

    Functions:
    ====================
    def request() -> make a requests with the given paramaters.

    WARNING: These following functions isnt finish yet!
    def send_message() -> Send a message to Messageable object.

    def delete_message() -> Delete a certain message in Messageable object.

    def post_tweet() -> Post a tweet directly to twitter through your client.

    def follow_user() -> Follow a Messageable object
    
    def unfollow_user() -> Unfollow a Messageable object.
    """

    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: Optional[str],
        consumer_key_secret: Optional[str],
        access_token: Optional[str],
        access_token_secret: Optional[str],
    ):  
        credentials={"bearer_token": bearer_token, "consumer_key": consumer_key, "consumer_key_secret": consumer_key_secret, "access_token": access_token, "access_token_secret": access_token_secret}
        for k, v in credentials.items():
            if isinstance(v, int):
                raise Unauthorized(f"Wrong authorization passed for credential: {k}.")
                
        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def request(
        self,
        route: Route,
        *,
        headers: Dict[str, Any],
        params: Dict[str, str] = {},
        is_json: bool = True,
    ):
        res = getattr(requests, route.method.lower(), None)
        if not res:
            raise TypeError("Method isnt recognizable")

        respond = res(route.url, headers=headers, params=params)
        is_error(respond)
        res = respond.json()

        if "errors" in res.keys():
            raise NotFoundError(res["errors"][0]["detail"])

        elif "meta" in res.keys():
            if res["meta"]["result_count"] == 0:
                return 0

        if is_json:
            return res['data']
        return respond

    def send_message(self, text: str, **kwargs):
        raise UnfinishFunctionError("This function is not finish yet")

    def delete_message(self, id: int, **kwargs):
        raise UnfinishFunctionError("This function is not finish yet")

    def post_tweet(self, text: str, **kwargs):
        raise UnfinishFunctionError("This function is not finish yet")

    def follow_user(self, id:int, **kwargs):
        raise UnfinishFunctionError("This function is not finish yet")

    def unfollow_user(self, id:int, **kwargs):
        raise UnfinishFunctionError("This function is not finish yet")