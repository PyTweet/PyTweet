from typing import Optional, Any
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

    @classmethod
    def with_oauth_flow(
        cls,
        client,
        *,
        callback: str = "https://twitter.com",
        auth_access_type: str = "write",
        force_login: bool = False,
        screen_name: Optional[str] = None
    ):
        """Authorize a user using the 3 legged oauth flow classmethod!

        .. warning::
            This classmethod is not finished yet!

        """
        return 0
        request_tokens = client.http.request("POST", "", "oauth/request_token", auth=True)
        oauth_token, oauth_token_secret, oauth_callback_confirmed = request_tokens.split("&")
        params = {"oauth_token": oauth_token}

        res = client.http.request("GET", "", "oauth/authorize", params=params, auth=True)

    @property
    def oauth1(self) -> OAuth1:
        """:class:`Oauth1`: Wrap the credentials in a function that return Oauth1. Usually Uses for Authorization.

        .. versionadded:: 1.2.0
        """
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_key_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            callback_uri=self.callback,
            decoding=None,
        )

    def set_access_token(self, key: str, secret: str) -> None:
        """Set the access token's key and secret."""
        self.access_token = key
        self.access_token_secret = secret
