from typing import Optional, Any
from requests_oauthlib import OAuth1, OAuth1Session

__all__ = ("OauthSession",)


class OauthSession(OAuth1Session):
    """
    The OauthSession, this usually is uses for POST requests and requests that need Oauth1 Authorization.

    .. versionadded:: 1.2.0
    """

    def __init__(self, consumer_key: Optional[str], consumer_secret: Optional[str], callback=None) -> None:
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        self.is_with_oauth_flow = False
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_secret
        self.access_token: str = None
        self.access_token_secret: str = None
        self.callback: Any = callback

    @classmethod
    def with_oauth_flow(
        cls,
        client,
        *,
        callback: str = "https://twitter.com"
    ):
        """Authorize a user using the 3 legged oauth flow classmethod!

        .. warning::
            This classmethod is not finished yet!

        """
        self = cls(None, None, callback)
        self.is_with_oauth_flow = True
        def post_access_token(oauth_token: str, oauth_verifier: str):
            print(oauth_token, oauth_verifier)
            res = client.http.request("POST", "", "oauth/access_token", params={"oauth_token": oauth_token, "oauth_verifier": oauth_verifier})
            oauth_token, oauth_token_secret, user_id, screen_name = res.split("&")
            return oauth_token, oauth_token_secret, user_id, screen_name

        def generate_oauth_url(auth_access_type: str = "write"):
            assert auth_access_type in ["read", "write"]
            request_tokens = client.http.request(
                "POST", 
                "", 
                "oauth/request_token",
                params={
                    "oauth_callback": callback,
                    "x_auth_access_type": auth_access_type
                }, 
                auth=True
            )
            oauth_token, oauth_token_secret, oauth_callback_confirmed = request_tokens.split("&")
            url = "https://api.twitter.com/oauth/authorize" + f"?{oauth_token}"
            return url

        self.post_access_token = post_access_token 
        self.generate_oauth_url = generate_oauth_url
        return self

    @property
    def oauth1(self) -> OAuth1:
        """:class:`Oauth1`: Wrap the credentials in a function that return Oauth1. Usually Uses for Authorization.

        .. versionadded:: 1.2.0
        """
        if self.is_with_oauth_flow:
            return None

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
        if self.is_with_oauth_flow:
            return None

        self.access_token = key
        self.access_token_secret = secret
