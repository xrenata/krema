from dataclasses import dataclass
from datetime import datetime
from typing import Union

@dataclass
class Message:
    def __init__(self, client, data: dict) -> None:
        from ..utils import convert_iso
        from .user import User, Member
        
        self.client = client
    
        self.id: int = int(data.get("id"))
        self.channel_id: int = int(data.get("channel_id"))
        self.guild_id: Union[int, None] = int(data.get("guild_id")) if data.get("guild_id") else None
        self.author: Union[User, int, None] = User(self.client, data.get("author")) if data.get("author") else None
        self.member: Union[Member, int, None] = Member(self.client, data.get("author")) if data.get("author") else None
        self.content: str = data.get("content")
        self.timestamp: datetime = convert_iso(data.get("timestamp"))
        self.edited_timestamp: Union[datetime, None] = convert_iso(data.get("edited_timestamp")) if data.get("edited_timestamp") else None
        self.tts: bool = data.get("tts")
        self.mention_everyone: bool = data.get("mention_everyone")
        self.mentions: list = data.get("mentions")

        print(self.mentions)