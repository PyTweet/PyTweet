from typing import Any, Dict

from .enums import RelationsTypeEnum

__all__ = (
    "Relations",
    "RelationFollow",
    "RelationLike",
    "RelationRetweet",
    "RelationHide",
)


class Relations:
    """Represent the base class of(Relations) all relations type.

    .. versionadded:: 1.2.5
    """

    def __init__(self, type: int):
        self.type = RelationsTypeEnum(type)


class RelationFollow(Relations):
    """Represent the follow relation from a follow & unfollow request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data.get("data")
        super().__init__(1 if self.following else 0)

    def __repr__(self) -> str:
        return "RelationFollow(type={0.type} following={0.following} pending={0.pending})".format(self)

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


class RelationLike(Relations):
    """Represent the like relation from a like & unlike request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data.get("data")
        super().__init__(2 if self.liked else None)

    def __repr__(self) -> str:
        return "RelationFollow(liked={0.liked})".format(self)

    @property
    def liked(self) -> bool:
        """:class:`bool`: Return True if user liked the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("liked")


class RelationRetweet(Relations):
    """Represent the retweet relations from a retweet & unretweet request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data.get("data")
        super().__init__(3 if self.retweeted else None)

    def __repr__(self) -> str:
        return "RelationRetweet(liked={0.retweeted})".format(self)

    @property
    def retweeted(self) -> bool:
        """:class:`bool`: Return True if user retweeted the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("retweeted")


class RelationHide(Relations):
    """Represent the hide relations from a hide & unhide request.

    .. versionadded:: 1.2.0
    """

    def __init__(self, data: Dict[str, Any]):
        self.original_payload: Dict[str, Any] = data
        self._payload: Dict[Any, Any] = data.get("data")
        super().__init__(4 if self.hidden else None)

    def __repr__(self) -> str:
        return "RelationHide(hidden={0.hidden})".format(self)

    @property
    def hidden(self) -> bool:
        """:class:`bool`: Return True if a tweet is hidden else False

        .. versionadded:: 1.2.0
        """
        return self._payload.get("hidden")
