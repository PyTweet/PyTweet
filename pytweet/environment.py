from __future__ import annotations

import logging
import datetime
from typing import Any, List, Dict, TYPE_CHECKING
from .utils import time_parse_todt

if TYPE_CHECKING:
    from .client import Client
    from .type import ID

_log = logging.getLogger(__name__)


class Environment:
    """Represents a dev environment to use one of the subscription APIs (Account Activity API or events etc)

    .. versionadded:: 1.5.0
    """

    __slots__ = ("_payload", "client")

    def __init__(self, data: Dict[str, Any], *, client: Client):
        self._payload = data
        self.client = client

    def __repr__(self) -> str:
        return f"Environment(name={self.name})"

    @property
    def name(self) -> str:
        """:class:`str`: The environment name/label.

        .. versionadded:: 1.5.0
        """
        return self._payload.get("environment_name")

    @property
    def label(self) -> str:
        """:class:`str`: An alias to :meth:`Environment.name`

        .. versionadded:: 1.5.0
        """
        return self.name

    @property
    def webhooks(self) -> List[Webhook]:
        """List[:class:`Webhook`]: Returns a list of webhooks.

        .. versionadded:: 1.5.0
        """
        return [Webhook(data, environment=self, client=self.client) for data in self._payload.get("webhooks")]

    def add_user_subscription(self, client: Client) -> None:
        """Add a new user subscription to the environment, which is the client (that you passed in the argument) itself.

        .. note::
            If you want to add other user subscription, use :class:`OauthSession.generate_oauth_url` to generate an oauth url and get the oauth token and verifier, then use :class:`OauthSession.post_oauth_token` to post the oauth token.


        .. versionadded:: 1.5.0
        """
        client.http.request("POST", "1.1", f"/account_activity/all/{self.label}/subscriptions.json", auth=True)

    def add_my_subscription(self) -> None:
        """Add a new user subscription to the environment, which is the client WHO made the environment request. Use :meth:`add_user_subscription` to add other user subscription. This method only add the client WHO made the fetch environment request.


        .. versionadded:: 1.5.0
        """
        self.client.http.request("POST", "1.1", f"/account_activity/all/{self.label}/subscriptions.json", auth=True)

    def register_webhook(self, url: str) -> Webhook:
        """Register your WebHook with your WebApp's url that you develop. Before this, you need to develop, deploy and host a WebApp that will receive Twitter webhook events. You also need to perform a Twitter Challenge Response Check (CRC) GET request and responds with a properly formatted JSON response.

        Parameters
        ------------
        url: :class:`str`
            Your WebApp url that you want to register as the WebHook url. Twitter will send account events to this url as an http post request.'

        Returns
        ---------
        :class:`Webhook`
            This method returns a :class:`Webhook` object.


        .. versionadded:: 1.5.0
        """
        res = self.client.http.request(
            "POST", "1.1", f"/account_activity/all/{self.label}/webhooks.json", auth=True, params={"url": url}
        )
        return Webhook(res, environment=self, client=self)

    def fetch_all_subscriptions(self) -> List[int]:
        """Returns a list of the the current users subscriptions from the environment.

        Returns
        ---------
        List[:class:`int`]
            This method returns a list of :class:`int` object.


        .. versionadded:: 1.5.0
        """
        res = self.client.http.request("GET", "1.1", f"/account_activity/all/{self.label}/subscriptions/list.json")

        return [int(subscription.get("user_id")) for subscription in res.get("subscriptions")]


class Webhook:
    """Represents a webhook for an environment. This webhook belongs to an environment and have a webhook url for sending account activity events.

    .. versionadded:: 1.5.0
    """

    __slots__ = ("_id", "_url", "_valid", "_environment", "client")

    def __init__(self, data: Dict[str, Any], *, environment: Environment, client: Client):
        self._id = data.get("id")
        self._url = data.get("url")
        self._valid = data.get("valid")
        self._environment = environment
        self.client = client

    def __repr__(self) -> str:
        return f"Webhook(id={self.id} url={self.url} valid={self.valid} environment={self.environment})"

    @property
    def id(self) -> int:
        """:class:`int`: Returns the webhook unique id.

        .. versionadded:: 1.5.0
        """
        return self._id

    @id.setter
    def id(self, obj: ID) -> None:
        self._id = obj

    @property
    def url(self) -> str:
        """:class:`str`: Returns the webhook url.

        .. versionadded:: 1.5.0
        """
        return self._url

    @url.setter
    def url(self, obj: str) -> None:
        self._url = obj

    @property
    def valid(self) -> bool:
        """:class:`bool`: Returns True if the webhook is valid else False.

        .. versionadded:: 1.5.0
        """
        return self._valid

    @valid.setter
    def valid(self, obj: bool) -> None:
        if not isinstance(obj, bool):
            raise ValueError("Webhook.valid setter method can only set bool object!")
        self._valid = obj

    @property
    def environment(self) -> Environment:
        """:class:`Environment`: Returns an environment where the webhook belongs to.

        .. versionadded:: 1.5.0
        """
        return self._environment

    @property
    def env(self):
        """:class:`Environment`: An alias to :meth:`Webhook.environment`

        .. versionadded:: 1.5.0
        """
        return self.environment

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns a datetime.datetime object with the webhook's created timestamp.

        .. versionadded:: 1.5.0
        """
        return time_parse_todt(self._payload.get("created_at"))

    def delete(self) -> Webhook:
        """Delete the webhook.

        Returns
        ---------
        :class:`Webhook`
            Returns the webhook object with the valid set to False.


        .. versionadded:: 1.5.0
        """
        self.client.http.request(
            "DELETE", "1.1", f"/account_activity/all/{self.env.label}/webhooks/{self.id}.json", auth=True
        )
        self.valid = False
        return self

    def trigger_crc(self) -> bool:
        """Trigger a challenge-response-checks to enable Twitter to confirm the ownership of the WebApp receiving webhook events. Will return True if its successful else False.

        Returns
        ---------
        :class:`bool`
            This method returns a :class:`bool` object.


        .. versionadded:: 1.5.0
        """
        _log.info("Triggering a CRC Challenge.")

        if not self.client.environment or not self.client.webhook:
            _log.warn("CRC Failed: client is not listening! use the listen method at the very end of your file!")
            return False

        self.client.http.request(
            "PUT", "1.1", f"/account_activity/all/{self.env.label}/webhooks/{self.id}.json", auth=True
        )
        _log.info("Successfully triggered a CRC.")
        return True
