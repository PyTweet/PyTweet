import datetime
from typing import Dict, Any

class UserFollowActionEvent:
    """Represents a follow action event.
    
    """
    def __init__(self, data: Dict[str, Any], *, http_client: object):
        self.original_payload = data
        self._payload = data.get("follow_events")[0]

    @property
    def followed_at(self):
        timestamp = str(self._payload.get("created_timestamp"))[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def target(self):
        return self._payload.get("target")

    @property
    def source(self):
        return self._payload.get("source")

    @property
    def author(self):
        return self.source

class UserUnfollowActionEvent(UserFollowActionEvent):
    """Represents an unfollow action event. This inherits :class:`UserFollowActionEvent`.
    
    """
    pass