from dataclasses import dataclass


@dataclass
class Topic:
    """Represents a space topic.

    .. versionadded:: 1.5.0
    """

    id: int
    name: str
    description: str
