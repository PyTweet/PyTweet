from __future__ import annotations
from typing import Any, Type, Tuple, Optional, TYPE_CHECKING 
from requests_oauthlib import OAuth1, OAuth1Session
from .utils import build_object

if TYPE_CHECKING:
    from .client import Client

__all__ = ("OauthSession",)

class OauthSession(OAuth1Session):
    """Represents an OauthSession for Oauth1 Authorization. This class is very importantfo

    Parameters
    ------------
    consumer_key: Optional[:class:`str`]
        The application's consumer key.
    consumer_secret: Optional[:class:`str`]
        The application's consumer secret.
    callback: Optional[:class:`str`]
        The callback url, the user will get redirect to the callback url after they authorize. Default to None.


    .. versionadded:: 1.2.0
    """

    def __init__(self, consumer_key: Optional[str], consumer_secret: Optional[str], *, http_client: object, callback: Optional[str] = None) -> None:
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        HTTPClient = build_object("HTTPClient")
        
        self.http_client: HTTPClient = http_client
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_secret
        self.access_token: str = None
        self.access_token_secret: str = None
        self.callback: Any = callback

    @staticmethod
    def invalidate_access_token(client: Client) -> None:
        """A staticmethod that can be used to invalidate the access token and access token secret of a client.

        .. warning::
            This staticmethod will invalidate your access token and access token secret of your client.


        Parameters
        ------------
        client: :class:`Client`
            Your client.


        .. versionadded:: 1.3.5
        """
        client.http.request("POST", "1.1", "/oauth/invalidate_token", auth=True)

    def generate_oauth_url(self, auth_access_type: str = "write") -> Optional[str]:
        """Generate an oauth url with an access type.

        Parameters
        ------------
        auth_access_type: :class:`str`
            Must be either read, write, direct_messages. read for reading twitter info only, write will have the same as read and also write permission this includes but not limited to post & delete a :class:`Tweet`, and direct_messages is for read & write and sending & deleting :class:`DirectMessages`.

        Returns
        ---------
        :class:`str`
            Returns an oauth url.


        .. versionadded:: 1.3.5
        """
        auth_access_type = auth_access_type.lower()
        assert auth_access_type in ("read", "write", "direct_messages")
        request_tokens = self.http_client.request(
            "POST",
            "",
            "oauth/request_token",
            params={
                "oauth_callback": self.callback,
                "x_auth_access_type": auth_access_type,
            },
            auth=True,
        )
        (
            oauth_token,
            oauth_token_secret,
            oauth_callback_confirmed,
        ) = request_tokens.split("&")
        url = "https://api.twitter.com/oauth/authorize" + f"?{oauth_token}"
        return url

    def post_oauth_token(self, oauth_token: str, oauth_verifier: str) -> Optional[Tuple[str]]:
        """Post the oauth token & verifier, this method will returns a pair of access token & secret.

        Parameters
        ------------
        oauth_token: :class:`str`
            The Oauth token.
        oauth_verifier: :class:`str`
            The Oauth verifier.

        Returns
        ---------
        :class:`tuple`
            Returns a :class:`tuple` object with the credentials in.


        .. versionadded:: 1.3.5
        """
        res = self.http_client.request(
            "POST",
            "",
            "oauth/access_token",
            params={"oauth_token": oauth_token, "oauth_verifier": oauth_verifier},
        )

        return tuple(res.split("&"))

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

    def set_consumer_key(self, consumer_key: str, consumer_secret: str) -> None:
        """Set a the consumer key and secret"""
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
