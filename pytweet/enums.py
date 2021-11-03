from enum import Enum


class RelationsTypeEnum(Enum):
    PENDING = 0
    ACCEPT = 1
    NUL = None

class MessageTypeEnum(Enum):
    DIRECT_MESSAGE = 0
    MESSAGE_TWEET = 1
    NULL = None

class MessageEventsTypeEnum(Enum):
    MESSAGE_CREATE = "message_create"
    MESSAGE_DELETE = "message_delete"
    NULL = None
