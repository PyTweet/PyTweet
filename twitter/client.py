from typing import Optional
from .http import HTTPClient, Route
from .user import User
from .tweet import Tweet

class Client(HTTPClient): #Parent Class
    """
    Represent a client that connected to Twitter! 
    This client will interact with other through twitter's api version 2!

    Parameters:
    ===================
    bearer_token: :class: str

    api_key: Optional[str]

    api_key_secret: Optional[str]

    access_token: Optional[str]

    access_token_secret: Optional[str]

    Functions:
    ====================
    get_user_by_id -> Gets the user info by using their id.

    get_user_by_username -> Gets the user info by using their username.
    """
    def __init__(self, bearer_token:str, *, consumer_key=Optional[str], consumer_key_secret=Optional[str], access_token=Optional[str], access_token_secret=Optional[str]):
        super().__init__(bearer_token, consumer_key=consumer_key, consumer_key_secret=consumer_key_secret, access_token=access_token, access_token_secret=access_token_secret)

    def get_user_by_id(self, id: int) -> User: 
        data=super().request(Route('GET', f"/users/{id}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User(data)

    def get_user_by_username(self, username: str) -> User: 
        data=super().request(Route('GET', f"/users/by/username/{username}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User(data)

    def get_tweet(self, id: int):
        tup=self.oauth.requests_oauth()
        params={"expansions": "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id", "user.fields":"created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}
        session=self.oauth.session(
            tup[0],
            client_secret=tup[1],
            resource_owner_key=tup[2],
            resource_owner_secret=tup[3],
        )

        response = session.get(
            f"https://api.twitter.com/2/tweets/{id}", params=params
        )

        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format   (response.status_code, response.text)
            )
        json_response = response.json()
        return Tweet(json_response)