"""
MIT License

Copyright (c) 2021 TheFarGG & TheGenocides

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import datetime
from typing import Optional, List, TYPE_CHECKING
from .abc import Messageable
from .metrics import UserPublicMetrics
from .utils import time_parse_todt
from .types.user import User as UserPayload

if TYPE_CHECKING:
    from .http import HTTPClient
    
class User(Messageable):
    """Represent a user in Twitter.
    User is an identity in twitter, its very interactive. Can send message, post a tweet, and even send messages to other user through Dms.

    Parameters:
    ===================
    data: UserPayload
        The complete data of the user through a dictionary in a UserPayload format form!

    Attributes:
    ===================
    original_payload
        Represent the main data of a tweet.

    http_client
        Represent a :class: HTTPClient that make the request.
    
    user_metrics
	    Represent the public metrics of the user.
    """

    def __init__(self, data: UserPayload, **kwargs):
        super().__init__(data, **kwargs)
        self.original_payload = data
        self._payload = self.original_payload.get('data') if self.original_payload.get('data') != None else self.original_payload
        self.http_client: Optional[HTTPClient] = kwargs.get("http_client") or None
        self._metrics = UserPublicMetrics(self._payload) if self._payload != None else self.original_payload

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return "User(name={0.name} username={0.username} id={0.id})".format(
            self
        )

    @property
    def name(self) -> str:
        """str: Return the user's name."""
        return self._payload.get("name")

    @property
    def username(self) -> str:
        """str: Return the user's username, this usually start with '@' follow by their username."""
        return "@" + self._payload.get("username")

    @property
    def id(self) -> int:
        """id: Return the user's id."""
        return int(self._payload.get("id"))

    @property
    def bio(self) -> str:
        """str: Return the user's bio."""
        return self._payload.get("description")

    @property
    def description(self) -> str:
        """str: an alias to User.bio"""
        return self._payload.get("description")

    @property
    def profile_link(self) -> str:
        """str: Return the user's profile link"""
        return f"https://twitter.com/{self.username.replace('@', '', 1)}"

    @property
    def link(self) -> str:
        """str: Return url where the user put links, return an empty string if there isnt a url"""
        return self._payload.get("url")

    @property
    def verified(self) -> bool:
        """bool: Return True if the user is verified account, else False."""
        return self._payload.get("verified")

    @property
    def protected(self) -> bool:
        """bool: Return True if the user is protected, else False."""
        return self._payload.get("protected")

    @property
    def avatar_url(self) -> Optional[str]:
        """Optional[str]: Return the user profile image."""
        return self._payload.get("profile_image_url")

    @property
    def location(self) -> Optional[str]:
        """str: Return the user's location"""
        return self._payload.get("location")

    @property
    def created_at(self) -> datetime.datetime:
        """:class:datetime.datetime: Return datetime.datetime object with the user's account date."""
        return time_parse_todt(self._payload.get("created_at"))

    @property
    def pinned_tweet(self) -> Optional[object]:
        """Optional[:class:Tweet]: Returns the user's pinned tweet.
        Version Added: 1.1.3"""
        
        id=self._payload.get("pinned_tweet_id")
        return None if not id else self.http_client.fetch_tweet(int(id), http_client=self.http_client)

    @property
    def followers(self) -> List[object]:
        """List[:class:User]: Returns a list of users who are followers of the specified user ID."""
        return self._payload.get("followers")

    @property
    def following(self) -> List[object]:
        """List[:class:object]: Returns a list of users thats followed by the specified user ID."""
        return self._payload.get("following")

    @property
    def followers_count(self) -> int:
        """int: Return total of followers that a user has."""
        return int(self._metrics.followers_count)

    @property
    def following_count(self) -> int:
        """int: Return total of following that a user has."""
        return int(self._metrics.following_count)

    @property
    def tweet_count(self) -> int:
        """int: Return total of tweet that a user has."""
        return int(self._metrics.tweet_count)

    @property
    def listed_count(self) -> int:
        """int: Return total of listed that a user has."""
        return int(self._metrics.listed_count)