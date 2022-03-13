from dataclasses import dataclass
from ..type import ID


@dataclass
class InitiatedVia:
    """Represents an object that stores 'initiated_via' key from direct message event data.

    .. versionadded:: 1.5.0
    """

    tweet_id: ID
    welcome_message_id: ID
