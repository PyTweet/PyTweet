import datetime
from typing import Any, Dict, Optional

from .user import User

class DirectMessageTypingEvent:
    """Represents a typing event object for `on_typing` event. This object contains the event information that twitter posts through the webhook url. 
    
    .. versionadded:: 1.5.0
    """
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the action's created timestamp.

        .. versionadded:: 1.5.0
        """
        return datetime.datetime.fromtimestamp(int(self._payload.get("created_at")[:7]))

    @property
    def recipient(self) -> User:
        """:class:`User`: Returns the user where the :meth:`DirectMessageTypingEvent.sender` trigger the typing animation.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("target", {}).get("recipient")

    @property
    def sender(self) -> User:
        """:class:`User`: Returns the user that trigger this event.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("target", {}).get("sender", None)

    @property
    def typer(self) -> User:
        """:class:`User`: An alias to :meth:`DirectMessageTypingEvent.sender`.

        .. versionadded:: 1.5.0
        """
        return self.sender

class DirectMessageReadEvent:
    """Represents a direct message read event object for `on_direct_message_read` event. This object contains information that twitter posts through the webhook url.
    
    .. versionadded:: 1.5.0
    """
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the action's created timestamp.

        .. versionadded:: 1.5.0
        """
        return datetime.datetime.fromtimestamp(int(self._payload.get("created_at")[:7]))

    @property
    def recipient(self) -> Optional[User]:
        """:class:`User`: Returns the user where the :meth:`DirectMessageTypingEvent.sender` trigger this event.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("target", {}).get("recipient", None)

    @property
    def sender(self) -> Optional[User]:
        """:class:`User`: Returns the user that trigger this action.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("target", {}).get("sender", None)

    @property
    def reader(self) -> Optional[User]:
        """:class:`User`: An alias to :meth:`DirectMessageReadEvent.sender`.

        .. versionadded:: 1.5.0
        """
        return self.sender

    @property
    def last_read_event_id(self) -> int:
        """:class:`int`: Returns the last message's event id that got read.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("last_read_event_id")

class UserFollowActionEvent:
    """Represents a follow action event. This object contains information that twitter posts through the webhook url.
    
    .. versionadded:: 1.5.0
    """
    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data.get("follow_events")[0]

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the action's created timestamp.
        
        .. versionadded:: 1.5.0
        """
        timestamp = str(self._payload.get("created_timestamp"))[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def target(self) -> User:
        """:class:`User`: Returns the user who got followed/unfollowed by the source.
        
        .. versionadded:: 1.5.0
        """
        return self._payload.get("target")

    @property
    def source(self) -> User:
        """:class:`User`: Returns a user object that trigger this event.
        
        .. versionadded:: 1.5.0
        """
        return self._payload.get("source")

    @property
    def author(self):
        """:class:`User`: An alias to source.
        
        .. versionadded:: 1.5.0
        """
        return self.source


class UserUnfollowActionEvent(UserFollowActionEvent):
    """Represents an unfollow action event, This inherits :class:`UserFollowActionEvent`. This object contains information that twitter posts through the webhook url.
    
    .. versionadded:: 1.5.0
    """
    pass