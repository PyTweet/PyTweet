from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from .type import ID, Payload
from .utils import time_parse_todt
from .paginations import UserPagination, TweetPagination
from .constants import TWEET_EXPANSION, USER_FIELD, TWEET_FIELD
from .relations import RelationUpdate, RelationDelete, RelationPin
from .objects import Comparable

if TYPE_CHECKING:
    from .http import HTTPClient
    from .user import User

__all__ = ("List",)


class List(Comparable):
    """Represents a Twitter List object

    A Twitter List is a curated group of accounts. Create one or subscribe to a list created by others to streamline your timeline.

    .. versionadded:: 1.5.0
    """

    __slots__ = ("__original_payload", "_payload", "http_client")

    def __init__(self, data: Payload, *, http_client: HTTPClient):
        self.__original_payload = data
        self._payload = self.__original_payload.get("data") or self.__original_payload
        self.http_client = http_client
        super().__init__(self.id)

    def __repr__(self) -> str:
        return "List(name={0.name} id={0.id} description={0.description} owner={0.owner!r})".format(self)

    @property
    def name(self) -> str:
        """`str`: Returns the list's name

        .. versionadded:: 1.5.0
        """
        return self._payload.get("name")

    @property
    def id(self) -> ID:
        """`ID`: Returns the list's id

        .. versionadded:: 1.5.0
        """
        return int(self._payload.get("id"))

    @property
    def description(self) -> Optional[str]:
        """Optional[:class:`str`]: Returns the list's description or None if the list doesn't have one.

        .. versionadded:: 1.5.0
        """
        description = self._payload.get("description")
        return description if description else None

    @property
    def owner(self) -> Optional[User]:
        """:class:`User`: Returns the list's owner in a user object

        .. versionadded:: 1.5.0
        """
        from .user import User  # Avoid circular import error

        user_data = self.__original_payload.get("includes").get("users")
        if user_data:
            return User(user_data[0], http_client=self.http_client)
        return None

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the list created creation time.

        .. versionadded:: 1.5.0
        """
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def private(self) -> bool:
        """:class:`bool`: Returns True if the list is private else False.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("private")

    @property
    def member_count(self) -> int:
        """:class:`int`: Returns then number of users who are a member of the List.

        .. versionadded:: 1.5.0
        """
        return int(self._payload.get("member_count"))

    @property
    def follower_count(self) -> int:
        """:class:`int`: Returns the number of users who follow the List.

        .. versionadded:: 1.5.0
        """
        return int(self._payload.get("follower_count"))

    @property
    def url(self) -> str:
        """:class:`str`: Returns the list's url.

        .. versionadded:: 1.5.0
        """
        return f"https://twitter.com/i/lists/{self.id}"

    def fetch_tweets(self) -> TweetPagination:
        """Fetches tweets from the list.


        .. versionadded:: 1.5.0
        """
        params = {
            "expansions": TWEET_EXPANSION,
            "user.fields": USER_FIELD,
            "tweet.fields": TWEET_FIELD,
        }

        res = self.http_client.request(
            "GET",
            "2",
            f"/lists/{self.id}/tweets",
            params=params,
        )

        if not res:
            return []

        return TweetPagination(
            res,
            endpoint_request=f"/lists/{self.id}/tweets",
            http_client=self.http_client,
            params=params,
        )

    def update(
        self, *, name: Optional[str] = None, description: Optional[str] = None, private: Optional[bool] = None
    ) -> Optional[RelationUpdate]:
        """Updates the list.

        Paramaters
        -----------
        name: :class:`str`
            The name of the List you wish to update.
        description: :class:`str`
            Description of the List.
        private: :class:`bool`
            Determine whether the List should be private, default to None.


        .. versionadded:: 1.5.0
        """
        return self.http_client.update_list(self.id, name=name, description=description, private=private)

    def delete(self) -> Optional[RelationDelete]:
        """Deletes the list.

        Returns
        ---------
        Optional[:class:`RelationDelete`]
            This method returns a :class:`RelationDelete` object.


        .. versionadded:: 1.5.0
        """
        res = self.http_client.request("DELETE", "2", f"/lists/{self.id}", auth=True)
        return RelationDelete(res)

    def pin(self) -> Optional[RelationPin]:
        """Pins the list.

        Returns
        ---------
        Optional[:class:`RelationPin`]
            This method returns a :class:`RelationPin` object.


        .. versionadded:: 1.5.0
        """
        res = self.http_client.request(
            "POST", "2", f"/users/{self.owner.id}/pinned_lists", auth=True, json={"list_id": str(self.id)}
        )

        return RelationPin(res)

    def unpin(self) -> Optional[RelationPin]:
        """Unpins the list.

        Returns
        ---------
        Optional[:class:`RelationPin`]
            This method returns a :class:`RelationPin` object.


        .. versionadded:: 1.5.0
        """
        res = self.http_client.request("DELETE", "2", f"/users/{self.owner.id}/pinned_lists/{self.id}", auth=True)

        return RelationPin(res)

    def add_members(self, *users: User):
        """Adds members to the list.

        Parameters
        ------------
        *users: :class:`User`
            An array of :class:`User` arguments that you wist to add from the list. Example:

            .. code-blocks:: python

                some_list.add_members(user1, user2, user3)


        .. versionadded:: 1.5.0
        """
        executor = self.http_client.thread_manager.create_new_executor(thread_name="add-members-list-method")
        for user in users:
            executor.submit(
                self.http_client.request,
                "POST",
                "2",
                f"/lists/{self.id}/members",
                json={"user_id": str(user.id)},
                auth=True,
            )
        executor.wait_for_futures()

    def remove_members(self, *users: User):
        """Removes members to the list.

        Parameters
        ------------
        *users: :class:`User`
            An array of :class:`User` arguments that you wist to delete from the list. Example:

            .. code-blocks:: python

                some_list.remove_members(user1, user2, user3)


        .. versionadded:: 1.5.0
        """
        executor = self.http_client.thread_manager.create_new_executor(thread_name="remove-members-list-method")
        for user in users:
            executor.submit(self.http_client.request, "DELETE", "2", f"/lists/{self.id}/members/{user.id}", auth=True)
        executor.wait_for_futures()

    def fetch_members(self) -> Optional[UserPagination]:
        res = self.http_client.request(
            "GET",
            "2",
            f"/lists/{self.id}/members",
            params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
            auth=True,
        )
        if not res:
            return []

        return UserPagination(
            res,
            endpoint_request=f"/lists/{self.id}/member",
            http_client=self.http_client,
            params={"expansions": "pinned_tweet_id", "user.fields": USER_FIELD, "tweet.fields": TWEET_FIELD},
        )
