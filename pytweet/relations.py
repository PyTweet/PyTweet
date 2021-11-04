from typing import Any, Dict
from .enums import RelationsTypeEnum

__all__ = ("RelationFollow",)


class RelationFollow:
    """Represent the follow relation from a follow request.

    .. describe:: str(x)
        Returns the type.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data["data"]

    def __repr__(self) -> str:
        return "Followed(type: {0.type} following: {0.following} pending: {0.pending})".format(self)

    @property
    def pending(self) -> bool:
        """bool: Check if the relation is pending.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("pending", False)

    @property
    def following(self) -> bool:
        """bool: Check if the relation is following.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("following", False)

    @property
    def type(self) -> RelationsTypeEnum:
        """RelationTypeEnum: Check what relation type it is.
        
        .. versionadded:: 1.2.0
        """
        return RelationsTypeEnum(1 if self._payload["following"] else 0)
