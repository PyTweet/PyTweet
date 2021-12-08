import datetime
from typing import Any, Dict

from .user import User


class UserFollowActionEvent:
    """Represents a follow action event."""

    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data.get("follow_events")[0]

    @property
    def followed_at(self) -> datetime.datetime:
        timestamp = str(self._payload.get("created_timestamp"))[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def target(self) -> User:
        return self._payload.get("target")

    @property
    def source(self) -> User:
        return self._payload.get("source")

    @property
    def author(self):
        return self.source


class UserUnfollowActionEvent(UserFollowActionEvent):
    """Represents an unfollow action event. This inherits :class:`UserFollowActionEvent`."""

    @property
    def unfollowed_at(self):
        timestamp = str(self._payload.get("created_timestamp"))[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))


class DirectMessageTypingEvent:
    """Represents a typing event in direct message."""

    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def recipient(self) -> User:
        """:class:`User`: Returns the user where the :meth:`DirectMessageTypingEvent.typer` trigger the typing animation.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("target", {}).get("recipient")

    @property
    def typer(self) -> User:
        """:class:`User`: Returns the user that trigger the typing animation in the :meth:`DirectMessageTypingEvent.recipient`'s dm.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("target", {}).get("sender", None)

    @property
    def sender(self) -> User:
        """:class:`User`: An alias to :meth:`DirectMessageTypingEvent.typer`.

        .. versionadded:: 1.5.0
        """
        return self.typer

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the time when the user trigger a typing animation.

        .. versionadded:: 1.5.0
        """
        return datetime.datetime.fromtimestamp(int(self._payload.get("created_at")[:7]))
