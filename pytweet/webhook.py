from typing import Dict, Any
from .utils import time_parse_todt


class Webhook:
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def id(self) -> int:
        return int(self._payload.get("id"))

    @property
    def url(self) -> str:
        return self._payload.get("url")

    @property
    def valid(self) -> bool:
        return self._payload.get("valid")

    @property
    def created_at(self) -> int:
        return time_parse_todt(self._payload.get("created_at"))


class Environment:
    def __init__(self, data: Dict[str, Any]):
        self._payload = data

    @property
    def name(self) -> str:
        return self._payload.get("environment_name")

    @property
    def label(self) -> str:
        return self.name

    @property
    def webhooks(self):
        return [Webhook(data) for data in self._payload.get("webhooks")]
