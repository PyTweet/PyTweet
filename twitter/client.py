from .http import HTTPClient, Route
from .user import User

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
    def __init__(self, bearer_token:str):
        super().__init__(bearer_token)

    def get_user_by_id(self, id: int) -> User: #Typehinted to twitter.User
        #super() called the parent class, super().request is the same as HTTPClient.request()
        data=super().request(Route('GET', f"/users/{id}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User.from_dict(data)

    def get_user_by_username(self, username: str) -> User: 
        data=super().request(Route('GET', f"/users/by/username/{username}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User.from_dict(data)