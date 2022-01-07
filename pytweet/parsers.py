from __future__ import annotations
from typing import TYPE_CHECKING

from .events import (
    DirectMessageTypingEvent,
    DirectMessageReadEvent,
    TweetFavoriteActionEvent,
    UserFollowActionEvent,
    UserUnfollowActionEvent,
    UserBlockActionEvent,
    UserUnblockActionEvent,
    UserMuteActionEvent,
    UserUnmuteActionEvent,
)
from .message import Message, DirectMessage
from .user import User
from .app import ApplicationInfo
from .tweet import Tweet
from .dataclass import TimezoneInfo, Location, SleepTimeSettings

if TYPE_CHECKING:
    from .type import Payload


class PayloadParser:
    def parse_user_payload(self, payload: Payload):
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

    def parse_tweet_payload(self, payload: Payload):
        copy = payload.copy()
        copy["public_metrics"] = {
            "quote_count": payload.get("quote_count"),
            "reply_count": payload.get("reply_count"),
            "retweet_count": payload.get("retweet_count"),
            "like_count": payload.get("favorite_count"),
        }
        copy["includes"] = {}
        copy["includes"]["mentions"] = [user.get("screen_name") for user in copy.get("entities").get("user_mentions")]

        if "timestamp_ms" in payload.keys():
            copy["timestamp"] = payload.get("timestamp_ms")

        if "user" in payload.keys():
            copy["includes"]["users"] = [self.parse_user_payload(payload.get("user"))]

        return copy

    def parse_time_zone_payload(self, payload: Payload):
        copy = payload.copy
        _timezone = copy.get("time_zone")
        _timezone["name_info"] = _timezone.get("tzinfo_name")
        _timezone.pop("tzinfo_name")
        copy["timezone"] = TimezoneInfo(**copy.get("time_zone"))
        copy.pop("time_zone")
        return copy

    def parse_trend_location_payload(self, payload: Payload):
        copy = payload.copy()["trend_location"]
        copy["place_type"] = copy["placeType"]
        copy["country_code"] = copy["countryCode"]
        copy.pop("placeType")
        copy.pop("countryCode")
        copy["location"] = Location(**copy)
        return copy

    def parse_sleep_time_payload(self, payload: Payload):
        copy = payload.copy()
        copy["sleep_time_setting"] = SleepTimeSettings(**copy["sleep_time"])
        copy.pop("sleep_time")
        return copy


class EventParser:
    __slots__ = ("payload_parser", "http_client", "client_id")

    def __init__(self, http_client: object):
        self.payload_parser = PayloadParser()
        self.http_client = http_client
        self.client_id = int(self.http_client.access_token.partition("-")[0])

    def parse_direct_message_create(self, direct_message_payload: Payload):
        event_payload = {"event": direct_message_payload.get("direct_message_events")[0]}
        users = direct_message_payload.get("users")

        message_create = event_payload["event"].get("message_create")
        recipient_id = message_create.get("target").get("recipient_id")
        sender_id = message_create.get("sender_id")

        recipient = User(self.payload_parser.parse_user_payload(users.get(recipient_id)), http_client=self.http_client)
        sender = User(self.payload_parser.parse_user_payload(users.get(sender_id)), http_client=self.http_client)
        application_info = direct_message_payload.get("apps")
        if application_info:
            source_app = ApplicationInfo({"apps": direct_message_payload.get("apps")})

        else:
            source_app = None

        event_payload["event"]["message_create"]["target"]["recipient"] = recipient
        event_payload["event"]["message_create"]["target"]["sender"] = sender
        event_payload["event"]["message_create"]["target"]["source_application"] = source_app

        direct_message = DirectMessage(event_payload, http_client=self.http_client)

        if recipient.id != self.client_id:
            self.http_client.user_cache[recipient.id] = recipient

        if sender.id != self.client_id:
            self.http_client.user_cache[sender.id] = sender

        self.http_client.message_cache[direct_message.id] = direct_message
        self.http_client.dispatch("direct_message", direct_message)

    def parse_direct_message_typing(self, typing_payload: Payload):
        event_payload = typing_payload.get("direct_message_indicate_typing_events")[0]
        users = typing_payload.get("users")

        recipient_id = event_payload.get("target").get("recipient_id")
        sender_id = event_payload.get("sender_id")
        recipient = User(self.payload_parser.parse_user_payload(users.get(recipient_id)), http_client=self.http_client)
        sender = User(self.payload_parser.parse_user_payload(users.get(sender_id)), http_client=self.http_client)

        event_payload["target"]["recipient"] = recipient
        event_payload["target"]["sender"] = sender

        if recipient.id != self.client_id:
            self.http_client.user_cache[recipient.id] = recipient

        if sender.id != self.client_id:
            self.http_client.user_cache[sender.id] = sender

        payload = DirectMessageTypingEvent(event_payload, http_client=self.http_client)
        self.http_client.dispatch("typing", payload)

    def parse_direct_message_read(self, read_payload: Payload):
        event_payload = read_payload.get("direct_message_mark_read_events")[0]
        users = read_payload.get("users")

        recipient_id = event_payload.get("target").get("recipient_id")
        sender_id = event_payload.get("sender_id")
        recipient = User(self.payload_parser.parse_user_payload(users.get(recipient_id)), http_client=self.http_client)
        sender = User(self.payload_parser.parse_user_payload(users.get(sender_id)), http_client=self.http_client)

        event_payload["target"]["recipient"] = recipient
        event_payload["target"]["sender"] = sender

        if recipient.id != self.client_id:
            self.http_client.user_cache[recipient.id] = recipient

        if sender.id != self.client_id:
            self.http_client.user_cache[sender.id] = sender

        payload = DirectMessageReadEvent(event_payload, http_client=self.http_client)
        self.http_client.dispatch("read", payload)

    def parse_user_action(self, action_payload: Payload, action_type):
        action_payload = action_payload.copy()
        event_payload = action_payload.get(action_type)[0]
        action_type = event_payload.get("type")
        target = User(self.payload_parser.parse_user_payload(event_payload.get("target")), http_client=self.http_client)
        source = User(self.payload_parser.parse_user_payload(event_payload.get("source")), http_client=self.http_client)

        event_payload["target"] = target
        event_payload["source"] = source

        if target.id != self.client_id:
            self.http_client.user_cache[target.id] = target

        if source.id != self.client_id:
            self.http_client.user_cache[source.id] = source

        if action_type == "follow":
            action = UserFollowActionEvent(action_payload)
            self.http_client.dispatch("user_follow", action)

        elif action_type == "unfollow":
            action = UserUnfollowActionEvent(action_payload)
            self.http_client.dispatch("user_unfollow", action)

        elif action_type == "block":
            action = UserBlockActionEvent(action_payload)
            self.http_client.dispatch("user_block", action)

        elif action_type == "unblock":
            action = UserUnblockActionEvent(action_payload)
            self.http_client.dispatch("user_unblock", action)

        elif action_type == "mute":
            action = UserMuteActionEvent(action_payload)
            self.http_client.dispatch("user_mute", action)

        elif action_type == "unmute":
            action = UserUnmuteActionEvent(action_payload)
            self.http_client.dispatch("user_unmute", action)

    def parse_tweet_create(self, tweet_payload: Payload):
        tweet_payload = self.payload_parser.parse_tweet_payload(tweet_payload.get("tweet_create_events")[0])
        tweet = Tweet(tweet_payload, http_client=self.http_client)
        self.http_client.tweet_cache[tweet.id] = tweet
        self.http_client.dispatch("tweet_create", tweet)

    def parse_tweet_delete(self, tweet_payload: Payload):
        event_payload = tweet_payload.get("tweet_delete_events")[0]
        tweet_id = event_payload.get("status").get("id")
        tweet = self.http_client.tweet_cache.get(int(tweet_id))
        if not tweet:
            message = Message(None, tweet_id, 1)
            return self.http_client.dispatch("tweet_delete", message)

        try:
            self.http_client.tweet_cache.pop(int(tweet_id))
        except KeyError:
            pass
        finally:
            tweet.deleted_timestamp = int(event_payload.get("timestamp_ms"))
            self.http_client.dispatch("tweet_delete", tweet)

    def parse_favorite_tweet(self, favorite_payload: Payload):
        action_payload = favorite_payload.copy()
        event_payload = favorite_payload.get("favorite_events")[0]
        tweet = Tweet(self.payload_parser.parse_tweet_payload(event_payload.get("favorited_status")))
        user = User(self.payload_parser.parse_user_payload(event_payload.get("user")))
        event_payload["tweet"] = tweet
        event_payload["liker"] = user

        if user.id != self.client_id:
            self.http_client.user_cache[user.id] = user

        action = TweetFavoriteActionEvent(action_payload)
        self.http_client.dispatch("tweet_favorite", action)
