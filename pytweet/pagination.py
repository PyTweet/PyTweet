from __future__ import annotations
from typing import Any, List, Tuple, TYPE_CHECKING
from .expansions import TWEET_FIELD, USER_FIELD
from .errors import NoPageAvailable

if TYPE_CHECKING:
    from .http import HTTPClient
    from .type import Payload

class Pagination:
    """Represents a pagination object, some endpoints returns more objects but limits it to some pages. Using :class:`Pagination`, you can change page and manage objects easily. Example:

    .. code-block:: py

        user = client.fetch_user(ID)
        pagination = user.fetch_following()
        print("Page 1 :", pagination.content)
        pagination.next_page() #Change page to the next page
        print("Page 2 :", pagination.content)
        pagination.previous_page() #Change page to the previous page
        print("Page 1 :", pagination.content)
    
    .. versionadded:: 1.5.0
    """
    def __init__(self, data: Payload, item_type: Any, endpoint_request: str, *,http_client: HTTPClient):
        self.__original_payload = data
        self._payload = self.__original_payload.get("data")
        self._meta = self.__original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0
        self._paginate_over = 0
        self.item_type = item_type
        self.endpoint_request = endpoint_request
        self.http_client = http_client
        self.pages_cache = {1: {user.id:user for user in self.content}}

    @property
    def content(self) -> list:
        """:class:`list`: Returns a list of objects.
        
        .. versionadded:: 1.5.0
        """
        return [self.item_type(data, http_client=self.http_client) for data in self._payload]

    @property
    def paginate_over(self) -> int:
        """:class:`int`: Returns how many pages you change over the pagination.
        
        .. versionadded:: 1.5.0
        """
        return self._paginate_over

    @property
    def pages(self) -> List[Tuple]:
        """List[Tuple]: Returns the zipped pages with the page number and content. example to use:

        .. code-block:: py

            for page_number, page_content in pagination.pages:
                ... #do something

        
        .. versionadded:: 1.5.0
        """
        return zip(range(1, len(self.pages_cache) + 1), list(self.pages_cache.values()))

    def get_page_content(self, page_number: int) -> list:
        """Gets the page content from the pagination pages cache.

        .. note::
            Note that, if the page_number is 0 it automatically would returns None. Specify number 1 or above.
        

        .. versionadded:: 1.5.0
        """
        content = self.pages_cache.get(page_number)
        if not content:
            return None
        return [self.item_type(data, http_client=self.http_client) for data in list(content.values())]

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

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params={
                "expansions": "pinned_tweet_id",
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
                "pagination_token": self._next_token
            }
        )
        previous_content = self.content

        self.__original_payload = res
        self._payload = self.__original_payload.get("data")
        self._meta = self.__original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {user.id:user for user in self.content}

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

        res = self.http_client.request(
            "GET",
            "2",
            self.endpoint_request,
            auth=True,
            params={
                "expansions": "pinned_tweet_id",
                "user.fields": USER_FIELD,
                "tweet.fields": TWEET_FIELD,
                "pagination_token": self._previous_token
            }
        )
        previous_content = self.content

        self.__original_payload = res
        self._payload = self.__original_payload.get("data")
        self._meta = self.__original_payload.get("meta")
        self._next_token = self._meta.get("next_token")
        self._previous_token = self._meta.get("previous_token")
        self._count = 0

        if not previous_content[0] == self.content[0]:
            self.pages_cache[len(self.pages_cache) + 1] = {user.id:user for user in self.content}