from typing import Any

from requests_oauthlib import OAuth1, OAuth1Session

__all__ = ("OauthSession",)


class OauthSession(OAuth1Session):
    def __init__(self, consumer_key: str, consumer_secret: str, callback=None) -> None:
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        self.consumer_key: str = consumer_key
        self.consumer_key_secret: str = consumer_secret
        self.access_token: str = None
        self.access_token_secret: str = None
        self.callback: Any = callback

    @property
    def oauth1(self) -> OAuth1:
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_key_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            decoding=None,
        )

    def set_access_token(self, key: str, secret: str) -> None:
        self.access_token = key
        self.access_token_secret = secret
