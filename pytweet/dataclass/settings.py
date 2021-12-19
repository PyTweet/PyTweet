from dataclasses import dataclass
from typing import Optional
from .locations import Location, TimezoneInfo


@dataclass
class SleepTimeSettings:
    enabled: bool
    end_time: Optional[int]
    start_time: Optional[int]


@dataclass
class UserSettings:
    always_use_https: Optional[bool]
    geo_enabled: Optional[bool]
    sleep_time_setting: SleepTimeSettings
    use_cookie_personalization: Optional[bool]
    language: Optional[str]
    discoverable_by_email: Optional[bool]
    discoverable_by_mobile_phone: Optional[bool]
    display_sensitive_media: Optional[bool]
    allow_contributor_request: Optional[str]
    allow_dms_from: Optional[str]
    allow_dm_groups_from: Optional[str]
    protected: Optional[bool]
    translator_type: Optional[str]
    screen_name: Optional[str]
    show_all_inline_media: Optional[bool] = None
    location: Optional[Location] = None
    timezone: Optional[TimezoneInfo] = None
