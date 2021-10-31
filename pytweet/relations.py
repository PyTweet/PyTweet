from typing import Any, Dict

from .enums import RelationsTypeEnum


class RelationFollow:
    """Represent the follow relation from a follow request.
    Version Added: 1.2.0

    .. describe:: str(x)
        Returns the type.


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

    def __init__(self, data: Dict[str, Any]):
        self.original_payload = data
        self._payload = data["data"]

    def __str__(self) -> str:
        return self.type

    def __repr__(self) -> str:
        return "Followed(type: {0.type} following: {0.following} pending: {0.pending})".format(
            self
        )

    @property
    def pending(self) -> bool:
        """bool: Check if the relation is pending."""
        return self._payload.get("pending", False)

    @property
    def following(self) -> bool:
        """bool: Check if the relation is following."""
        return self._payload.get("following", False)

    @property
    def type(self) -> RelationsTypeEnum:
        """RelationTypeEnum: Check what relation type it is."""
        return RelationsTypeEnum(1 if self._payload["following"] else 0)
