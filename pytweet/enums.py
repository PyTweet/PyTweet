from enum import Enum

class RelationsTypeEnum(Enum):
    PENDING = 0
    ACCEPT = 1
    NUL = None

class MessageTypeEnum(Enum):
    DIRECT_MESSAGE = 0
    MESSAGE_TWEET = 1