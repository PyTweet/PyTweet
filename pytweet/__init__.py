"""
PyTweet
~~~~~~~

PyTweet is a Synchronous python API wrapper for Twitter's API!

:copyright: (c) 2021-present TheFarGG & TheGenocides
:license: MIT, see LICENSE for more details.
"""
import logging
from typing import Literal, NamedTuple

from .app import *
from .attachments import *
from .auth import *
from .client import *
from .entities import *
from .enums import *
from .environment import *
from .errors import *
from .events import *
from .expansions import *
from .http import *
from .message import *
from .metrics import *
from .mixins import *
from .pagination import *
from .parsers import *
from .relations import *
from .space import *
from .stream import *
from .tweet import *
from .user import *
from .utils import *

__title__ = "PyTweet"
__version__ = "1.5.0a5"
__author__ = "TheFarGG & TheGenocides"
__license__ = "MIT"
__copyright__ = "Copyright 2021-present TheFarGG & TheGenocides"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=1, minor=5, micro=0, releaselevel="alpha", serial=5)

logging.getLogger(__name__).addHandler(logging.NullHandler())

assert version_info.releaselevel in ("alpha", "beta", "candidate", "final"), "Invalid release level given."
