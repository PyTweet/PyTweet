import datetime
from typing import Any, Dict, List, Optional

from .enums import SpaceState
from .utils import time_parse_todt

__all__ = ("Space",)


class Space:
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        try:
            if isinstance(data.get("data"), list):
                self._payload = data.get("data")[0]
            else:
                self._payload = data.get("data")
        except AttributeError:
            return self.original_payload

    def __repr__(self) -> str:
        return "Space(name={0.title} id={0.id} state={0.state})".format(self)

    @property
    def title(self) -> str:
        """:class:`str`: The space's title.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("title")

    @property
    def raw_state(self) -> str:
        """:class:`str`: The raw space's state in  a string.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("state")

    @property
    def state(self) -> SpaceState:
        """:class:`SpaceState`: The type of the space's state.

        .. versionadded:: 1.3.5
        """
        return SpaceState(self.raw_state)

    @property
    def id(self) -> str:
        """:class:`str`: The space's unique id.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("id")

    @property
    def lang(self) -> str:
        """:class:`str`: The space's language.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("lang")

    @property
    def creator_id(self) -> int:
        """:class:`str`: Returns the creator's id.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("creator_id")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the space's created datetime.

        .. versionadded:: 1.3.5
        """
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def hosts_id(self) -> Optional[List[int]]:
        """Optional[List[:class:`int`]]: Returns a list of the hosts id.

        .. versionadded:: 1.3.5
        """
        if self._payload.get("host_ids"):
            return [int(id) for id in self._payload.get("host_ids")]
        return None

    @property
    def invited_users(self) -> Optional[List[int]]:
        """Optional[List[:class:`int`]]: Returns the a list of users id. Usually, users in this list are invited to speak via the Invite user option and have a Speaker role when the Space starts. Returns None if there isn't invited users.

        .. versionadded:: 1.3.5
        """
        if self._payload.get("invited_users"):
            return [int(id) for id in self._payload.get("invited_users")]
        return None

    @property
    def started_at(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: Returns a datetime.datetime object with the space's started time. Only available if the space has started.

        .. versionadded:: 1.3.5
        """
        return time_parse_todt(self._payload.get("started_at")) if self._payload.get("started_at") else None

    @property
    def updated_at(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: Returns a datetime.datetime object with the space's last update to any of this Space's metadata, such as the title or scheduled time. Only available if the space has started.

        .. versionadded:: 1.3.5
        """
        return time_parse_todt(self._payload.get("updated_at"))

    def is_ticketed(self) -> bool:
        """Returns a bool indicate if the space is ticketed.

        Returns
        ---------
        :class:`bool`
            This method returns a bool object.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("is_ticketed")
