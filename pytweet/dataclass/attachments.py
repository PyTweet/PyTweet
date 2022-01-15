from dataclasses import dataclass
from typing import Union, Optional
from ..enums import ButtonType

@dataclass
class Option:
    """Represents an Option object for :class:`QuickReply`. You can add an Option using :meth:`QuickReply.add_option`.

    .. versionadded:: 1.3.5
    """
    label: str
    description: str
    metadata: str


@dataclass
class PollOption:
    """Represents an Option for :class:`Poll`. You can add an option to a poll using :meth:`Poll.add_option`.

    .. versionadded:: 1.3.5
    """
    label: str
    position: int = 0
    votes: int = 0


@dataclass
class Button:
    """Represents a Button object. Button is an attachment that you can attach via :meth:`CTA.add_button`.

    .. versionadded:: 1.3.5
    """
    label: str
    type: Union[ButtonType, str]
    url: str
    tco_url: Optional[str] = None