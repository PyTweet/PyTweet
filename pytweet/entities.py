from typing import Any, Dict, Optional


class Hashtags:
    def __init__(self, data=Dict[str, Any]):
        self.payload = data
        if self.payload:
            self.text = self.payload.get("text")
            self.startpoint, self.endpoint = self.payload.get("indices")


class UserMentions:
    def __init__(self, data=Dict[str, Any]):
        self.payload: Dict[str, Any] = data
        if self.payload:
            self.name: str = self.payload.get("name")
            self.screen_name: str = self.payload.get("screen_name")
            self.id: int = self.payload.get("id")
            self.startpoint, self.endpoint = self.payload.get("indices")


class Urls:
    def __init__(self, data=Dict[str, Any]):
        self.payload: Dict[str, Any] = data
        if self.payload:
            self.url: str = self.payload.get("url")
            self.display_url: str = self.payload.get("display_url")
            self.expanded_url: str = self.payload.get("expanded_url")
            self.startpoint, self.endpoint = self.payload.get("indices")


class Symbols:
    def __init__(self, data=Optional[Dict[str, Any]]):
        self.payload: Dict[str, Any] = data
        if self.payload:
            self.text: str = self.payload.get("text")
            self.startpoint, self.endpoint = self.payload.get("indices")
