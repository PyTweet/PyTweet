import requests
import json
from typing import Dict, Any, Optional
from .errors import Unauthorized, NotFoundError 

class Route:
    def __init__(self, method:str, version: str, path:str):
        url=f"https://api.twitter.com/{version}"
        self.method: str = method
        self.path: str = path
        self.url: str = url + self.path

class HTTPClient:
    """
    Represent the http/base client for :class: Client! 
    This http/base client will be the parent class for :class: Client.

    Parameters:
    ===================
    bearer_token: str -> The Bearer Token of the app. The most important one, Make sure to put the right credentials

    consumer_key: Optional[str] -> The Consumer Key of the app.

    consumer_key_secret: Optional[str] -> The Consumer Key Secret of the app.

    access_token: Optional[str] -> The Access Token of the app.

    access_token_secret: Optional[str] -> The Access Token Secret of the app.

    Functions:
    ====================
    def request() -> make a requests with the given paramaters.

    def is_error() -> Check if a requests return error code: 401
    """
    def __init__(self, bearer_token:str, *, consumer_key=Optional[str], consumer_key_secret=Optional[str], access_token=Optional[str], access_token_secret=Optional[str]):
        self.bearer_token = bearer_token
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_key_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret 
        
    
    def request(self, route:Route, *,payload:Dict[str, Any], params:Dict[str, str], is_json: bool = True) -> Any:
        method=getattr(route, 'method', None)
        if not method:
            raise TypeError("Method isnt recognizable")

        res=getattr(requests, method.lower(), None)
        if not res:
            raise TypeError("Method isnt recognizable")
        
        respond=res(route.url, headers=payload, params=params)
        
        self.is_error(respond)
        
        if 'data' not in respond.text:
            error=json.loads(respond.text)["errors"][0]
            try:
                error["detail"]
            except KeyError:
                raise Exception(error)
            else:
                raise NotFoundError(error["detail"])

            
        if is_json:
            return respond.json()['data']
        return respond
    
    def bearer_oauth(self, r): #Taken from sample code
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r 

    def is_error(self, respond: requests.models.Response):
        code=respond.status_code
        if code == 401:
            raise Unauthorized("Invalid bearer_token passed!")