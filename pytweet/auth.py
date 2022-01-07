from __future__ import annotations

import base64
import random
import string
import datetime

from random import randint
from typing import Tuple, Optional, TYPE_CHECKING
from requests_oauthlib import OAuth1
from .errors import PytweetException

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = ("OauthSession", "Scope")

class Scope:
    """Scopes allow you to set granular access for your App so that your App only has the permissions that it needs. Here are the full documented scopes!

    .. list-table:: Scopes
        :widths: 33, 33
        :header-rows: 1

        *   - Scope
            - Description
        *   - tweet.read
            - All the Tweets you can view, including Tweets from protected accounts.
        *   - tweet.write
            - Tweet and Retweet for you.
        *   - tweet.moderate.write
            - Hide and unhide replies to your Tweets.
        *   - users.read
            - Any account you can view, including protected accounts.
        *   - follows.read
            - People who follow you and people who you follow.
        *   - follows.write
            - Follow and unfollow people for you.
        *   - offline.access
            - Stay connected to your account until you revoke access.
        *   - space.read
            - All the Spaces you can view.
        *   - mute.read
            - Accounts you’ve muted.
        *   - mute.write
            - Mute and unmute accounts for you.
        *   - like.read
            - Tweets you’ve liked and likes you can view.
        *   - like.write
            - Like and un-like Tweets for you.
        *   - list.read
            - Lists, list members, and list followers of lists you’ve created or are a member of, including private lists..
        *   - list.write
            - Create and manage Lists for you..
        *   - block.read
            - Accounts you’ve blocked.
        *   - block.write
            - Block and unblock accounts for you.


    .. versionadded:: 1.5.0
    """

    def __init__(
        self,
        *,
        tweet_read: bool = False,
        tweet_write: bool = False,
        tweet_moderate_write: bool = False,
        users_read: bool = False,
        follows_read: bool = False,
        follows_write: bool = False,
        offline_access: bool = False,
        space_read: bool = False,
        mute_read: bool = False,
        mute_write: bool = False,
        like_read: bool = False,
        like_write: bool = False,
        list_read: bool = False,
        list_write: bool = False,
        block_read: bool = False,
        block_write: bool = False,
    ):
        self.tweet_read = "tweet.read" if tweet_read else None
        self.tweet_write = "tweet.write" if tweet_write else None
        self.tweet_moderate_write = "tweet.moderate.write" if tweet_moderate_write else None
        self.users_read = "users.read" if users_read else None
        self.follows_read = "follows.read" if follows_read else None
        self.follows_write = "follows.write" if follows_write else None
        self.offline_access = "offline.access" if offline_access else None
        self.space_read = "space.read" if space_read else None
        self.mute_read = "mute.read" if mute_read else None
        self.mute_write = "mute.write" if mute_write else None
        self.like_read = "like.read" if like_read else None
        self.like_write = "like.write" if like_write else None
        self.list_read = "list.read" if list_read else None
        self.list_write = "list.write" if list_write else None
        self.block_read = "block.read" if block_read else None
        self.block_write = "block.write" if block_write else None

    @classmethod
    def read_only(cls, *, offline_access: bool = False):
        """A classmethod that enables only read scopes. offline_access scope is optional, you can set it true or not. Defaults to False.

        Parameters
        ------------
        offline_access: :class:`bool`
            Indicates to stay connected to your account until you revoke access.


        .. versionadded:: 1.5.0
        """
        return cls(
            tweet_read=True,
            users_read=True,
            follows_read=True,
            space_read=True,
            mute_read=True,
            like_read=True,
            list_read=True,
            block_read=True,
            offline_access=offline_access,
        )

    @classmethod
    def write_only(cls, *, offline_access: bool = False):
        """A classmethod that enables only write scopes. This includes tweet_moderate_write scope. offline_access scope is optional, you can set it true or not. Defaults to False.

        Parameters
        ------------
        offline_access: :class:`bool`
            Indicates to stay connected to your account until you revoke access.


        .. versionadded:: 1.5.0
        """
        return cls(
            tweet_write=True,
            follows_write=True,
            mute_write=True,
            like_write=True,
            list_write=True,
            block_write=True,
            tweet_moderate_write=True,
            offline_access=offline_access,
        )

    @classmethod
    def all(cls, *, offline_access: bool = False):
        """A classmethod that enables all scopes. offline_access scope is optional, you can set it true or not. Defaults to False.

        Parameters
        ------------
        offline_access: :class:`bool`
            Indicates to stay connected to your account until you revoke access.


        .. versionadded:: 1.5.0
        """
        return cls(
            tweet_read=True,
            tweet_write=True,
            tweet_moderate_write=True,
            users_read=True,
            follows_read=True,
            follows_write=True,
            offline_access=offline_access,
            space_read=True,
            mute_read=True,
            mute_write=True,
            like_read=True,
            like_write=True,
            list_read=True,
            list_write=True,
            block_read=True,
            block_write=True,
        )

    @property
    def values(self) -> str:
        """:class:`str`: Returns the scope url encoded value. Example:

        .. code-block:: py

            import pytweet

            scope = pytweet.Scope(tweet_read=True, tweet_write=True)
            print(scope.value)
            #>>> This will returns: tweet.read%20tweet.write


        .. versionadded:: 1.5.0
        """
        value = ""
        for attr in dir(self):
            if "_read" in attr or "_write" in attr or "_access" in attr:
                scope = getattr(self, attr, None)
                if scope:
                    value += f"{scope}%20"

        return value.rstrip("%20")  # Only remove the last %20.


class OauthSession:
    """Represents an OauthSession for OAuth1 and OAuth2 Authorization.

    Parameters
    ------------
    consumer_key: Optional[:class:`str`]
        The application's consumer key.
    consumer_secret: Optional[:class:`str`]
        The application's consumer secret.
    access_token: Optional[:class:`str`]
        The application's access token.
    access_token_secret: Optional[:class:`str`]
        The application's access token secret.
    http_client: :class:`HTTPClient
        The :class:`HTTPClient` for making requests.
    callback_url: Optional[:class:`str`]
        The callback url, the user will get redirect to the callback url after they authorize. Default to None.
    client_id: Optional[:class:`str`]
        The client's OAuth 2.0 Client ID from keys and tokens page.
    client_secret: Optional[:class:`str`]
        The client's OAuth 2.0 Client Secret from keys and tokens page.


    .. versionadded:: 1.2.0
    """

    def __init__(
        self,
        consumer_key: Optional[str],
        consumer_secret: Optional[str],
        *,
        access_token: Optional[str],
        access_token_secret: Optional[str],
        http_client: HTTPClient,
        callback_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> None:
        self.http_client: HTTPClient = http_client
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.callback_url = callback_url
        self.client_id = client_id
        self.client_secret = client_secret

    @property
    def oauth1(self) -> OAuth1:
        """:class:`Oauth1`: Wrap the credentials in a function that return Oauth1. Usually Uses for Authorization.

        .. versionadded:: 1.2.0
        """
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
            callback_uri=self.callback_url,
            decoding=None,
        )

    @property
    def request_session(self):
        return self.http_client._HTTPClient__session

    @property
    def basic_auth(self) -> str:
        """:class:`str`: The decoded base64 encoded client id and secret.

        .. versionadded:: 1.5.0
        """
        if not self.client_id and not self.client_secret:
            raise PytweetException("'client_id' and 'client_secret' argument is missing in your client instance!")

        return base64.b64encode(bytes(f"{self.client_id}:{self.client_secret}", "utf-8")).decode()

    def invalidate_access_token(self) -> None:
        """Invalidate the access token and access token secret of yout client.

        .. warning::
            This staticmethod will invalidate your access token and access token secret of your client.


        .. versionadded:: 1.3.5
        """
        self.http_client.request("POST", "1.1", "/oauth/invalidate_token", auth=True)

    def generate_oauth_url(self, access_type: str = "write", *,force_login: bool = False, screen_name: Optional[str] = None) -> Optional[str]:
        """Generates an oauth url with an access type. The callback after pressing authorize button is your callback url that you passed in your :class:`Client`. The oauth_token and oauth_verifier will automatically appended in the callback url. If you are setting up a sign up button in your website to lookup the user's profile information, You have to setup a system where if the oauth_token or oauth_verifier is present in the url then, it will use :meth:`OauthSession.post_oauth_token` to post an oauth token and verifier to exchange with the user's access token and secret. If its for personal uses then just copy the result and passed in :meth:`OauthSession.post_oauth_token`.

        Parameters
        ------------
        access_type: :class:`str`
            Must be either read, write, direct_messages. read for reading twitter info only, write will have the same as read and also write permission this includes but not limited to post & delete a :class:`Tweet`, and direct_messages is for read & write and sending & deleting :class:`DirectMessages`.
        force_login: :class:`bool`
            Forces the user to enter their credentials to ensure the correct users account is authorized.
        screen_name: :class:`str`
            Prefills the username input box of the OAuth login screen with the given value.

        Returns
        ---------
        :class:`str`
            Returns an oauth url.


        .. versionadded:: 1.3.5
        """
        if not self.callback_url:
            raise PytweetException("'callback_url' argument is missing in your client instance")

        access_type = access_type.lower()
        assert access_type in ("read", "write", "direct_messages")
        request_tokens = self.http_client.request(
            "POST",
            "",
            "oauth/request_token",
            params={
                "oauth_callback": self.callback_url,
                "x_auth_access_type": access_type,
            },
            auth=True,
        )
        oauth_token, oauth_token_secret, oauth_callback_confirmed, = request_tokens.split("&")
        url = "https://api.twitter.com/oauth/authorize" + f"?{oauth_token}"
        if force_login:
            url += "?force_login=true"
        
        if screen_name:
            url += f"?screen_name={screen_name}"        
        return url

    def post_oauth_token(self, oauth_token: str, oauth_verifier: str) -> Optional[Tuple[str]]:
        """Posts the oauth token & verifier, this method will returns a pair of access token & secret also the user's username(present as screen_name) and id e.g ("access_token=xxxxxxxxxxxxx", "access_token_secret=xxxxxxxxxxxxx", "screen_name=TheGenocides", "user_id=1382006704171196419"). Uses the access token and secret to make request on behalf of users! You can use the raw api or construct another client with the access token and secret.

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

    def create_oauth2_url(self, scope: Scope, *, code_challenge_method: str = "plain", state: Optional[str] = None):
        """Creates an oauth 2 url. This is The 1st step of using OAuth 2.0 Authorization Code Flow with PKCE. The callback after pressing authorize button is your callback url that you passed in your :class:`Client`.

        Parameters
        ------------
        scope: :class:`Scope`
            The scope permissions. Must be an instance of :class:`Scope`.
        code_challenge_method: :class:`str`
            The code challenge method, must be tiher plain or s256. Default to plain.
        state: Optional[:class:`str`]
            A random string you provide to verify against CSRF attacks. If none specified, the method will generates one.


        .. versionadded:: 1.5.0
        """
        if not self.callback_url:
            raise PytweetException("'callback_url' argument is missing in your client instance")

        code_challenge_method = code_challenge_method.lower()
        assert code_challenge_method in [
            "plain",
            "s256",
        ], "Wrong code_challenge_method passed: must be 'plain' or 's256'"

        if not state:
            state = "".join(random.choices(string.ascii_uppercase + string.digits, k=10)).lower()
        else:
            state = base64.b64decode(state.encode())

        now = datetime.datetime.now()
        timestamp = now.strftime("%m%d%Y%H%M%S")
        random_append = randint(1000, 100000)
        rand_dec = randint(300, 800)
        state = base64.b64encode(state.encode()).decode()
        code_challenge = "{}{}.{}".format(timestamp, random_append, rand_dec)
        client_id = self.client_id
        response_type = "code"
        scope = scope.values

        return f"https://twitter.com/i/oauth2/authorize?response_type={response_type}&client_id={client_id}&redirect_uri={self.callback_url}&scope={scope}&state={state}&code_challenge={code_challenge}&code_challenge_method={code_challenge_method}"

    def post_auth_code(self, code: str, code_challenge: str):
        """Posts the authorize code and code challenge. This is The 2nd step of using OAuth 2.0 Authorization Code Flow with PKCE. In this method, the client will make a request and create a new bearer token. With this, you can make request on behalf of users.

        Parameters
        ------------
        code: :class:`str`
            The authorize code.
        code_challenge: :class:`str`
            The code challenge.


        .. versionadded:: 1.5.0
        """
        res = self.http_client.request(
            "POST",
            "2",
            "/oauth2/token",
            data=f"code={code}&grant_type=authorization_code&client_id={self.client_id}&redirect_uri={self.callback_url}&code_verifier={code_challenge}",
            headers={"Authorization": f"Basic {self.basic_auth}", "Content-Type": "application/x-www-form-urlencoded"},
        )

        return res
