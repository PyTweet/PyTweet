from .http import HTTPClient, Route
from .user import User
from typing import Union

class Client(HTTPClient): #Parent Class
    def __init__(self, bearer_token:str):
        super().__init__(bearer_token)

    def get_user(self, id: int) -> User: #Typehinted to twitter.User
        #super() called the parent class, super().request is the same as HTTPClient.request()
        data=super().request(Route('GET', f"/users/{id}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User.from_dict(data)

    def get_user_by_username(self, username: str) -> User: #Typehinted to twitter.User
        #super() called the parent class, super().request is the same as HTTPClient.request()
        data=super().request(Route('GET', f"/users/by/username/{username}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User.from_dict(data)