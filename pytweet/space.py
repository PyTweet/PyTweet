import datetime
from typing import Dict, Any, List
from .utils import time_parse_todt 

class Space:
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data.get("data")

    def __repr__(self) -> str:
        return "Space(name:{0.title} state:{0.state} id:{0.id})".format(self)

    @property
    def title(self) -> str:
        """:class:`str`: The space's title."""
        return self._payload.get("title")

    @property
    def state(self) -> str:
        """:class:`str`: The space's state."""
        return self._payload.get("state")

    @property
    def id(self) -> int:
        """:class:`int`: The space's id."""
        return int(self._payload.get("id"))

    @property
    def lang(self) -> str:
        """:class:`str`: The space's language."""
        return self._payload.get("lang")

    @property
    def creator_id(self) -> int:
        """:class:`str`: Returns the creator's id."""
        return self._payload.get("creator_id")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the space's created datetime."""
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def hosts(self) -> List[int]:
        """List[:class:`int`]: Returns a list of the hosts id."""
        return [int(id) for id in self._payload.get("host_ids")]
    
    @property
    def invited_users(self) -> List[int]:
        """List[:class:`int`]: Returns the a list of users id. Usually, users in this list are invited to speak via the Invite user option and have a Speaker role when the Space starts."""
        return [int(id) for id in self._payload.get("invited_users")]

    @property
    def started_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the space's started time. Only available if the space has started."""
        return time_parse_todt(self._payload.get("started_at"))

    @property
    def updated_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the space's last update to any of this Space's metadata, such as the title or scheduled time. Only available if the space has started."""
        return time_parse_todt(self._payload.get("started_at"))
    
    def is_ticketed(self) -> bool:
        """:class:`bool`: Returns a bool indicate if the space is ticketed."""
        return self._payload.get("is_ticketed")