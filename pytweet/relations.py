from typing import Any, Dict

from .enums import RelationsTypeEnum

__all__ = (
    "Relation",
    "RelationFollow",
    "RelationLike",
    "RelationRetweet",
    "RelationHide",
    "RelationUpdate",
    "RelationPin",
    "RelationDelete",
)


class Relation:
    """Represents a base class of all relations classes.

    .. versionadded:: 1.2.5
    """

    __slots__ = "_type"

    def __init__(self, type: int):
        self._type = RelationsTypeEnum(type)

    @property
    def type(self) -> RelationsTypeEnum:
        """:class:`RelationsTypeEnum`: Returns the relation type.

        .. versionadded:: 1.5.0
        """
        return self._type


class RelationFollow(Relation):
    """Represents a follow relation from a follow & unfollow request.

    .. versionadded:: 1.2.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
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


class RelationLike(Relation):
    """Represents a like relation from a like & unlike request.

    .. versionadded:: 1.2.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(2 if self.liked else None)

    def __repr__(self) -> str:
        return "RelationFollow(liked={0.liked})".format(self)

    @property
    def liked(self) -> bool:
        """:class:`bool`: Return True if user liked the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("liked")


class RelationRetweet(Relation):
    """Represents a retweet relation from a retweet & unretweet request.

    .. versionadded:: 1.2.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(3 if self.retweeted else None)

    def __repr__(self) -> str:
        return "RelationRetweet(liked={0.retweeted})".format(self)

    @property
    def retweeted(self) -> bool:
        """:class:`bool`: Return True if user retweeted the tweet else False.

        .. versionadded:: 1.2.0
        """
        return self._payload.get("retweeted")


class RelationHide(Relation):
    """Represents a hide relation from a hide & unhide request.

    .. versionadded:: 1.2.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(4 if self.hidden else None)

    def __repr__(self) -> str:
        return "RelationHide(hidden={0.hidden})".format(self)

    @property
    def hidden(self) -> bool:
        """:class:`bool`: Return True if a tweet is hidden else False

        .. versionadded:: 1.2.0
        """
        return self._payload.get("hidden")


class RelationUpdate(Relation):
    """Represents an update relation that gets return from :meth:`List.update`.

    .. versionadded:: 1.5.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(5 if self.updated else None)

    def __repr__(self) -> str:
        return "RelationUpdate(updated={0.updated})".format(self)

    @property
    def updated(self) -> bool:
        """:class:`bool`: Return True if the list is updated else False.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("updated")


class RelationPin(Relation):
    """Represents a pin relation that gets return from :meth:`List.pin`.

    .. versionadded:: 1.5.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(7 if self.pinned else None)

    def __repr__(self) -> str:
        return "RelationPin(pinned={0.pinned})".format(self)

    @property
    def pinned(self) -> bool:
        """:class:`bool`: Return True if the list is pinned else False.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("pinned")


class RelationDelete(Relation):
    """Represents a delete relation that gets return from:

    * :meth:`List.delete`
    * :meth:`Tweet.delete`

    .. versionadded:: 1.5.0
    """

    __slots__ = ("__original_payload", "_payload")

    def __init__(self, data: Dict[str, Any]):
        self.__original_payload = data
        self._payload = data.get("data")
        super().__init__(8 if self.deleted else None)

    def __repr__(self) -> str:
        return "RelationDelete(deleted={0.deleted})".format(self)

    @property
    def deleted(self) -> bool:
        """:class:`bool`: Return True if the list or tweet is deleted else False.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("deleted")
