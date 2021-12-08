from typing import Any, Dict

from .events import (
    DirectMessageTypingEvent, 
    UserFollowActionEvent,
    UserUnfollowActionEvent
)
from .message import DirectMessage
from .user import User
from .client import ApplicationInfo


class PayloadParser:
    def parse_user_payload(self, payload: Dict[str, Any]):
        copy = payload.copy()
        copy["public_metrics"] = {
            "followers_count": copy.get("followers_count"),
            "following_count": copy.get("friends_count"),
            "tweet_count": copy.get("statuses_count"),
            "listed_count": 0,
        }
        if "created_timestamp" in copy.keys():
            copy["created_at"] = copy.get("created_timestamp")
        if "screen_name" in copy.keys():
            copy["username"] = copy.get("screen_name")

        if "profile_image_url_https" in copy.keys():
            copy["profile_image_url"] = copy.get("profile_image_url_https")
        return copy


class EventParser:
    def __init__(self, http_client: object):
        self.http_client = http_client
        self.payload_parser = PayloadParser()

    def parse_direct_message_create(self, direct_message_payload: Dict[str, Any]):
        event_payload = {"event": direct_message_payload.get("direct_message_events")[0]}
        users = direct_message_payload.get("users")

        message_create = event_payload["event"].get("message_create")
        recipient_id = message_create.get("target").get("recipient_id")
        sender_id = message_create.get("sender_id")

        recipient = User(self.payload_parser.parse_user_payload(users.get(recipient_id)), http_client=self.http_client)
        sender = User(self.payload_parser.parse_user_payload(users.get(sender_id)), http_client=self.http_client)
        source_app = ApplicationInfo(direct_message_payload.get("apps"))


        event_payload["event"]["message_create"]["target"]["recipient"] = recipient
        event_payload["event"]["message_create"]["target"]["sender"] = sender
        event_payload["event"]["message_create"]["target"]["source_application"] = source_app

        direct_message = DirectMessage(
            event_payload, http_client=self.http_client
        )
        client_id = int(self.http_client.access_token.partition("-")[0])

        if recipient.id != client_id:
            self.http_client.user_cache[recipient.id] = recipient

        if sender.id != client_id:
            self.http_client.user_cache[sender.id] = sender

        self.http_client.message_cache[direct_message.id] = direct_message
        self.http_client.dispatch("direct_message", direct_message)

    def parse_user_follow(self, follow_payload: Dict[str, Any]):
        follow_payload = follow_payload.copy()
        event_payload = follow_payload.get("follow_events")[0]
        action_type = event_payload.get("type")
        target = User(self.payload_parser.parse_user_payload(event_payload.get("target")), http_client=self.http_client)
        source = User(self.payload_parser.parse_user_payload(event_payload.get("source")), http_client=self.http_client)

        event_payload["target"] = target
        event_payload["source"] = source
        client_id = int(self.http_client.access_token.partition("-")[0])
        if target.id != client_id:
            self.http_client.user_cache[target.id] = target

        if source.id != client_id:
            self.http_client.user_cache[source.id] = source

        if action_type == "follow":
            action = UserFollowActionEvent(follow_payload)
            self.http_client.dispatch("user_follow", action)
        elif action_type == "unfollow":
            action = UserUnfollowActionEvent(follow_payload)
            self.http_client.dispatch("user_unfollow", action)

    def parse_direct_message_typing(self, typing_payload: Dict[str, Any]):
        event_payload = typing_payload.get("direct_message_indicate_typing_events")[0]
        users = typing_payload.get("users")

        recipient_id = event_payload.get("target").get("recipient_id")
        sender_id = event_payload.get("sender_id")
        recipient = User(self.payload_parser.parse_user_payload(users.get(recipient_id)), http_client=self.http_client)
        sender = User(self.payload_parser.parse_user_payload(users.get(sender_id)), http_client=self.http_client)

        event_payload["target"]["recipient"] = recipient
        event_payload["target"]["sender"] = sender
        client_id = int(self.http_client.access_token.partition("-")[0])

        if recipient.id != client_id:
            self.http_client.user_cache[recipient.id] = recipient

        if sender.id != client_id:
            self.http_client.user_cache[sender.id] = sender

        payload = DirectMessageTypingEvent(event_payload)
        self.http_client.dispatch("typing", payload)