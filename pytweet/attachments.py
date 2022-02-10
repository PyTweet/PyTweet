from __future__ import annotations

import datetime
import io
import os
from typing import Any, Dict, List, NoReturn, Optional, Union, TYPE_CHECKING

from .dataclass import PollOption, Option, Button
from .entities import Media
from .enums import ButtonType
from .utils import time_parse_todt
from .errors import PytweetException
from .constants import LANGUAGES_CODES
from .objects import Comparable

if TYPE_CHECKING:
    from .type import ID

__all__ = ("Poll", "QuickReply", "Geo", "CTA", "File", "SubFile")


def guess_mimetype(byts: bytes):
    if byts[6:10] == b"\x1a\n\x00\x00":
        return "image/png"

    elif byts[6:10] == b"JFIF":
        return "image/jpeg"

    elif byts[6:10] == b"ypis":
        return "video/mp4"

    elif byts.startswith((b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")):
        return "image/gif"

    else:
        return "text/plain"


class Poll(Comparable):
    """Represents a Poll attachment in a tweet.

    .. describe:: x == y

        Check if one Poll's id is equal to another.


    .. describe:: x != y

        Check if one Poll's id is not equal to another.


    .. describe:: len(x)

        returns how many options the poll have.

    Parameters
    ------------
    duration: :class:`int`
        The poll duration in minutes.
    id: Optional[`ID`]
        The poll's unique ID.
    voting_status: Optional[:class:`str`]
        The poll's voting status.
    end_date: Optional[:class:`str`]
        The poll's end date.


    .. versionadded:: 1.1.0
    """

    __slots__ = (
        "_id",
        "_voting_status",
        "_end_date",
        "_duration",
        "_options",
        "_raw_options",
    )

    def __init__(self, *,duration: int, **kwargs):
        self._id: Optional[ID] = kwargs.get("id", None)
        self._voting_status: Optional[str] = kwargs.get("voting_status", None)
        self._end_date = kwargs.get("end_date", None)
        self._duration = duration
        self._options = []
        self._raw_options = []
        super().__init__(self.id)

    def __repr__(self) -> str:
        return "Poll(id={0.id} voting_status={0.voting_status} duration={0.duration})".format(self)

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
    def voting_status(self) -> str:
        """:class:`str`: Returns the current voting status of the poll.

        .. versionadded:: 1.1.0

        .. versionchanged:: 1.3.7
        """
        return self._voting_status

    @property
    def is_open(self) -> bool:
        """:class:`bool`: Return True if the poll is still open for voting, if it's closed it will returns False.

        .. versionadded:: 1.3.7
        """

        return self.voting_status == "open"

    @property
    def is_closed(self) -> bool:
        """:class:`bool`: Returns False if the poll is still open for voting, if it's closed it returns True.

        .. versionadded:: 1.3.7
        """

        return not self.is_open

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
    """Represents a quick_reply attachment in Direct Message.

    Parameters
    ------------
    type: :class:`str`
        The quick_reply's types, it must be and only 'options'


    .. versionadded:: 1.2.0
    """

    __slots__ = ("_type", "_options", "_raw_options")

    def __init__(self, type: str = "options"):
        self._type = type if type == "options" else "options"
        self._options: List[Option] = []
        self._raw_options: List[dict] = []

    def add_option(
        self,
        *,
        label: str,
        description: Optional[str] = None,
        metadata: Optional[str] = None,
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
    def type(self) -> str:
        """:class:`str`: Returns the QuickReply type.

        .. versionadded:: 1.5.0
        """
        return self._type

    @property
    def options(self) -> List[Option]:
        """List[:class:`Option`]: Returns a list of pre-made Option objects.

        .. versionadded:: 1.3.5
        """
        return self._options

    @property
    def raw_options(self) -> List[dict]:
        """List[:class:`dict`]: Returns the raw options.

        .. versionadded:: 1.2.0
        """
        return self._raw_options


class CTA:
    """Represents call-to-action attachment(CTA)
    You can use it in :meth:`User.send` via CTA kwarg. CTA will perform and action whenever a user "call" something, an example of this is buttons.

    .. versionadded:: 1.3.5
    """

    __slots__ = ("_buttons", "_raw_buttons")

    def __init__(self):
        self._buttons = []
        self._raw_buttons = []

    def add_button(
        self,
        *,
        label: str,
        url: str,
        type: Union[ButtonType, str] = ButtonType.web_url,
        tco_url: Optional[str] = None,
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
    """Represents a File attachment for messages.

    Parameters
    ------------
    path: :class:`str`
        The file's path.
    dm_only: :class:`bool`
        Indicates if the file is use in dm only. Default to False.
    alt_text: Optional[:class:`str`]
        The image's alt text, if None specified the image won't have an alt text. Default to None.
    subtitle_language_code: :class:`str`
        The language code should be a BCP47 code (e.g. "en").
    subfile: :class:`SubFile`
        The subtitle's source file. Must be a .srt file with the correct formats.


    .. versionadded:: 1.3.5
    """

    __slots__ = (
        "__path",
        "__media_id",
        "__subfile",
        "__subfiles",
        "_total_bytes",
        "_mimetype",
        "dm_only",
        "alt_text",
    )

    def __init__(
        self,
        path: str,
        *,
        dm_only: bool = False,
        alt_text: Optional[str] = None,
        subfile: Optional[SubFile] = None,
        subfiles: Optional[List[SubFile]] = None,
    ):
        self.__path = path
        self.__media_id = None
        self.__subfile = subfile
        self.__subfiles = subfiles
        self._total_bytes = os.path.getsize(path) if isinstance(path, str) else os.path.getsize(path.name)
        self._mimetype = (
            guess_mimetype(open(path, "rb").read()) if isinstance(path, str) else guess_mimetype(path.read())
        )
        self.dm_only = dm_only
        self.alt_text = alt_text

    def __repr__(self) -> str:
        return "File(filename={0.filename})".format(self)

    @property
    def path(self) -> str:
        """:class:`str`: Returns the file's path.

        .. versionadded:: 1.3.5
        """
        return self.__path

    @property
    def media_id(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the file's media id. Returns None if the file was never uploaded.

        .. versionadded:: 1.5.0
        """
        return int(self.__media_id) if self.__media_id else self.__media_id

    @property
    def subfile_media_id(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the file's subtitle file's media id. Returns None if the subfile was never uploaded.

        .. versionadded:: 1.5.0
        """
        return int(self.subfile.media_id) if self.subfile.media_id else self.subfile.media_id

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
        return self.path.name if isinstance(self.path, io.IOBase) else os.path.basename(self.path)

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
        mimetype = self._mimetype
        if mimetype in ("image/jpeg", "image/png"):
            return startpoint + "IMAGE" if not self.dm_only else "dm_image"
        elif mimetype == "image/gif":
            return startpoint + "GIF" if not self.dm_only else "dm_gif"
        elif mimetype == "video/mp4":
            return startpoint + "VIDEO" if not self.dm_only else "dm_video"

    @property
    def subfile(self) -> Optional[SubFile]:
        """Optional[:class:`SubFile`]: Returns the file's subfile.

        .. versionadded:: 1.5.0
        """
        return self.__subfile

    @property
    def subfiles(self) -> Optional[List[SubFile]]:
        """Optional[List[:class:`SubFile`]]: Returns a list of the file's subfiles.

        .. versionadded:: 1.5.0
        """
        return self.__subfiles


class SubFile(File):
    """Represents a subtitle File for :class:`File`. You can attach one subfile in :class:`File` via subfile arguments. This method inherits :class:`File`. Always remembers that twitter only supports srt extension file with the correct timestamps.


    .. versionadded:: 1.5.0
    """

    __slots__ = ("_language_code", "_language")

    def __init__(self, path: str, *, language_code: Optional[str]):
        self._language_code = language_code
        if self.language_code:
            fullname = LANGUAGES_CODES.get(language_code)
            if fullname:
                self._language = fullname
            else:
                raise PytweetException("Wrong language codes passed! Must be a BCP47 code (e.g. 'en')")
        super().__init__(path)

    def __repr__(self) -> str:
        return "SubFile(filename={0.filename} language={0.language} language_code={0.language_code})".format(self)

    @property
    def filename(self) -> str:
        """:class:`str`: Returns the SubFile's filename.

        .. versionadded:: 1.5.0
        """
        return self.path.name if isinstance(self.path, io.IOBase) else os.path.basename(self.path)

    @property
    def path(self) -> str:
        """:class:`str`: Returns the SubFile's path.

        .. versionadded:: 1.3.5
        """
        return self._File__path

    @property
    def language(self) -> str:
        """:class:`str`: Returns the SubFile's language.

        .. versionadded:: 1.5.0
        """
        return self._language

    @property
    def language_code(self) -> str:
        """:class:`str`: Returns the SubFile's language code.

        .. versionadded:: 1.5.0
        """
        return self._language_code

    @property
    def media_id(self) -> Optional[int]:
        """Optional[:class:`int`]: Returns the SubFile's media id. Returns None if the file was never uploaded.

        .. versionadded:: 1.5.0
        """
        return int(self._File__media_id) if self._File__media_id else self._File__media_id

    @property
    def total_bytes(self) -> int:
        """:class:`int`: Returns an integer value that represents the size of the specified path in bytes.

        .. versionadded:: 1.5.0
        """
        return self._total_bytes

    @property
    def mimetype(self) -> str:
        """:class:`str`: Returns the subfile's media category. This always returns 'text/srt'

        .. versionadded:: 1.5.0
        """
        return "text/srt"

    @property
    def media_category(self) -> str:
        """:class:`str`: Returns the subfile's media category. This always returns 'Subtitles'.

        .. versionadded:: 1.5.0
        """
        return "Subtitles"

class Geo(Comparable):
    """Represents the Geo location in twitter.
    You can use this as attachment in a tweet or for searching a location


    .. versionadded:: 1.3.5
    """

    __slots__ = ("_payload", "__bounding_box")

    def __init__(self, data: Dict[str, Any]):
        self._payload = data
        self.__bounding_box = self._payload.get("bounding_box")
        super().__init__(self.id)

    def __repr__(self) -> str:
        return "Geo(name={0.name} fullname={0.fullname} country={0.country} country_code={0.country_code} id={0.id})".format(
            self
        )

    @property
    def name(self) -> str:
        """:class:`str`: Returns the geo's name.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("name")

    @property
    def id(self) -> str:
        """:class:`str`: Returns the geo's unique id.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("id")

    @property
    def fullname(self) -> str:
        """:class:`str`: Returns the geo's fullname.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("full_name")

    @property
    def type(self) -> str:
        """:class:`str`: Returns the geo's type.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("place_type")

    @property
    def country(self) -> str:
        """:class:`str`: Returns the country where the geo is in.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("country")

    @property
    def country_code(self) -> str:
        """:class:`str`: Returns the country's code where the geo is in.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("country_code")

    @property
    def centroid(self) -> str:
        """:class:`str`: Returns the geo's centroid.

        .. versionadded:: 1.3.5
        """
        return self._payload.get("centroid")

    @property
    def bounding_box_type(self) -> str:
        """:class:`str`: Returns the geo's bounding box type.

        .. versionadded:: 1.3.5
        """
        if self.__bounding_box:
            return self.__bounding_box.get("type")
        return None

    @property
    def coordinates(self) -> List[str]:
        """List[:class:`str`]: Returns a list of coordinates where the geo's located.

        .. versionadded:: 1.3.5
        """
        if self.__bounding_box:
            return self.__bounding_box.get("coordinates")
        return None

class CustomProfile(Comparable):
    """Represents a CustomProfile attachments that allow a Direct Message author to present a different identity than that of the Twitter account being used.

    .. versionadded:: 1.3.5
    """

    __slots__ = ("_name", "_id", "_timestamp", "_media")

    def __init__(
        self,
        name: str,
        id: ID,
        timestamp: ID,
        media: Dict[str, Any],
    ):
        self._name = name
        self._id = id
        self._timestamp = timestamp
        self._media = Media(media)
        super().__init__(self.id)

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
        return datetime.datetime.fromtimestamp(int(self._timestamp) / 1000)

    @property
    def media(self) -> Media:
        """:class:`Media`: Returns the media object.

        .. versionadded:: 1.3.5
        """
        return self._media
