from __future__ import annotations

from typing import Optional, Tuple, Any, Type, TYPE_CHECKING
from requests_oauthlib import OAuth1, OAuth1Session

if TYPE_CHECKING:
    from .client import Client

__all__ = ("OauthSession",)


class OauthSession(OAuth1Session):
    """
    The OauthSession, this usually is uses for POST requests and requests that need Oauth1 Authorization.

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

    def __init__(self, consumer_key: Optional[str], consumer_secret: Optional[str], callback=None) -> None:
        super().__init__(consumer_key, client_secret=consumer_secret, callback_uri=callback)
        self.is_with_oauth_flow = False
        self.consumer_key = consumer_key
        self.consumer_key_secret = consumer_secret
        self.access_token: str = None
        self.access_token_secret: str = None
        self.callback: Any = callback

    @staticmethod
    def invalidate_access_token(client: Client) -> None:
        """A staticmethod to invalidate a pair of access token and access token secret!

        .. warning::
            This staticmethod will invalidate your access token and access token secret that you passed in your :meth:`Client` argument.

        Parameters
        ------------
        access_token: :class:`str`
            The oauth1 access token to be invalidate.
        access_token_secret: :class:`str`
            The oauth1 access token secret to be invalidate.
        client: :class:`Client`
            An instance of your :meth:`Client`, note that this staticmethod will invalidate the access token and access token secret in this :meth:`Client`.


        .. versionadded:: 1.3.5
        """
        client.http.request("POST", "1.1", "/oauth/invalidate_token", auth=True)

    @classmethod
    def with_oauth_flow(cls: Type[OauthSession], client, *, callback: str = "https://twitter.com") -> OauthSession:
        """Authorize a user using the 3 legged oauth flow classmethod! This let's your application to do an action on behalf of a user. This will give you 2 new methods, :meth:`OauthSession.generate_oauth_url` for generating an oauth url so a user can authorize and `post_oauth_token` posting oauth token and verifier for getting a pair of access token and secret.

        .. note::
            There are 3 steps for using 3 legged oauth flow:

            * Use :meth:`OauthSession.generate_oauth_url`
            method and generate an oauth link.

            * Click that link and press the authorize button, you should get redirect to the callback-url with an oauth token and verifier appended in that url, e.g `http://twitter.com/home` will be `http://twitter.com/home?oauth_token=xxxxxxxxxxxxxxxxxx?oauth_verifier=xxxxxxxxxxxxxxxxxx`, copy the oauth token & verifier and use it in the next step.

            * Use post_oauth_token method with the oauth token and verifier. It should return a pair of access token & secret, it also return the screen name and user id. Now use those access token & secret in access_token & access_token_secret arguments in pytweet.Client, and now you can use the client to do certain action!

        """
        self = cls(None, None, callback)
        self.is_with_oauth_flow = True

        def generate_oauth_url(auth_access_type: str = "write") -> Optional[str]:
            """Generate a url with an access type.

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
            request_tokens = client.http.request(
                "POST",
                "",
                "oauth/request_token",
                params={
                    "oauth_callback": callback,
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

        def post_oauth_token(oauth_token: str, oauth_verifier: str) -> Optional[Tuple[str]]:
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
            res = client.http.request(
                "POST",
                "",
                "oauth/access_token",
                params={"oauth_token": oauth_token, "oauth_verifier": oauth_verifier},
            )

            return tuple(res.split("&"))

        self.post_oauth_token = post_oauth_token
        self.generate_oauth_url = generate_oauth_url
        return self

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
