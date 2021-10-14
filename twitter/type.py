from typing import Optional, Dict, str, Any, TYPE_CHECKING

if TYPE_CHECKING: #prevent circular import error
    from .client import Client

class Messageable:
    """
    Represent an object that can send and receive a message through DM.
    """
    def __init__(self, data:Dict[str, Any], **kwargs):
        self._payload = data
        self.provider: Optional[Client] = kwargs.get('provider') or None



