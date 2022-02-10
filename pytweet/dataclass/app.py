from dataclasses import dataclass
from ..type import ID


@dataclass
class ApplicationInfo:
    """Represents an application's info.

    .. versionadded:: 1.5.0
    """

    name: str
    id: ID
    url: str
