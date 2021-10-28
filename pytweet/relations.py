from typing import Dict, Any
from enum import Enum

class RelationsType(Enum):
    PENDING = 0
    ACCEPT = 1
    NUL = None

Payload: Dict[str, Any] = Any

class RelationFollow():
    """Represent the follow relation from a follow request.
    Version Added: 1.2.0

    Parameters
    ==============
    data: Payload
        The data of the relations

    Attributes
    ==============

    original_payload
        The data paramater.

    _payload
        The data paramater in data key.
    """
    def __init__(self, data: Payload):
        self.original_payload = data
        self._payload = data["data"]

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return "Followed(type: {0.type} following: {0.following} pending: {0.pending})".format(self)

        
    @property
    def pending(self):
        """bool: Check if the relation is pending."""
        return self._payload.get("pending") if self._payload.get("pending") else False

    @property
    def following(self):
        """bool: Check if the relation is following."""
        return self._payload.get("following") if self._payload.get("following") else False

    @property
    def type(self):
        """RelationType: Check what relation type it is."""
        return RelationsType(1 if self._payload['following'] else 0)