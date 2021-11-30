from __future__ import annotations

import datetime
import mimetypes
import os
from dataclasses import dataclass
from typing import Any, Dict, List, NoReturn, Optional, Union

from .enums import ButtonType
from .utils import time_parse_todt
from .entities import Media

__all__ = ("PollOption", "Poll", "QuickReply", "Geo", "CTA", "Button", "Option", "File")


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
    duration: :class:`int`
        The poll duration in minutes.
    id: Optional[Union[:class:`str`, :class:`int`]]
        The poll's unique ID.
    voting_status: Optional[:class:`str`]
        The poll's voting status.
    end_date: Optional[:class:`str`]
        The poll's end date.


    .. versionadded:: 1.1.0
    """

    def __init__(self, duration: int, **kwargs):
        self._id: Optional[Union[str, int]] = kwargs.get("id", None)
        self._voting_status: Optional[str] = kwargs.get("voting_status", None)
        self._end_date = kwargs.get("end_date", None)
        self._duration = duration
        self._options = []
        self._raw_options = []

    def __repr__(self) -> str:
        return "Poll(id={0.id} voting_status={0.voting_status} duration={0.duration})".format(self)

    def __eq__(self, other: Poll) -> Union[bool, NoReturn]:
        if not isinstance(other, Poll):
            raise ValueError("== operation cannot be done with one of the element not a valid Poll object")
        return self.id == other.id

    def __ne__(self, other: Poll) -> Union[bool, NoReturn]:
        if not isinstance(other, Poll):
            raise ValueError("!= operation cannot be done with one of the element not a valid Poll object")
        return self.id != other.id

    def __len__(self) -> int:
        return len(self.options)

    def add_option(self, *, label: str, **kwargs) -> Poll:
        """Add option to your Poll instance.

        .. note::
            For attaching a poll object you should use the label argument and only label as the api only need labels to make poll.

        Parameters
        ------------
        label: :class:`str`
            The option's label.
        position: :class:`int`
            The option's position.
        votes: :class:`int`
            The option's votes.

        Returns
        ---------
        :class:`Poll`
            This method return your :class:`Poll` instance.


        .. versionadded 1.3.5
        """
        data = {
            "position": kwargs.get("position") or 0,
            "label": label,
            "votes": kwargs.get("votes") or 0,
        }
        self._options.append(PollOption(**data))
        self._raw_options.append(data)
        return self

    @property
    def id(self) -> Optional[int]:
        """Optional[:class:`int`]: Return the poll's unique ID.

        .. versionadded:: 1.1.0
        """
        return int(self._id) if self._id else None

    @property
    def options(self) -> List[PollOption]:
        """List[:class:`PollOption`]: Return a list of :class:`PollOption`.

        .. versionadded:: 1.1.0
        """
        return self._options

    @property
    def raw_options(self) -> List[dict]:
        """List[:class:`dict`]: Return a list of raw poll option.

        .. versionadded:: 1.3.5
        """
        return self._raw_options

    @property
    def voting_status(self) -> bool:
        """:class:`bool`: Return True if the poll is still open for voting, if its closed it return False.

        .. versionadded:: 1.1.0
        """
        return self._voting_status == "open"

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
        self._raw_options: List[dict] = []

    def add_option(
        self, *, label: str, description: Optional[str] = None, metadata: Optional[str] = None
    ) -> QuickReply:
        """Method for adding an option in your quick reply instance.

        Parameters
        ------------
        label: :class:`str`
            The option's label. Label text is returned as the user's message response, Must be less then 36 characters.
        description: :class:`str`
            The option's description. Description text displayed under label text. All options must have this property defined if property is present in any option. Text is auto-wrapped and will display on a max of two lines and supports n for controlling line breaks, Must be less then 72 characters.
        metadata: :class:`str`
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
    def options(self) -> List[Option]:
        """List[:class:`Option`]: Returns a list of pre-made Option objects.

        .. versionadded:: 1.3.5
        """
        return self._options

    @property
    def raw_options(self) -> List[Dict]:
        """List[Dict]: Returns the raw options.

        .. versionadded:: 1.2.0
        """
        return self._raw_options


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
        return "Geo(name={0.name} fullname={0.fullname} country={0.country} country_code={0.country_code} id={0.id})".format(
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


        .. versionadded:: 1.3.5
        """
        self._raw_buttons.append(
            {
                "type": type.value if isinstance(type, ButtonType) else type,
                "label": label,
                "url": url,
            }
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


class CustomProfile:
    """Represent a CustomProfile attachments that allow a Direct Message author to present a different identity than that of the Twitter account being used.

    .. versionadded:: 1.3.5
    """

    def __init__(
        self,
        name: str,
        id: Union[str, int],
        timestamp: Union[str, int],
        media: Dict[str, Any],
    ):
        self._name = name
        self._id = id
        self._timestamp = timestamp
        self._media = Media(media)

    def __repr__(self) -> str:
        return "CustomProfile(name={0.name} id={0.id} media_id={0.media_id})".format(self)

    @property
    def name(self) -> str:
        """:class:`str`: The author's custom name.

        .. versionadded:: 1.3.5
        """
        return self._name

    @property
    def id(self) -> int:
        """:class:`int`: The custom profile unique ID.

        .. versionadded:: 1.3.5
        """
        return int(self._id)

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the CustomProfile created time.

        .. versionadded:: 1.3.5
        """
        timestamp = str(self._timestamp)[:10]
        return datetime.datetime.fromtimestamp(int(timestamp))

    @property
    def media(self) -> Media:
        """:class:`Media`: Returns the media object.

        .. versionadded:: 1.3.5
        """
        return self._media
