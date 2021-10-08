from .user import User
from typing import Optional, Dict, Any

class Tweet:
    def __init__(self, client, data: Dict[str, Any]):
        self.client = client
        print(data)
        self._payload = data['data']
    
    @property
    def author(self) -> Optional[User]:
        return self.client.get_user_by_id(int(self._payload.get("id")))

class ReTweet(Tweet):
    ...