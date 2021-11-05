"""
PyTweet
~~~~~~~

PyTweet is a Synchronous python API wrapper for Twitter's API!

:copyright: (c) 2021 TheFarGG & TheGenocides
:license: MIT, see LICENSE for more details.
"""
from typing import Literal, NamedTuple
import logging

from .attachments import *
from .auth import *
from .client import *
from .entities import *
from .enums import *
from .errors import *
from .http import *
from .message import *
from .metrics import *
from .relations import *
from .tweet import *
from .user import *
from .utils import *

__title__ = "PyTweet"
__version__ = "1.2.0"
__authors__ = ["TheFarGG", "TheGenocides"]
__license__ = "MIT"
__copyright__ = "Copyright 2021 TheFarGG & TheGenocides"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(major=1, minor=2, micro=0, releaselevel="final", serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())
