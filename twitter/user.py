import datetime
from typing import Dict, Any, Optional
from dateutil import parser
from .errors import UserNotFound

#Continue Later...
class UserPublicMetrics:
    def __init__(self, data=Dict[str, Any]):
        self.original_payload=data
        self._payload=data['public_metrics']

    @property
    def followers_count(self) -> int:
        return self._payload['followers_count']

    @property
    def following_count(self) -> int:
        return self._payload['following_count']

    @property
    def tweet_count(self) -> int:
        return self._payload['tweet_count']

    def __repr__(self) -> str:
        return f"<UserPublicMetrics: user={self.original_payload.get('username')} followers_count={self._payload.get('followers_count')} following_count={self._payload.get('following_count')} tweet_count={self._payload.get('tweet_count')}>"

class User:
    def __init__(self, data:Dict[str, Any]): 
        self._payload=data

    @property
    def name(self) -> str:
        return self._payload['name']

    @property
    def username(self) -> str:
        return self._payload['username']
    
    @property
    def id(self) -> int:
        return self._payload['id']

    @property
    def description(self) -> str:
        return self._payload['description']

    @property
    def verified(self) -> bool:
        return self._payload['verified']

    @property
    def protected(self) -> bool:
        return self._payload['protected']

    @property
    def profile_mage(self) -> Optional[str]:
        return self._payload['profile_image_url']    

    @property
    def created_at(self) -> datetime.datetime:
        date=str(parser.parse(self._payload['created_at']))
        y, mo, d=date.split("-")
        h, mi, s, null=d.split(" ")[1].replace("0", " ").replace("+", " ").strip(" ").split(":")
        return datetime.datetime(year=int(y), month=int(mo), day=int(d.split(" ")[0]), hour=int(h), minute=int(mi), second=int(s))

    @property
    def public_metrics(self) -> UserPublicMetrics:
        return UserPublicMetrics(self._payload)

    def __repr__(self) -> str: #Return the repr of User, repr called when we print the class!
        return "<User: name={0.name} username={0.username} description={0.description} id={0.id} created_at={0.created_at} verified={0.verified} protected={0.protected} profile_mage={0.profile_mage} <UserPublicMetrics: followers_count={0.public_metrics.followers_count} following_count={0.public_metrics.following_count} tweet_count={0.public_metrics.tweet_count}>>".format(self)

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]):
        try:
            if 'data' in dict.keys():
                raise TypeError("data key in dict, please return the data's value!")
        except KeyError:
            error=dict["errors"][0]
            raise UserNotFound(error["detail"])
        
        return cls(dict) #Return new instance of User! 