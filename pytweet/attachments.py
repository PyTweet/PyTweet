from __future__ import annotations

import datetime
from typing import Any, Dict, List, NoReturn, Optional, TypeVar, Union
from .utils import time_parse_todt

M = TypeVar("M", bound="Media")
PO = TypeVar("PO", bound="PollOptions")
P = TypeVar("P", bound="Poll")

__all__ = (
    "Media",
    "PollOptions",
    "Poll",
)


class Media:
    """Represent a Media attachment in a tweet.

    .. describe:: x == y
        Check if one Media key is equal to another.


    .. describe:: x != y
        Check if one Media key is not equal to another.


    .. describe:: str(x)
        Get the media url.

    .. versionadded:: 1.1.0
    """

    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    def __repr__(self) -> str:
        return "Media(type={0.type} url={0.url} width={0.width} height={0.height} media_key={0.media_key})".format(self)

    def __str__(self) -> str:
        return self.url

    def __eq__(self, other: M) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Media object")
        return self.media_key == other.media_key

    def __ne__(self, other: M) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid Media object")
        return self.media_key != other.media_key

    @property
    def type(self) -> Optional[str]:
        """Optional[:class:`str`]: Return the media's type.

        .. versionadded:: 1.1.0
        """
        return self._payload.get("type")

    @property
    def url(self) -> Optional[str]:
        """Optional[:class:`str`]: Return the media's url.

        .. versionadded:: 1.1.0
        """
        return self._payload.get("url")

    @property
    def width(self) -> Optional[int]:
        """Optional[:class:`int`]: the media's width.

        .. versionadded:: 1.1.0
        """
        return self._payload.get("width")

    @property
    def height(self) -> Optional[int]:
        """Optional[:class:`int`]: Return the media's height.

        .. versionadded:: 1.1.0
        """
        return self._payload.get("height")

    @property
    def media_key(self) -> Optional[Union[int, str]]:
        """Optional[Union[:class:`int`, :class:`str`]]: Returns the media's unique key.

        .. versionadded:: 1.1.0
        """
        return self._payload.get("media_key")


class PollOptions:
    """Represent the Poll Options, The minimum options in a poll is 2 and maximum is 4.

    .. describe:: x == y
        Check if one PollOption position is equal to another.


    .. describe:: x != y
        Check if one PollOption position is not equal to another.


    .. describe:: x > y
        Check if one PollOption position is higher then to another.


    .. describe:: x < y
        Check if one PollOption position is less then to another.


    .. describe:: x >= y
        Check if one PollOption position is higher then equal to another.


    .. describe:: x <= y
        Check if one PollOption position is less then equal to another.

    .. versionadded:: 1.1.0
    """

    def __init__(self, options: Dict[str, Any]):
        self.options = options

    def __repr__(self) -> str:
        return "PollOption({0.position} {0.label} {0.votes})".format(self)

    def __eq__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid PollOptions object")
        return self.position == other.position

    def __ne__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid PollOptions object")
        return self.position != other.position

    def __lt__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("< operation cannot be done with one of the element not a valid PollOptions object")
        return self.position < other.position

    def __gt__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("> operation cannot be done with one of the element not a valid PollOptions object")
        return self.position > other.position

    def __le__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("<= operation cannot be done with one of the element not a valid PollOptions object")
        return self.position <= other.position

    def __ge__(self, other: PO) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError(">= operation cannot be done with one of the element not a valid PollOptions object")
        return self.position >= other.position

    @property
    def position(self) -> Optional[int]:
        """Optional[:class:`int`]: The option's position.

        .. versionadded:: 1.1.0
        """
        return self.options.get("position")

    @property
    def label(self) -> Optional[str]:
        """Optional[:class:`str`]: The option's label.

        .. versionadded:: 1.1.0
        """
        return self.options.get("label")

    @property
    def votes(self) -> Optional[int]:
        """Optional[:class:`int`]: The option's votes.

        .. versionadded:: 1.1.0
        """
        return self.options.get("votes", 0)


class Poll:
    """Represent a Poll attachment in a tweet.

    .. describe:: x == y
        Check if one Poll's id is equal to another.


    .. describe:: x != y
        Check if one Poll's id is not equal to another.


    .. describe:: len(x)
        return how many options in the poll.


    .. describe:: bool(x)
        return True if the poll is open else it return False.

    .. versionadded:: 1.1.0
    """

    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    def __repr__(self) -> str:
        return "Poll(id={0.id}, voting_status={0.voting_status}, duration={0.duration}, end_date={0.end_date} options={0.options})".format(
            self
        )

    def __eq__(self, other: P) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Poll object")
        return self.id == other.id

    def __ne__(self, other: P) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid Poll object")
        return self.id != other.id

    def __len__(self) -> int:
        return len(self.options)

    def __bool__(self) -> bool:
        return self.voting_status

    @property
    def id(self) -> Optional[int]:
        """:class:`int`: Return the poll's unique ID.

        .. versionadded:: 1.1.0
        """
        return int(self._payload.get("id"))

    @property
    def options(self) -> List[PollOptions]:
        """List[:class:`PollOptions`]: Return a list of :class:`PollOptions`.

        .. versionadded:: 1.1.0
        """
        return [PollOptions(option) for option in self._payload.get("options")]

    @property
    def voting_status(self) -> bool:
        """:class:`bool`: Return True if the poll is still open for voting, if its closed it return False.

        .. versionadded:: 1.1.0
        """
        return True if self._payload.get("voting_status") == "open" else False

    @property
    def duration(self) -> int:
        """:class:`int`: Return the poll duration in seconds.

        .. versionadded:: 1.1.0
        """
        return int(self._payload.get("duration_minutes")) * 60

    @property
    def end_date(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Return the end date in datetime.datetime object.

        .. versionadded:: 1.1.0
        """
        return time_parse_todt(self._payload.get("end_datetime"))


class QuickReply:
    """Represent a quick_reply attachment in Direct Message.

    Parameters
    ------------
    type: :class:`str`
        The quick_reply's types, it must be and only 'options'

    Attributes
    ------------
    options: List[Any, Any]
        The QuickReply's options. An option must have a label, description and metadata, Maximum options is 20.
    items: :class:`int`
        Return how many options in your quick_reply object.

    .. versionadded:: 1.2.0
    """

    def __init__(self, type: str = "options"):
        self.type = type if type == "options" else "options"
        self.options: List[Any, Any] = []
        self.items: int = len(self.options)

    def add_option(self, *, label: str, description: str = None, metadata: str = None) -> QuickReply:
        """:class:`QuickReply`: Method for adding an option in your quick reply instance.

        Parameters
        ------------
        label: str
            The option's label. Label text is returned as the user's message response, Must be less then 36 characters.
        description: str
            The option's description. Description text displayed under label text. All options must have this property defined if property is present in any option. Text is auto-wrapped and will display on a max of two lines and supports n for controlling line breaks, Must be less then 72 characters.
        metadata: str
            The option's metadata. Metadata that will be sent back in the webhook request, must be less then 1000 characters.

        Returns
        ---------
        :class:`QuickReply`
            Returns the :class:`QuickReply` object.

        .. versionadded:: 1.2.0
        """

        self.options.append({"label": label, "description": description, "metadata": metadata})

        return self
