from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass
class Channel:
    def __init__(self, client, data: dict) -> None:
        from .user import User, ThreadMember
        from ..utils import convert_iso

        self.id: int = int(data.get("id"))
        self.type: int = data.get("type")
        self.guild_id: Union[int, None] = int(
            data.get("guild_id")) if data.get("guild_id") else None
        self.position: Union[int, None] = data.get("position")
        self.permission_overwrites: Union[list, None] = data.get(
            "permission_overwrites")
        self.name: Union[str, None] = data.get("name")
        self.topic: Union[str, None] = data.get("topic")
        self.nsfw: Union[bool, None] = data.get("nsfw")
        self.last_message_id: Union[int, None] = int(
            data.get("last_message_id")) if data.get("last_message_id") else None
        self.bitrate: Union[int, None] = data.get("bitrate")
        self.user_limit: Union[int, None] = data.get("user_limit")
        self.rate_limit_per_user: Union[int,
                                        None] = data.get("rate_limit_per_user")
        self.recipients: Union[list, None] = [User(self.client, i) for i in data.get(
            "recipients")] if data.get("recipients") else None
        self.icon: Union[str, None] = data.get("icon")
        self.owner_id: Union[int, None] = int(
            data.get("owner_id")) if data.get("owner_id") else None
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") else None
        self.parent_id: Union[int, None] = int(
            data.get("parent_id")) if data.get("parent_id") else None
        self.last_pin_timestamp: Union[datetime, None] = convert_iso(
            data.get("last_pin_timestamp")) if data.get("last_pin_timestamp") else None
        self.rtc_region: Union[str, None] = data.get("rtc_region")
        self.video_quality_mode: Union[int,
                                       None] = data.get("video_quality_mode")
        self.message_count: Union[int, None] = data.get("message_count")
        self.member_count: Union[int, None] = data.get("member_count")
        self.thread_metadata: Union[dict, None] = data.get("thread_metadata")
        self.member: Union[ThreadMember, None] = ThreadMember(
            data.get("member")) if data.get("member") else None
        self.default_auto_archive_duration: Union[int, None] = data.get(
            "default_auto_archive_duration")
