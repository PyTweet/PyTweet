from typing import Dict, Any, Union, Type
from .enums import RelationsTypeEnum

Payload: Union[Dict[str, Any], Any] = Any


class RelationFollow:
    """Represent the follow relation from a follow request.
    Verion Added: 1.2.0

    Parameters
    -----------
    data: Payload
        The data of the relations

    Attributes
    -----------

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
    def pending(self) -> bool:
        """bool: Check if the relation is pending."""
        return self._payload.get("pending") if self._payload.get("pending") else False

    @property
    def following(self) -> bool:
        """bool: Check if the relation is following."""
        return self._payload.get("following") if self._payload.get("following") else False

    @property
    def type(self):
        """RelationType: Check what relation type it is."""
        return RelationsTypeEnum(1 if self._payload["following"] else 0)
