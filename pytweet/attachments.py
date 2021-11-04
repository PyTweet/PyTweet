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
    .. versionadded:: 1.1.0

    .. describe:: x == y
        Check if one Media key is equal to another.


    .. describe:: x != y
        Check if one Media key is not equal to another.


    .. describe:: str(x)
        Get the media url.

    Parameters:
    -----------
    data: Dict[str, Any]
        The full data of the media in a dictionary.

    Attributes:
    -----------
    _payload
        Represent the main data of a Media.
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
        """:class:`Optional[str]`: Return the media's type.
        .. versionadded:: 1.1.0
        """
        return self._payload.get("type")

    @property
    def url(self) -> Optional[str]:
        """:class:`Optional[str]`: Return the media's url.
        .. versionadded:: 1.1.0
        """
        return self._payload.get("url")

    @property
    def width(self) -> Optional[int]:
        """:class:`Optional[int]`: the media's width.
        .. versionadded:: 1.1.0
        """
        return self._payload.get("width")

    @property
    def height(self) -> Optional[int]:
        """int: Return the media's height.
        .. versionadded:: 1.1.0
        """
        return self._payload.get("height")

    @property
    def media_key(self) -> Optional[Union[int, str]]:
        """:class:`Optional[Union[int, str]]`: Returns the media's unique key.
        .. versionadded:: 1.1.0
        """
        return self._payload.get("media_key")


class PollOptions:
    """Represent the Poll Options, The minimum option of a poll is 2 and maximum is 4.
    .. versionadded:: 1.1.0

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

    Parameters:
    -----------
    options: Dict[str, Any]
        An dictionary filled with the option's: position, label, and votes.
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
        """:class:`Optional[int]`: The option's position.
        .. versionadded:: 1.1.0
        """
        return self.options.get("position")

    @property
    def label(self) -> Optional[str]:
        """:class:`Optional[int]`: The option's label.
        .. versionadded:: 1.1.0
        """
        return self.options.get("label")

    @property
    def votes(self) -> Optional[int]:
        """:class:`Optional[int]`: The option's votes.
        .. versionadded:: 1.1.0
        """
        return self.options.get("votes")


class Poll:
    """Represent a Poll attachment in a tweet.
    .. versionadded:: 1.1.0

    .. describe:: x == y
        Check if one Poll's id is equal to another.


    .. describe:: x != y
        Check if one Poll's id is not equal to another.


    .. describe:: len(x)
        return how many options in the poll.


    .. describe:: bool(x)
        return True if the poll is open else it return False.

    Parameters:
    -----------
    data: Dict[str, Any]
        The full data of the poll in a dictionary.

    Attributes:
    -----------
    _payload
        The complete data of a Poll keep inside a dictionary.
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
        """int: Return the poll's unique ID.
        .. versionadded:: 1.1.0.
        """
        return self._payload.get("id")

    @property
    def options(self) -> List[PollOptions]:
        """:class:`List[PollOptions]`: Return a list of :class:`PollOptions`.
        .. versionadded:: 1.1.0.
        """
        return [PollOptions(option) for option in self._payload.get("options")]

    @property
    def voting_status(self) -> bool:
        """bool: Return True if the poll is still open for voting, if its closed it return False.
        .. versionadded:: 1.1.0
        """
        return True if self._payload.get("voting_status") == "open" else False

    @property
    def duration(self) -> int:
        """int: Return the poll duration in seconds.
        .. versionadded:: 1.1.0
        """
        return int(self._payload.get("duration_minutes")) * 60

    @property
    def end_date(self) -> datetime.datetime:
        """`datetime.datetime`: Return the end date in datetime.datetime object.
        .. versionadded:: 1.1.0
        """
        return time_parse_todt(self._payload.get("end_datetime"))
