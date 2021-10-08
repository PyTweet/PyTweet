from .user import User
from typing import Optional, Dict, Any

class Tweet:
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data['data']
    
    @property
    def author(self) -> Optional[User]:
        return User(self.original_payload["includes"]["users"][0])

