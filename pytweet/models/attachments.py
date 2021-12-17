from dataclasses import dataclass
from typing import Union, Optional
from ..enums import ButtonType

@dataclass
class Button:
    """Represent a Button object. Button are attachment that you can attach via :class:`CTA`

    .. versionadded:: 1.3.5
    """

    label: str
    type: Union[ButtonType, str]
    url: str
    tco_url: Optional[str] = None


@dataclass
class Option:
    """Represent an Option object. You can create an Option using :class:`QuickReply.add_option`

    .. versionadded:: 1.3.5
    """

    label: str
    description: str
    metadata: str


@dataclass
class PollOption:
    """Represent an Option for :class:`Poll`

    .. versionadded 1.3.5
    """

    label: str
    position: int = 0
    votes: int = 0