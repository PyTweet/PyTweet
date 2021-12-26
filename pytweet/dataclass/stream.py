from dataclasses import dataclass
from typing import Optional
from ..type import ID 


@dataclass
class StreamRule:
    """Represents a stream rule.

    .. versionadded:: 1.3.5
    """

    value: str
    tag: Optional[str] = None
    id: Optional[ID] = None
