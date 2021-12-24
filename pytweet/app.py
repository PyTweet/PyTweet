from typing import Dict, Any


class ApplicationInfo:
    """Represents an application's info.

    .. versionadded:: 1.5.0
    """
    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        app_id = list(self.__original_payload.get("apps").keys())[0]
        self._payload = self.__original_payload.get("apps", {}).get(app_id, {})

    @property
    def name(self) -> str:
        """:class:`str`: Returns the application's name.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("name")

    @property
    def id(self) -> int:
        """:class:`int`: Returns the application's id.

        .. versionadded:: 1.5.0
        """
        return int(self._payload.get("id"))

    @property
    def url(self) -> str:
        """:class:`str`: Returns the application's url, specifically website url from the application authentication settings.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("url")
