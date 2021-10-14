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
from typing import Dict, Any, Optional, TYPE_CHECKING
from dateutil import parser
from .type import Messageable

if TYPE_CHECKING: #prevent circular import error
    from .client import Client

class UserPublicMetrics:
    def __init__(self, data=Dict[str, Any], **kwargs):
        self.original_payload=data
        self._public=data.get('public_metrics')

    @property
    def followers_count(self) -> int:
        return self._public.get('followers_count')

    @property
    def following_count(self) -> int:
        return self._public.get('following_count')

    @property
    def tweet_count(self) -> int:
        return self._public.get('tweet_count')

    def __str__(self) -> str:
        return f"<UserPublicMetrics: user={self.original_payload.get('username')} followers_count={self._payload.get('followers_count')} following_count={self._payload.get('following_count')} tweet_count={self._payload.get('tweet_count')}>"

    def __repr__(self) -> str:
        return f"<UserPublicMetrics: User={self.original_payload.get}>"

class User(UserPublicMetrics, Messageable):
    """
    Represent a user in Twitter. 
    This user is an account that has created by other person, not from an apps.

    Parameters:
    ===================
    data: Dict[str, Any] -> The complete data of the user through a dictionary!

    Attributes:
    ===================
    :property: name -> Return the user's name.

    :property: username -> Return the user's username, this usually start with '@' follow by their username.

    :property: description -> Return the user's description.

    :property: url -> Return url where the user put in links, return None if there isnt a url.
    
    :property: id -> Return the user's id.

    :property: verified -> Return True if the user is verified account, else False.

    :property: protected -> Return True if the user is protected, else False.

    :property: profile_image -> Return the user profile image.

    :property: created_at -> Return datetime.datetime object with user's account date.

    :property: location -> Return a user's location, Somehow it return None in get_user_by_username and get_user function, Get it using get_tweet function. Will fix that soon!  

    :property: followers -> Returns a list of users who are followers of the specified user ID.

    :property: following -> Returns a list of users thats followed by the specified user ID.  
    """
    def __init__(self, data:Dict[str, Any], **kwargs): 
        super().__init__(data, **kwargs)
        self._payload=data
        self.provider: Optional[Client] = kwargs.get('provider') or None
        self.description=self.bio

    @property
    def name(self) -> str:
        return self._payload.get('name')

    @property
    def username(self) -> str:
        return "@" + self._payload.get('username')
    
    @property
    def id(self) -> int:
        return self._payload.get('id')

    @property
    def bio(self) -> str:
        return self._payload.get('description')
   
    @property
    def link(self) -> str:
        return f"https://twitter.com/{self.username}" 

    @property
    def website(self) -> str:
        return self._payload.get('url')

    @property
    def verified(self) -> bool:
        return self._payload.get('verified')

    @property
    def protected(self) -> bool:
        return self._payload.get('protected')

    @property
    def profile_mage(self) -> Optional[str]:
        return self._payload.get('profile_image_url')

    @property
    def location(self) -> Optional[str]:
        return self._payload.get('location')

    @property
    def created_at(self) -> datetime.datetime:
        date=str(parser.parse(self._payload.get('created_at')))
        y, mo, d=date.split("-")
        h, mi, s=date.split(" ")[1].split('+')[0].split(":")
        
        return datetime.datetime(year=int(y), month=int(mo), day=int(d.split(" ")[0]), hour=int(h), minute=int(mi), second=int(s))

    @property
    def followers(self) -> Optional[list]:
        return self._payload.get("followers")

    @property
    def following(self) -> Optional[list]:
        return self._payload.get("following")

    # def follow(self) -> Any:
    #     r=Route("POST", "2", f"/users/22146191/following")
    #     headers={"Consumer Key": self.provider.consumer_key, "Consumer Secret": self.provider.consumer_key_secret, "Token": self.provider.access_token, "Token Secret": self.provider.access_token_secret, "content-type":"application/x-www-form-urlencoded"}
    #     print(r.url)
    #     req=requests.request("POST", r.url, headers=headers, json={"target_user_id": str(self.id)})
    #     print(req.text)
   
    #     return req.json()

    def __str__(self) -> str:
        return "<User: name={0.name} username={0.username} description={0.description} id={0.id} created_at={0.created_at} verified={0.verified} protected={0.protected} profile_mage={0.profile_mage} location={0.location} followers_count={0.followers_count} following_count={0.following_count} tweet_count={0.tweet_count}>".format(self)

    def __repr__(self) -> str:
        return "<User Object: {0.username}>".format(self)
    