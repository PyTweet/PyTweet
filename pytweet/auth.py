from typing import Any

from requests_oauthlib import OAuth1, OAuth1Session

__all__ = ("OauthSession",)


class OauthSession(OAuth1Session):
    """
    The OauthSession, this usually is uses for POST requests and requests that need Oauth1 Authorization.

    .. versionadded:: 1.2.0
    """

    def __init__(self, consumer_key: str, consumer_secret: str, callback=None) -> None:
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        self.consumer_key: str = consumer_key
        self.consumer_key_secret: str = consumer_secret
        self.access_token: str = None
        self.access_token_secret: str = None
        self.callback: Any = callback

    @property
    def oauth1(self) -> OAuth1:
        """:class:`Oauth1`: Wrap the credentials in a function that return Oauth1. Usually Uses for Authorization.

        Returns
        ---------
        :class:`OAuth1`
            This function returns an OAuth1 object.

        .. versionadded:: 1.2.0
        """
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_key_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            decoding=None,
        )

    def set_access_token(self, key: str, secret: str) -> None:
        """Set the access token's key and secret."""
        self.access_token = key
        self.access_token_secret = secret
