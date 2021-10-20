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
from typing import Union
from .http import HTTPClient, Route, is_error
from .user import User
from .tweet import Tweet

class Client:
    """
    Represent a client that connected to Twitter!
    This client will interact with other through twitter's api version 2!

    Parameters:
    ===================
    bearer_token: str -> The Bearer Token of the app. The most important one, Make sure to put the right credentials

    consumer_key: Optional[str] -> The Consumer Key of the app.

    consumer_key_secret: Optional[str] -> The Consumer Key Secret of the app.

    access_token: Optional[str] -> The Access Token of the app.

    access_token_secret: Optional[str] -> The Access Token Secret of the app.

    Functions:
    ====================
    def get_user() -> Gets the user info through their id.

    def get_user_by_username() -> Gets the user info through their username.

    def get_tweet() -> Gets a tweet info through the tweet's id.

    def tweet() -> Post a tweet directly to twitter. 

    def run() -> Stream in real-time, roughly a 1% sample of all public Tweets.
    """

    def __init__(
        self,
        bearer_token: str,
        *,
        consumer_key: Union[str, None] = None,
        consumer_key_secret: Union[str, None] = None,
        access_token: Union[str, None] = None,
        access_token_secret: Union[str, None] = None,
    ):
        self.http = HTTPClient(
            bearer_token,
            consumer_key=consumer_key,
            consumer_key_secret=consumer_key_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def __repr__(self) -> str:
        return "<Client: Credentials=SECRET>"

    def get_user(self, id: int) -> User:
        if isinstance(id, str):
            raise ValueError("Id paramater should be an integer!")

        data = self.http.request(
            Route("GET", "2", f"/users/{id}"),
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            is_json=True,
        )

        followers = self.http.request(
            Route("GET", "2", f"/users/{id}/followers"),
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        following = self.http.request(
            Route("GET", "2", f"/users/{id}/following"),
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
        )

        data.update(
            {
                "followers": [User(follower) for follower in followers]
                if followers != 0
                else 0
            }
        )
        data.update(
            {
                "following": [User(following) for following in following]
                if following != 0
                else 0
            }
        )
        return User(data, http_client=self.http)

    def get_user_by_username(self, username: str) -> User:
        if "@" in username:
            username = username.replace("@", "", 1)

        route = Route("GET", "2", f"/users/by/username/{username}")
        data = self.http.request(
            route,
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
            params={
                "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            is_json=True,
        )

        user_payload = self.get_user(int(data.get("id")))
        data.update({"followers": user_payload.followers})
        data.update({"following": user_payload.following})
        return User(data, http_client=self.http)

    def get_tweet(self, id: int) -> Tweet:
        r = Route("GET", "2", f"/tweets/{id}")
        res = requests.get(
            r.url,
            params={
                "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,geo,entities,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld",
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
                "expansions": "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id",
                "media.fields": "duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width",
                "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
                "poll.fields": "duration_minutes,end_datetime,id,options,voting_status"
            },
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
        )
        is_error(res)

        r = Route("GET", "2", f"/tweets/{id}/retweeted_by")
        res2 = requests.get(
            r.url,
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
        )

        is_error(res2)

        r = Route("GET", "2", f"/tweets/{id}/liking_users")
        res3 = requests.get(
            r.url,
            params={
                "user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
            },
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
        )
        is_error(res3)

        json_response = res.json()
        user_id = json_response["includes"]["users"][0].get("id")
        user = self.get_user(int(user_id))
        
        json_response["includes"]["users"][0].update({"followers": user.followers})
        json_response["includes"]["users"][0].update({"following": user.following})
        
        try:
            res2.json()["data"]
            res3.json()["data"]

            json_response["data"].update(
                {
                    "retweeted_by": [
                        User(user, http_client=self.http) for user in res2.json()["data"]
                    ]
                }
            )
            json_response["data"].update(
                {
                    "liking_users": [
                        User(user, http_client=self.http) for user in res3.json()["data"]
                    ]
                }
            )
        except KeyError:
            json_response["data"].update(
                {
                    "retweeted_by": 0
                }
            )

            json_response["data"].update(
                {
                    "liking_users": 0
                }
            )

        return Tweet(json_response)

    def tweet(self, text:str, **kwargs):
        self.http.post_tweet(text, kwargs)

    def run(self):
        self.http.request(
            Route("GET", "2", "/tweets/sample/stream"),
            headers={"Authorization": f"Bearer {self.http.bearer_token}"},
        )