from __future__ import annotations

import datetime
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, List, NoReturn, Optional, Union

from .enums import ButtonType
from .utils import time_parse_todt

__all__ = ("PollOptions", "Poll", "QuickReply", "Geo", "CTA", "Button", "Option")


@dataclass
class Button:
    label: str
    type: Union[ButtonType, str]
    url: str
    tco_url: Optional[str] = None


@dataclass
class Option:
    label: str
    description: str
    metadata: str

class File:
    """Represent a File attachment for messages.
    
    Parameters
    ------------
    path_to_filename: :class:`str`
        The file's path.
    dm_only: :class:`bool`
        Indicates if the file is use in dm only. Default to False.
    """
    def __init__(self, path_to_filename: str, *, dm_only: bool = False):
        self.__path = path_to_filename
        self._total_bytes = os.path.getsize(self.path)
        self._mimetype = mimetypes.MimeTypes().guess_type(self.path)[0]
        self.dm_only = dm_only

    def __repr__(self) -> str:
        return "File(filename={0.filename})".format(self)

    @property
    def path(self) -> str:
        """:class:`str`: Returns the file's path.
        
        .. versionadded:: 1.3.5
        """
        return self.__path

    @property
    def mimetype(self) -> str:
        """:class:`str`: Returns the file's mimetype.
        
        .. versionadded:: 1.3.5
        """
        return self._mimetype
    
    @property
    def filename(self) -> str:
        """:class:`str`: Returns the file's basename.
        
        .. versionadded:: 1.3.5
        """
        return os.path.basename(self.path)

    @property
    def total_bytes(self) -> int:
        """:class:`int`: Returns an integer value that represents the size of the specified path in bytes.
        
        .. versionadded:: 1.3.5
        """
        return self._total_bytes

    @property
    def media_category(self) -> str:
        """:class:`str`: Returns the file's media category. e.g If its more tweet messages it can be TWEET_IMAGE if its in direct messages it will be dm_image.
        
        .. versionadded:: 1.3.5
        """
        startpoint = "TWEET_"
        if "image" in self.mimetype and not "gif" in self.mimetype:
            return startpoint + "IMAGE" if not self.dm_only else "dm_image"
        elif "gif" in self.mimetype:
            return startpoint + "GIF" if not self.dm_only else "dm_gif"
        elif "video" in self.mimetype:
            return startpoint + "VIDEO" if not self.dm_only else "dm_video"

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
        return "PollOption(position={0.position} label={0.label} votes={0.votes})".format(self)

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
    def votes(self) -> int:
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
        returns how many options in the poll.

    Parameters
    ------------
    id: Optional[:class:`int`]
        The poll's unique ID.
    voting_status: Optional[Union[:class:`str`, :class:`int`]]
        The poll's voting status.
    duration: Optional[Union[:class:`str`, :class:`int`]]
        The poll duration in minutes.
    end_date: Optional[Union[:class:`str`, :class:`int`]]
        The poll's end date.


    .. versionadded:: 1.1.0
    """

    def __init__(
        self,
        id: Optional[int] = None,
        voting_status: Optional[str] = None,
        duration: Optional[Union[str, int]] = 20,
        end_date: Optional[Union[str, int]] = None,
    ):
        self._id = id
        self._voting_status = voting_status
        self._duration = duration
        self._end_date = end_date
        self._options = []

    def __repr__(self) -> str:
        return "Poll(id={0.id} voting_status={0.voting_status} duration={0.duration})".format(self)

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
        label: :class:`str`
            The option's label.

        Returns
        ---------
        :class:`Poll`
            This method return your :class:`Poll` instance.

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

        Returns
        ---------
        :class:`Poll`
            This method return your :class:`Poll` instance.


        .. versionadded 1.3.5
        """

        if position > 4:
            return
        self._options.append({"position": position, "label": label, "votes": votes})
        return self

    @property
    def id(self) -> Optional[int]:
        """Optional[:class:`int`]: Return the poll's unique ID.

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
    def end_date(self) -> Optional[datetime.datetime]:
        """Optional[:class:`datetime.datetime`]: Return the end date in datetime.datetime object.

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

    .. versionadded:: 1.2.0
    """

    def __init__(self, type: str = "options"):
        self.type = type if type == "options" else "options"
        self._options: List[Option] = []
        self._raw_options: List[Dict] = []

    def add_option(
        self, *, label: str, description: Optional[str] = None, metadata: Optional[str] = None
    ) -> QuickReply:
        """Method for adding an option in your quick reply instance.

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
            This method return your :class:`QuickReply` instance.


        .. versionadded:: 1.2.0
        """

        self._raw_options.append({"label": label, "description": description, "metadata": metadata})
        self._options.append(Option(label=label, description=description, metadata=metadata))

        return self

    @property
    def raw_options(self) -> List[Dict]:
        """List[Dict]: Returns the raw options.
        
        .. versionadded:: 1.2.0
        """
        return self._raw_options

    @property
    def options(self) -> List[Option]:
        """List[:class:`Option`]: Returns a list of pre-made Option objects.
        
        .. versionadded:: 1.3.5
        """
        return self._options


class Geo:
    """Represent the Geo location in twitter.
    You can use this as attachment in a tweet or for searching a location

    Parameters
    ------------
    data: Dict[:class:`str`, :class:`Any`]
        The Geo data in a dictionary.


    .. versionadded:: 1.3.5
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
        """:class:`str`: Returns place's name.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("name")

    @property
    def id(self) -> str:
        """:class:`str`: Returns place's unique id.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("id")

    @property
    def fullname(self) -> str:
        """:class:`str`: Returns place's fullname.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("full_name")

    @property
    def type(self) -> str:
        """:class:`str`: Returns place's type.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("place_type")

    @property
    def country(self) -> str:
        """:class:`str`: Returns the country where the place is in.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("country")

    @property
    def country_code(self) -> str:
        """:class:`str`: Returns the country's code where the location is in.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("country_code")

    @property
    def centroid(self) -> str:
        """:class:`str`: Returns the place's centroid.
        
        .. versionadded:: 1.3.5
        """
        return self._payload.get("centroid")

    @property
    def bounding_box_type(self) -> str:
        """:class:`str`: Returns the place's bounding box type.
        
        .. versionadded:: 1.3.5
        """
        if self._bounding_box:
            return self._bounding_box.get("type")
        return None

    @property
    def coordinates(self) -> List[str]:
        """List[:class:`str`]: Returns a list of coordinates where the place's located.
        
        .. versionadded:: 1.3.5
        """
        if self._bounding_box:
            return self._bounding_box.get("coordinates")
        return None


class CTA:
    """Represent call-to-action attachment(CTA)
    You can use this in a post_tweet method via direct_message_deep_link kwarg or use it in direct message via CTA kwarg. CTA will perform and action whenever a user "call" something, an example of this is buttons.

    .. versionadded:: 1.3.5
    """

    def __init__(self):
        self._buttons = []
        self._raw_buttons = []

    def add_button(
        self, *, label: str, url: str, type: Union[ButtonType, str] = ButtonType.web_url, tco_url: Optional[str] = None
    ) -> CTA:
        """Add a button in your CTA instance.

        Parameters
        ------------
        label: :class:`str`
            The button's label, will be shown in the main text.
        url: :class:`str`
            A url that specified where to take you when you click the button, e.g you can take a user to someone's dm, a tweet, etc.
        type: :class:`ButtonType`
            The button's type, For now twitter only use web_url, if none specified the default type is ButtonType.web_url.
        tco_url: Optional[:class:`str`]
            The url in tco style.

        Returns
        ---------
        :class:`CTA`
            Returns your :class:`CTA` instance.
        """
        self._raw_buttons.append(
            {"type": type.value if isinstance(type, ButtonType) else type, "label": label, "url": url}
        )

        self._buttons.append(Button(label, type, url, tco_url))
        return self

    @property
    def buttons(self) -> List[Button]:
        """List[:class:`Button`]: Returns a list of pre-made buttons object.
        
        .. versionadded:: 1.3.5
        """
        return self._buttons

    @property
    def raw_buttons(self) -> List[Dict]:
        """List[dict]: Returns the list of dictionaries filled with raw buttons.
        
        .. versionadded:: 1.3.5
        """
        return self._raw_buttons
