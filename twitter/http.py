import requests
import json
from typing import Dict, Any, Optional
from .errors import Unauthorized, UserNotFound

class Route:
    def __init__(self, method:str, path:str):
        self.method: str = method
        self.path: str = path
        url="https://api.twitter.com/2"
        self.url: str = url + self.path
    
class HTTPClient:
    def __init__(self, bearer_token:str, *, api_key=Optional[str], api_key_secret=Optional[str], access_token=Optional[str], access_token_secret=Optional[str]):
        self.bearer_token = bearer_token
        

    def request(self, route:Route, *,payload:Dict[str, Any], params:Dict[str, str]={"user.fields":"id,name,username"}, is_json: bool = True) -> Any:
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
            raise UserNotFound(error["detail"])

        if is_json:
            return json.loads(respond.text)['data']
        
        return respond
    
    def is_error(self, respond: requests.models.Response):
        code=respond.status_code
        if code == 401:
            raise Unauthorized("Invalid api-key passed!")
            
        
