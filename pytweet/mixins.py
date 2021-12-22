import logging
from typing import Any, Dict, Callable

_log = logging.getLogger(__name__)

__all__ = (
    "EventMixin",
)

class EventMixin:
    events: Dict[str, Callable] = {}

    def dispatch(self, event_name: str, *args: Any, **kwargs: Any) -> Any:
        event = self.events.get(event_name)
        if not event:
            return None

        _log.debug(f"Dispatching Event: on_{event_name}")
        return event(*args, **kwargs)
