from __future__ import annotations

import datetime
from typing import Any, Dict, List, NoReturn, Optional, Union
from .utils import time_parse_todt
from .enums import ButtonStyle
from dataclasses import dataclass

__all__ = ("Media", "PollOptions", "Poll", "QuickReply", "Geo", "CTA")


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

    def __eq__(self, other: Media) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Media object")
        return self.media_key == other.media_key

    def __ne__(self, other: Media) -> Union[bool, NoReturn]:
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

    def __eq__(self, other: PollOptions) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid PollOptions object")
        return self.position == other.position

    def __ne__(self, other: PollOptions) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid PollOptions object")
        return self.position != other.position

    def __lt__(self, other: PollOptions) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("< operation cannot be done with one of the element not a valid PollOptions object")
        return self.position < other.position

    def __gt__(self, other: PollOptions) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("> operation cannot be done with one of the element not a valid PollOptions object")
        return self.position > other.position

    def __le__(self, other: PollOptions) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("<= operation cannot be done with one of the element not a valid PollOptions object")
        return self.position <= other.position

    def __ge__(self, other: PollOptions) -> Union[bool, NoReturn]:
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

    def __init__(self, id: int = None, voting_status: str = None, duration: Union[str, int] = None, end_date: Union[str, int] = None):
        self._id = id
        self._voting_status = voting_status
        self._duration = duration
        self._end_date = end_date
        self._options = []

    def __repr__(self) -> str:
        return "Poll(id={0.id}, voting_status={0.voting_status}, duration={0.duration})".format(
            self
        )

    def __eq__(self, other: Poll) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("== operation cannot be done with one of the element not a valid Poll object")
        return self.id == other.id

    def __ne__(self, other: Poll) -> Union[bool, NoReturn]:
        if not isinstance(other, self):
            raise ValueError("!= operation cannot be done with one of the element not a valid Poll object")
        return self.id != other.id

    def __len__(self) -> int:
        return len(self.options)

    def add_option(self, label: str) -> Poll:
        """Add option to your Poll instance.

        Parameters
        ------------
        position: :class:`int`
            The option's position, maximum position is 4.
        label: :class:`str`
            The option's label.

        .. versionadded 1.3.5
        """

        self._options.append({"label": label})
        return self

    def add_option_FromRequest(self, position: int, label: str, votes: int) -> Poll:
        """Add option from a request, this differ from add_option. This one has votes argument use to specified how many votes that an option has. You should be using the add_option rather then this since this function is only use when a request return votes

        Parameters
        ------------
        position: :class:`int`
            The option's position, maximum position is 4.
        label: :class:`str`
            The option's label.
        votes: :class:`int`
            The option votes


        .. versionadded 1.3.5
        """

        if position > 4:
            return
        self._options.append({"position": position, "label": label, "votes": votes})
        return self

    @property
    def id(self) -> Optional[int]:
        """:class:`int`: Return the poll's unique ID.

        .. versionadded:: 1.1.0
        """
        return int(self._id) if self._id else None

    @property
    def options(self) -> List[PollOptions]:
        """List[:class:`PollOptions`]: Return a list of :class:`PollOptions`.

        .. versionadded:: 1.1.0
        """
        return [PollOptions(option) for option in self._options]

    @property
    def voting_status(self) -> bool:
        """:class:`bool`: Return True if the poll is still open for voting, if its closed it return False.

        .. versionadded:: 1.1.0
        """
        return True if self._voting_status == "open" else False

    @property
    def duration_inSeconds(self) -> int:
        """:class:`int`: Return the poll duration in seconds.

        .. versionadded:: 1.1.0
        """
        return int(self._duration) * 60 if self._duration else None

    @property
    def duration(self) -> int:
        """:class:`int`: Return the poll duration in minutes.

        .. versionadded:: 1.3.5
        """
        return int(self._duration) if self._duration else None

    @property
    def end_date(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Return the end date in datetime.datetime object.

        .. versionadded:: 1.1.0
        """
        return time_parse_todt(self._end_date) if self._end_date else None


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


class Geo:
    """Represent the Geo or location in twitter.
    You can use this as attachment in a tweet or for searching a location

    Parameters
    ------------
    data: Dict[:class:`str`, :class:`Any`]
        The Geo data in a dictionary.

    """

    def __init__(self, data: Dict[str, Any]):
        self._payload = data
        self._bounding_box = self._payload.get("bounding_box")

    def __repr__(self) -> str:
        return "Geo(name:{0.name} fullname:{0.fullname} country:{0.country} country_code:{0.country_code} id:{0.id})".format(
            self
        )

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        """:class:`str`: Returns place's name."""
        return self._payload.get("name")

    @property
    def id(self) -> str:
        """:class:`str`: Returns place's unique id."""
        return self._payload.get("id")

    @property
    def fullname(self) -> str:
        """:class:`str`: Returns place's fullname."""
        return self._payload.get("full_name")

    @property
    def type(self) -> str:
        """:class:`str`: Returns place's type."""
        return self._payload.get("place_type")

    @property
    def country(self) -> str:
        """:class:`str`: Returns the country where the place is in."""
        return self._payload.get("country")

    @property
    def country_code(self) -> str:
        """:class:`str`: Returns the country's code where the location is in."""
        return self._payload.get("country_code")

    @property
    def centroid(self) -> str:
        """:class:`str`: Returns the place's centroid."""
        return self._payload.get("centroid")

    @property
    def bounding_box_type(self) -> str:
        """:class:`str`: Returns the place's bounding box type."""
        if self._bounding_box:
            return self._bounding_box.get("type")
        return None

    @property
    def coordinates(self) -> List[str]:
        """List[:class:`str`]: Returns a list of coordinates where the place's located."""
        if self._bounding_box:
            return self._bounding_box.get("coordinates")
        return None


@dataclass
class Button:
    label: str
    style: ButtonStyle
    url: str


class CTA:
    def __init__(self):
        self._buttons = []
        self._raw_buttons = []

    def add_button(self, label: str, style: ButtonStyle, url: str):
        self._raw_buttons.append({"type": style.value, "label": label, "url": url})
        self._buttons.append(Button(label, style, url))
        return self

    @property
    def buttons(self) -> List[dict]:
        return self._buttons

    @property
    def raw_buttons(self) -> list[Button]:
        return self._raw_buttons
