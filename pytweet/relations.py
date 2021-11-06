from typing import Any, Dict
from .enums import RelationsTypeEnum

__all__ = ("RelationFollow", "RelationLike", "RelationRetweet")


class RelationFollow:
    """Represent the follow relation from a follow & unfollow request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data["data"]

    def __repr__(self) -> str:
        return "RelationFollow(type: {0.type} following: {0.following} pending: {0.pending})".format(self)

    @property
    def pending(self) -> bool:
        """:class:`bool`: Check if the relation is pending.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("pending", False)

    @property
    def following(self) -> bool:
        """:class:`bool`: Check if the relation is following.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("following", False)

    @property
    def type(self) -> RelationsTypeEnum:
        """:class:`RelationTypeEnum`: Check what relation type it is.

        .. versionadded:: 1.2.0
        """
        return RelationsTypeEnum(1 if self._payload["following"] else 0)


class RelationLike:
    """Represent the like relation from a like & unlike request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data["data"]

    def __repr__(self) -> str:
        return "RelationFollow(liked: {0.liked})".format(self)

    @property
    def liked(self) -> bool:
        """:class:`bool`: Return True if user liked the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("liked")

    @property
    def type(self) -> RelationsTypeEnum:
        """:class:`RelationTypeEnum`: Check what relation type it is.

        .. versionadded:: 1.2.0
        """
        return RelationsTypeEnum(2 if self.liked else None)


class RelationRetweet:
    """Represent the retweet relations from a retweet & unretweet request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data["data"]

    def __repr__(self) -> str:
        return "RelationRetweet(liked: {0.retweeted})".format(self)

    @property
    def retweeted(self) -> bool:
        """:class:`bool`: Return True if user retweeted the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("retweeted")

    @property
    def type(self) -> RelationsTypeEnum:
        """:class:`RelationTypeEnum`: Check what relation type it is.

        .. versionadded:: 1.2.0
        """
        return RelationsTypeEnum(3 if self.retweeted else None)
