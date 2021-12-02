from enum import Enum


class RelationsTypeEnum(Enum):
    PENDING = 0
    ACCEPT = 1
    LIKED = 2
    RETWEETED = 3
    HIDE = 4
    NULL = None


class MessageTypeEnum(Enum):
    DIRECT_MESSAGE = 0
    MESSAGE_TWEET = 1
    MESSAGE_WELCOME_MESSAGE = 2
    MESSAGE_WELCOME_MESSAGE_RULE = 3
    NULL = None


class MessageEventTypeEnum(Enum):
    MESSAGE_CREATE = "message_create"
    MESSAGE_DELETE = "message_delete"
    NULL = None


class ButtonType(Enum):
    web_url = "web_url"


class SpaceState(Enum):
    live = "live"
    scheduled = "scheduled"


class ReplySetting(Enum):
    everyone = "everyone"
    mention_users = "mentionedUsers"
    following = "following"


class MediaType(Enum):
    photo = "photo"
    video = "video"
    gif = "gif"
