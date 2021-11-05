from enum import Enum


class RelationsTypeEnum(Enum):
    PENDING = 0
    ACCEPT = 1
    LIKED = 2
    RETWEETED = 3
    NULL = None


class MessageTypeEnum(Enum):
    DIRECT_MESSAGE = 0
    MESSAGE_TWEET = 1
    NULL = None


class MessageEventTypeEnum(Enum):
    MESSAGE_CREATE = "message_create"
    MESSAGE_DELETE = "message_delete"
    NULL = None
