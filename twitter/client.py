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
    def __init__(self, bearer_token:str):
        super().__init__(bearer_token)

    def get_user_by_id(self, id: int) -> User: 
        data=super().request(Route('GET', f"/users/{id}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User(data)

    def get_user_by_username(self, username: str) -> User: 
        data=super().request(Route('GET', f"/users/by/username/{username}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"}, is_json=True) 
        return User(data)

    def get_tweet(self, id: int) -> Tweet:
        data=super().request(Route('GET', f"/tweets/{id}"), payload={"Authorization": f"Bearer {self.bearer_token}"}, params={"tweet.fields":"attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld"}, is_json=True) 
        return Tweet(self, data)