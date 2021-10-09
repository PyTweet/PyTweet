import requests
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
    """
    def __init__(self, bearer_token:str, *, consumer_key=Optional[str], consumer_key_secret=Optional[str], access_token=Optional[str], access_token_secret=Optional[str]):
        super().__init__(bearer_token, consumer_key=consumer_key, consumer_key_secret=consumer_key_secret, access_token=access_token, access_token_secret=access_token_secret)

    def get_user(self, id: int) -> User: 
        data=self.request(
            Route('GET', "2", f"/users/{id}"), 
            payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"},
            is_json=True
        ) 
        
        followers=self.request(
            Route("GET", "2", f"/users/{id}/followers"), 
            payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}
        )
        
        users=[User(follower) for follower in followers]
        data.update({'followers': users})
        return User(data)
 
        
    #Put Followers id here later...
    def get_user_by_username(self, username: str) -> User: 
        route=Route("GET", "2", f"/users/by/username/{username}")
        data=self.request(
            route,
            payload={"Authorization": f"Bearer {self.bearer_token}"}, 
            params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, 
            is_json=True
        ) 
        
        followers=self.request(
            Route("GET", "2", f"/users/{data['id']}/followers"), 
            payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}
        )
        users=[User(follower) for follower in followers]
        data.update({"followers": users})
        return User(data)

    def get_tweet(self, id: int): 
        params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld", "expansions": "author_id,referenced_tweets.id.author_id"}
        
        route=Route("GET", "2", f"/tweets/{id}")

        method=getattr(route, 'method', None)
        if not method:
            raise TypeError("Method isnt recognizable")

        res=getattr(requests, method.lower(), None)
        if not res:
            raise TypeError("Method isnt recognizable")

        res=res(route.url, params=params, headers={"Authorization": f"Bearer {self.bearer_token}"})
        self.is_error(res)
       
        json_response = res.json()
        user_id=json_response["includes"]["users"][0].get('id')

        user=self.get_user(user_id)
        json_response["includes"]["users"][0].update({"followers": user.followers})

        return Tweet(json_response)