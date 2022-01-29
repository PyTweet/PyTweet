from __future__ import annotations
from typing import Any, List, Tuple, Optional, TYPE_CHECKING
from .errors import NoPageAvailable


if TYPE_CHECKING:
    from .http import HTTPClient
    from .type import Payload


class Pagination:
    """Represents the base class of all pagination objects.


    .. versionadded:: 1.5.0
    """
    __slots__ = ("__original_payload", "_payload", "_meta", "_next_token", "_previous_token", "_count", "_paginate_over", "_current_page_number", "_params", "item_type", "endpoint_request", "http_client", "pages_cache")

    def __init__(self, data: Payload, *,item_type: Any, endpoint_request: str, http_client: HTTPClient, **kwargs: Any):
        self.__original_payload = data
        self._payload = self.__original_payload.get("data")
        self._meta = self.__original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0
        self._paginate_over = 0
        self._current_page_number = 1
        self._params = kwargs.get("params", None)
        self.item_type = item_type
        self.endpoint_request = endpoint_request
        self.http_client = http_client
        self.pages_cache = {1: {obj.id: obj for obj in self.content}}

    @property
    def original_payload(self):
        return self.__original_payload

    @original_payload.setter
    def original_payload(self, other: dict):
        self.__original_payload = other
        return self.original_payload

    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, other: dict):
        self._payload = other
        return self._payload

    @property
    def content(self) -> list:
        """:class:`list`: Returns a list of objects from the current page's content.

        .. versionadded:: 1.5.0
        """
        return [self.item_type(data, http_client=self.http_client) for data in self.payload]

    @property
    def paginate_over(self) -> int:
        """:class:`int`: Returns how many times you change page over the pagination.

        .. versionadded:: 1.5.0
        """
        return self._paginate_over

    @property
    def current_page_number(self) -> int:
        """:class:`int`: Returns the current page number.

        .. versionadded:: 1.5.0
        """
        return self._current_page_number

    @property
    def pages(self) -> List[Tuple[int, list]]:
        """List[Tuple[:class:`int`, :class:`list`]]: Returns the zipped pages with the page number and content from a cache. If you never been into the page you want, it might not be returns in this property. example to use:

        .. code-block:: py

            for page_number, page_content in pagination.pages:
                ... #do something


        .. versionadded:: 1.5.0
        """
        fulldata = []
        for page_number in self.pages_cache.keys():
            fulldata.append(list(self.pages_cache.get(page_number).values()))
        return zip(range(1, len(self.pages_cache) + 1), fulldata)

    def get_page_content(self, page_number: int) -> Optional[list]:
        """Gets the page `content` from the pagination pages cache. If you never been into the page you want, it might not be returns.

        .. note::
            Note that, if the page_number is 0 it automatically would returns None. Specify number 1 or above.

        Returns
        ---------
        Optional[:class:`list`]
            This method returns a list of objects.


        .. versionadded:: 1.5.0
        """
        content = self.pages_cache.get(page_number)
        if not content:
            return None
        return list(content.values())

    def next_page(self):
        raise NotImplementedError

    def previous_page(self):
        raise NotImplementedError


class UserPagination(Pagination):
    """Represents a pagination that handles users object. This inherits :class:`Pagination`. These following methods returns this object:

    * :meth:`User.fetch_following`
    * :meth:`User.fetch_followers`
    * :meth:`User.fetch_muters`
    * :meth:`User.fetch_blockers`
    * :meth:`Tweet.fetch_likers`
    * :meth:`Tweet.fetch_retweeters`


    .. versionadded:: 1.5.0
    """
    def __init__(self, data, **kwargs):
        from .user import User #Avoid circular import error.
        super().__init__(data, item_type=User, **kwargs)

    def next_page(self):
        """Change page to the next page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._next_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._next_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number += 1
        self.original_payload = res
        self.payload = self.original_payload.get("data")
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {user.id: user for user in self.content}

    def previous_page(self):
        """Change page to the previous page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._previous_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._previous_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number -= 1
        self.original_payload = res
        self.payload = self.original_payload.get("data")
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {user.id: user for user in self.content}


class TweetPagination(Pagination):
    """Represents a pagination that handles tweets object. This inherits :class:`Pagination`. Only :meth:`User.fetch_timelines` returns this Pagination object.


    .. versionadded:: 1.5.0
    """
    def __init__(self, data, **kwargs):
        from .tweet import Tweet #Avoid circular import error.
        super().__init__(data, item_type=Tweet, **kwargs)

    # def _insert_author(self):
    #     fulldata = []
    #     for index, data in enumerate(self.original_payload["data"]):
    #         fulldata.append({})
    #         fulldata[index]["data"] = data
    #         fulldata[index]["includes"] = {}
    #         fulldata[index]["includes"]["users"] = [self.original_payload.get("includes", {}).get("users", [None])[0]]

    #     return [self.item_type(data, http_client=self.http_client) for data in fulldata]

    @property
    def content(self) -> list:
        """:class:`list`: Returns a list of objects from the current page's content.

        .. versionadded:: 1.5.0
        """

        return [self.item_type(data, http_client=self.http_client) for data in self.http_client.payload_parser.insert_tweet_pagination_author(self.original_payload)]

    def next_page(self):
        """Change page to the next page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._next_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._next_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number += 1
        self.original_payload = res
        self.payload = self.content()
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {tweet.id: tweet for tweet in self.content}

    def previous_page(self):
        """Change page to the previous page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._previous_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._previous_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number -= 1
        self.original_payload = res
        self.payload = self.content()
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {tweet.id: tweet for tweet in self.content}

class ListPagination(Pagination):
    """Represents a pagination that handles list objects. This inherits :class:`Pagination`. Only :meth:`User.fetch_lists` returns this Pagination object.


    .. versionadded:: 1.5.0
    """
    def __init__(self, data, **kwargs):
        from .list import List as TwitterList #Avoid circular import error
        super().__init__(data, item_type=TwitterList, **kwargs)

    def _insert_owner(self):
        fulldata = []
        for index, data in enumerate(self.original_payload["data"]):
            fulldata.append({})
            fulldata[index]["data"] = data
            fulldata[index]["includes"] = {}
            fulldata[index]["includes"]["users"] = [self.original_payload.get("includes", {}).get("users", [None])[0]]

        return [self.item_type(data, http_client=self.http_client) for data in fulldata]

    @property
    def content(self) -> list:
        """:class:`list`: Returns a list of objects from the current page's content.

        .. versionadded:: 1.5.0
        """

        return self._insert_owner()

    def next_page(self):
        """Change page to the next page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._next_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._next_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number += 1
        self.original_payload = res
        self.payload = self._insert_owner()
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {_TwitterList.id: _TwitterList for _TwitterList in self.content}

    def previous_page(self):
        """Change page to the previous page.

        Raises
        --------
        :class:`NoPageAvailable`
            Raises when no page available to change.


        .. versionadded:: 1.5.0
        """
        if not self._previous_token:
            raise NoPageAvailable()
        self._params["pagination_token"] = self._previous_token

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params=self._params,
        )
        if not res:
            raise NoPageAvailable()

        previous_content = self.content
        self._current_page_number -= 1
        self.original_payload = res
        self.payload = self._insert_owner()
        self._meta = self.original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {_TwitterList.id: _TwitterList for _TwitterList in self.content}