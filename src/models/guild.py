"""
Models for guild and other related stuff.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Union

from aiohttp.formdata import FormData

from ..utils import convert_iso, dict_to_query


@dataclass
class Guild:
    """Guild class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes are same with https://discord.com/developers/docs/resources/guild#guild-object-guild-structure
    """

    def __init__(self, client, data: dict) -> None:
        from .user import Member
        from .channel import Channel

        self.client = client

        self.id: int = int(data.get("id"))
        self.name: str = data.get("name")
        self.icon: Union[str, None] = data.get("icon")
        self.icon_hash: Union[str, None] = data.get("icon_hash")
        self.splash: Union[str, None] = data.get("splash")
        self.discovery_splash: Union[str, None] = data.get("discovery_splash")
        self.owner: Union[bool, None] = data.get("owner")
        self.owner_id: Union[int, None] = int(
            data.get("owner_id")) if data.get("owner_id") is not None else None
        self.permissions: Union[str, None] = data.get("permissions")
        self.region: Union[str, None] = data.get("region")
        self.afk_channel_id: Union[int, None] = int(
            data.get("afk_channel_id")) if data.get("afk_channel_id") is not None else None
        self.afk_timeout: int = data.get("afk_timeout")
        self.widget_enabled: Union[bool, None] = data.get("widget_enabled")
        self.widget_channel_id: Union[int, None] = int(
            data.get("widget_channel_id")) if data.get("widget_channel_id") is not None else None
        self.verification_level: int = data.get("verification_level")
        self.default_message_notifications: int = data.get(
            "default_message_notifications")
        self.explicit_content_filter: int = data.get("explicit_content_filter")
        self.roles: list = [Role(i) for i in data.get("roles")]
        self.emojis: list = [Emoji(self.client, i) for i in data.get("emojis")]
        self.features: list = data.get("features")
        self.mfa_level: int = data.get("mfa_level")
        self.application_id: Union[int, None] = int(
            data.get("application_id")) if data.get("application_id") is not None else None
        self.system_channel_id: Union[int, None] = int(
            data.get("system_channel_id")) if data.get("system_channel_id") is not None else None
        self.system_channel_flags: Union[int, None] = data.get(
            "system_channel_flags")
        self.rules_channel_id: Union[int, None] = int(
            data.get("rules_channel_id")) if data.get("rules_channel_id") is not None else None
        self.joined_at: Union[datetime, None] = convert_iso(
            data.get("joined_at")) if data.get("joined_at") is not None else None
        self.large: Union[bool, None] = data.get("large")
        self.unavailable: Union[bool, None] = data.get("unavailable")
        self.member_count: Union[int, None] = data.get("member_count")
        self.voice_states: Union[list, None] = data.get("voice_states")
        self.members: Union[list, None] = [Member(self.client, i) for i in data.get(
            "members")] if data.get("members") is not None else None
        self.channels: Union[list, None] = [Channel(self.client, i) for i in data.get(
            "channels")] if data.get("channels") is not None else None
        self.threads: Union[list, None] = [Channel(self.client, i) for i in data.get(
            "threads")] if data.get("threads") is not None else None
        self.presences: Union[list, None] = data.get("presences")
        self.max_presences: Union[int, None] = data.get("max_presences")
        self.max_members: Union[int, None] = data.get("max_members")
        self.vanity_url_code: Union[str, None] = data.get("vanity_url_code")
        self.description: Union[str, None] = data.get("description")
        self.banner: Union[str, None] = data.get("banner")
        self.premium_tier: int = data.get("premium_tier")
        self.premium_subscription_count: Union[int, None] = data.get(
            "premium_subscription_count")
        self.preferred_locale: str = data.get("preferred_locale")
        self.public_updates_channel_id: Union[int, None] = int(data.get(
            "public_updates_channel_id")) if data.get("public_updates_channel_id") is not None else None
        self.max_video_channel_users: Union[int, None] = data.get(
            "max_video_channel_users")
        self.approximate_member_count: Union[int, None] = data.get(
            "approximate_member_count")
        self.approximate_presence_count: Union[int, None] = data.get(
            "approximate_presence_count")
        self.welcome_screen: Union[dict, None] = data.get("welcome_screen")
        self.nsfw_level: int = data.get("nsfw_level")
        self.stage_instances: Union[list, None] = data.get("stage_instances")

    async def edit(self, **kwargs):
        """Modify the Guild with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#modify-guild-json-params

        Returns:
            Guild: Updated guild object.
        """

        result = await self.client.http.request("PATCH", f"/guilds/{self.id}", json=kwargs)
        return Guild(self.client, result)

    async def delete(self):
        """Delete the Guild.

        Returns:
            True: Guild deleted successfully.
        """

        await self.client.http.request("DELETE", f"/guilds/{self.id}")
        return True

    async def fetch_emojis(self):
        """Fetch all emojis in the Guild.

        Returns:
            list: List of Emoji objects.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/emojis")
        return [Emoji(self.client, i) for i in result]

    async def fetch_emoji(self, emoji_id: int):
        """Fetch a emoji from Guild.

        Args:
            emoji_id (int): Emoji ID.

        Returns:
            Emoji: Found emoji object.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/emojis/{emoji_id}")
        return Emoji(self.client, result)

    async def create_emoji(self, **kwargs):
        """Create a Guild emoji.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/emoji#create-guild-emoji-json-params (for image, use `krema.utils.image_to_data_uri` function.)

        Returns:
            Emoji: Created Emoji object.
        """

        result = await self.client.http.request("POST", f"/guilds/{self.id}/emojis", json=kwargs)
        return Emoji(self.client, result)

    async def update_emoji(self, emoji_id: int, **kwargs):
        """Update a Guild emoji.

        Args:
            emoji_id (int): Emoji ID.
            **kwargs: https://discord.com/developers/docs/resources/emoji#modify-guild-emoji-json-params

        Returns:
            Emoji: Updated Emoji object.
        """

        result = await self.client.http.request("PATCH", f"/guilds/{self.id}/emojis/{emoji_id}", json=kwargs)
        return Emoji(self.client, result)

    async def delete_emoji(self, emoji_id: int):
        """Delete a Guild emoji.

        Args:
            emoji_id (int): Emoji ID.

        Returns:
            True: Emoji deleted successfully.
        """

        await self.client.http.request("DELETE", f"/guilds/{self.id}/emojis/{emoji_id}")
        return True

    async def fetch_channels(self):
        """Fetch all Guild Channels.

        Returns:
            list: List of Channel objects. (Threads does not included.)
        """

        from .channel import Channel

        result = await self.client.http.request("GET", f"/guilds/{self.id}/channels")
        return [Channel(self.client, i) for i in result]

    async def create_channel(self, **kwargs):
        """Create Guild Channel with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#create-guild-channel-json-params

        Returns:
            Channel: Created Channel object.
        """

        from .channel import Channel

        result = await self.client.http.request("POST", f"/guilds/{self.id}/channels", json=kwargs)
        return Channel(self.client, result)

    async def modify_channel_positions(self, parameters: list):
        """Modifiy Guild Channel positions with API params.

        Args:
            parameters: JSON list that contains https://discord.com/developers/docs/resources/guild#modify-guild-channel-positions-json-params objects.

        Returns:
            True: Channel positions modified successfully.
        """

        await self.client.http.request("PATCH", f"/guilds/{self.id}/channels", json=parameters)
        return True

    async def fetch_member(self, member_id: int):
        """Fetch a Member from Guild.

        Args:
            member_id (int): Member ID.

        Returns:
            Member: Found Member.
        """

        from .user import Member

        result = await self.client.http.request("GET", f"/guilds/{self.id}/members/{member_id}")
        return Member(self.client, result)

    async def fetch_member_list(self, **kwargs):
        """Fetch list of Guild Member with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#list-guild-members-query-string-params

        Returns:
            list: List of Guild Members.
        """

        from .user import Member

        result = await self.client.http.request("GET", f"/guilds/{self.id}/members{dict_to_query(kwargs)}")
        return [Member(self.client, i) for i in result]

    async def search_member(self, **kwargs):
        """Search Guild Member with API params.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#search-guild-members-query-string-params

        Returns:
            list: List of Guild Members.
        """

        from .user import Member

        if "limit" not in kwargs:
            kwargs["limit"] = 25

        result = await self.client.http.request("GET", f"/guilds/{self.id}/members/search{dict_to_query(kwargs)}")
        return [Member(self.client, i) for i in result]

    async def edit_member(self, member_id: int, **kwargs):
        """Edit a Guild Member with API params.

        Args:
            member_id (int): Member ID.
            **kwargs: https://discord.com/developers/docs/resources/guild#modify-guild-member-json-params

        Returns:
            Member: Updated Guild Member.
        """

        from .user import Member

        result = await self.client.http.request("PATCH", f"/guilds/{self.id}/members/{member_id}", json=kwargs)
        return Member(self.client, result)

    async def add_member_role(self, member_id: int, role_id: int):
        """Add a Role to Guild Member.

        Args:
            member_id (int): Member ID.
            role_id (int): Role ID.

        Returns:
            True: Added role to Member successfully.
        """

        await self.client.http.request("PUT", f"/guilds/{self.id}/members/{member_id}/roles/{role_id}")
        return True

    async def remove_member_role(self, member_id: int, role_id: int):
        """Remove a Role from Guild Member.

        Args:
            member_id (int): Member ID.
            role_id (int): Role ID.

        Returns:
            True: Removed role from Member successfully.
        """

        await self.client.http.request("DELETE", f"/guilds/{self.id}/members/{member_id}/roles/{role_id}")
        return True

    async def kick_member(self, member_id: int, reason: str = None):
        """Kick Member from Guild.

        Args:
            member_id (int): Member ID.
            reason (str, optional): Kick reason.

        Returns:
            True: Member is kicked successfully.
        """

        extra = {}

        if reason is not None:
            extra["log_reason"] = reason

        await self.client.http.request("DELETE", f"/guilds/{self.id}/members/{member_id}", **extra)
        return True

    async def ban_member(self, member_id: int, reason: str = None, **kwargs):
        """Ban Member from Guild.

        Args:
            member_id (int): Member ID.
            reason (str, optional): Ban reason.
            **kwargs: https://discord.com/developers/docs/resources/guild#create-guild-ban-json-params

        Returns:
            True: Member is banned successfully.
        """

        extra = {"json": kwargs}

        if reason is not None:
            extra["log_reason"] = reason

        await self.client.http.request("PUT", f"/guilds/{self.id}/bans/{member_id}", **extra)
        return True

    async def fetch_bans(self):
        """Fetch all bans from Guild.

        Returns:
            list: List of Ban object.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/bans")
        return [Ban(self.client, i) for i in result]

    async def fetch_ban(self, member_id: int):
        """Fetch a member ban from Guild.

        Args:
            member_id (int): Member ID.

        Returns:
            Ban: Found member's ban object.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/bans/{member_id}")
        return Ban(self.client, result)

    async def unban_member(self, member_id: int, reason: str = None):
        """Un-ban a Member from Guild.

        Args:
            member_id (int): Member ID.
            reason (str, optional): un-ban reason.

        Returns:
            True: Member is un-banned successfully.
        """

        extra = {}

        if reason is not None:
            extra["log_reason"] = reason

        await self.client.http.request("DELETE", f"/guilds/{self.id}/bans/{member_id}", **extra)
        return True

    async def fetch_roles(self):
        """Fetch all Guild Roles.

        Returns:
            list: List of Role objects.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/roles")
        return [Role(i) for i in result]

    async def create_role(self, **kwargs):
        """Fetch all Guild Roles.

        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#create-guild-role-json-params

        Returns:
            Role: Created Role object.
        """

        result = await self.client.http.request("POST", f"/guilds/{self.id}/roles", json=kwargs)
        return Role(result)

    async def modify_role_positions(self, parameters: list):
        """Modifiy Guild Role positions with API params.

        Args:
            parameters: JSON list that contains https://discord.com/developers/docs/resources/guild#modify-guild-role-positions-json-params objects.

        Returns:
            list: List of all Guild Roles.
        """

        result = await self.client.http.request("PATCH", f"/guilds/{self.id}/roles", json=parameters)
        return [Role(i) for i in result]

    async def edit_role(self, role_id: int, **kwargs):
        """Edit a Guild Role.

        Args:
            role_id (int): Role ID.
            **kwargs: https://discord.com/developers/docs/resources/guild#modify-guild-role-json-params.

        Returns:
            Role: Updated Guild Role.
        """

        result = await self.client.http.request("PATCH", f"/guilds/{self.id}/roles/{role_id}", json=kwargs)
        return Role(result)

    async def delete_role(self, role_id: int):
        """Delete a Guild Role.

        Args:
            role_id (int): Role ID.

        Returns:
            True: Role deleted successfully.
        """

        await self.client.http.request("DELETE", f"/guilds/{self.id}/roles/{role_id}")
        return True

    async def fetch_webhooks(self):
        """Fetch all Webhooks in the Guild.

        Returns:
            list: List of Webhook objects.
        """

        from .webhook import Webhook

        result = await self.client.http.request("GET", f"/guilds/{self.id}/webhooks")
        return [Webhook(self.client, i) for i in result]

    async def list_stickers(self):
        """List all of the stickers from Guild.

        Returns:
            list: List of Sticker objects.
        """

        from .sticker import Sticker

        result = await self.client.http.request("GET", f"/guilds/{self.id}/stickers")
        return [Sticker(self.client, i) for i in result]

    async def fetch_sticker(self, sticker_id: int):
        """Fetch Guild Sticker by ID.

        Returns:
            Sticker: Found sticker object.
        """

        from .sticker import Sticker

        result = await self.client.http.request("GET", f"/guilds/{self.id}/stickers/{sticker_id}")
        return Sticker(self.client, result)

    async def create_sticker(self, name: str, description: str, tags: str, image: str):
        """Create a Sticker.

        Args:
            name (str): Sticker name.
            description (str): Sticker description.
            tags (str): The Discord name of a unicode emoji representing the sticker's expression (2-200 characters)
            image (str): Image path to upload. (max 500kb.)

        Returns:
            Sticker: Created sticker object.
        """

        from .sticker import Sticker

        data = FormData()

        image_name = image.split('/')

        if len(image_name) == 1:
            image_name = image.split("\\")[-1]
        else:
            image_name = image_name[-1]

        with open(image, "rb") as f:
            image_data = f.read()

        data.add_field(name="name", value=name)
        data.add_field(name="description", value=description)
        data.add_field(name="tags", value=tags)
        data.add_field(name="file", value=image_data, filename=image_name,
                       content_type=f"image/{image.split('.')[-1].replace('jpg', 'jpeg')}")

        result = await self.client.http.request("POST", f"/guilds/{self.id}/stickers", data=data)
        return Sticker(self.client, result)

    async def fetch_application_command(self, command_id: int):
        """Fetch guild application command.

        Args:
            command_id (int): Command ID.

        Returns:
            ApplicationCommand: Found Command object.
        """

        from .client import ApplicationCommand

        result = await self.client.http.request("GET", f"/applications/{self.client.user.id}/guilds/{self.id}/commands/{command_id}")
        return ApplicationCommand(self.client, result)

    async def fetch_integrations(self):
        """Fetch guild integrations.

        Returns:
            list: List of Integration objects.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/integrations")
        return [Integration(self.client, i) for i in result]

    async def delete_integration(self, integration_id: int):
        """Fetch guild integrations.

        Args:
            integration_id (int): Integration Id.

        Returns:
            True: Integration deleted successfully.
        """

        await self.client.http.request("DELETE", f"/guilds/{self.id}/integrations/{integration_id}")
        return True

    async def fetch_vanity_url(self):
        """Fetch vanity url for guild.

        Returns:
            Invite: Partial invite object.
        """

        from .invite import Invite

        result = await self.client.http.request("GET", f"/guilds/{self.id}/vanity-url")
        return Invite(self.client, result)

    async def fetch_prune_count(self, **kwargs) -> int:
        """Fetch guild prune count.
        
        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#get-guild-prune-count-query-string-params.

        Returns:
            int: Total kickable user count.
        """

        result = await self.client.http.request("GET", f"/guilds/{self.id}/prune{dict_to_query(kwargs)}")
        return result.get("pruned")

    async def prune(self, **kwargs) -> int:
        """Begin guild prune.
        
        Args:
            **kwargs: https://discord.com/developers/docs/resources/guild#begin-guild-prune-json-params.

        Returns:
            int: Total kicked user count.
        """

        result = await self.client.http.request("POST", f"/guilds/{self.id}/prune", json=kwargs)
        return result.get("pruned")

@dataclass
class Emoji:
    """Emoji class.

    Attributes:
        id (int, None): Emoji ID.
        name (str, None): Emoji name.
        roles (list, None): Allowed roles list.
        user (User, None): Owner of the emoji.
        require_colons (bool, None): whether this emoji must be wrapped in colons.
        managed (bool, None): whether this emoji is managed.
        animated (bool, None): whether this emoji is animated.
        available (bool, None): "whether this emoji can be used, may be false due to loss of Server Boosts".
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.client = client

        self.id: Union[int, None] = int(
            data.get("id")) if data.get("id") is not None else None
        self.name: Union[str, None] = data.get("name")
        self.roles: Union[list, None] = data.get("roles")
        self.user: Union[User, None] = User(self.client, data.get(
            "user")) if data.get("user") is not None else None
        self.require_colons: Union[bool, None] = data.get("require_colons")
        self.managed: Union[bool, None] = data.get("managed")
        self.animated: Union[bool, None] = data.get("animated")
        self.available: Union[bool, None] = data.get("available")


@dataclass
class Ban:
    """Ban class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet from websocket.

    Attributes:
        client (Client): Krema client.
        reason (str, None): Ban reason.
        user (User): Banned user object.
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.client = client

        self.reason: Union[str, None] = data.get("reason")
        self.user: User = User(self.client, data.get("user"))


@dataclass
class Role:
    """Role class.

    Args:
        data (dict): Sent packet.

    Attributes:
        id (int): Role id.
        name (str): Role name.
        color (int): Role color.
        hoist (bool): If this role is pinned in the user listing.
        position (int): Role position.
        permissions (str): Role permissions bitvise value.
        managed (bool): Whether this role is managed by an integration.
        mentionable (bool): Whether this role is mentionable.
        tags (dict, None): The tags this role has.
    """

    def __init__(self, data: dict) -> None:
        self.id: int = int(data.get("id"))
        self.name: str = data.get("name")
        self.color: int = data.get("color")
        self.hoist: bool = data.get("hoist")
        self.position: int = data.get("position")
        self.permissions: str = data.get("permissions")
        self.managed: bool = data.get("managed")
        self.mentionable: bool = data.get("mentionable")
        self.tags: Union[dict, None] = data.get("tags")


@dataclass
class Integration:
    """Integration class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet.

    Attributes:
        client (Client): Krema client.
        id (int): Integration Id.
        name (str): Integration name.
        type (str): Integration type (twitch, youtube, or discord).
        enabled (bool): Is this integration enabled.
        syncing (bool, None): Is this integration syncing.
        role_id (int, None): Id that this integration uses for "subscribers".
        enable_emoticons (bool, None): Whether emoticons should be synced for this integration.
        expire_behavior (int, None): The behavior of expiring subscribers.
        expire_grace_period (int, None): The grace period (in days) before expiring subscribers .
        user (User, None): User for this integration.
        account (dict): Integration account information.
        synced_at (datetime, None): When this integration was last synced.
        subscriber_count (int, None): How many subscribers this integration has.
        revoked (bool, None): Has this integration been revoked.
        application (IntegrationApplication, None): The bot/OAuth2 application for discord integrations.
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.id: int = int(data.get("id"))
        self.name: str = data.get("name")
        self.type: str = data.get("type")
        self.enabled: bool = data.get("enabled")
        self.syncing: Union[bool, None] = data.get("syncing")
        self.role_id: int = int(data.get("role_id")) if data.get(
            "role_id") is not None else None
        self.enable_emoticons: Union[bool, None] = data.get("enable_emoticons")
        self.expire_behavior: Union[int, None] = data.get("expire_behavior")
        self.expire_grace_period: Union[int,
                                        None] = data.get("expire_grace_period")
        self.user: Union[User, None] = User(client, data.get(
            "user")) if data.get("user") is not None else None
        self.account: dict = data.get("account")
        self.synced_at: Union[datetime, None] = convert_iso(
            data.get("synced_at")) if data.get("synced_at") is not None else None
        self.subscriber_count: Union[int, None] = data.get("subscriber_count")
        self.revoked: Union[bool, None] = data.get("revoked")
        self.application: Union[IntegrationApplication, None] = IntegrationApplication(
            client, data.get("application")) if data.get("application") is not None else None


@dataclass
class IntegrationApplication:
    """Integration application class.

    Args:
        client (Client): Krema client.
        data (dict): Sent packet.

    Attributes:
        client (Client): Krema client.
        id (int): App Id.
        name (str): App name.
        icon (str, None): App icon hash.
        description (str): App description.
        summary (str): App summary.
        bot (User, None): The bot associated with this application.
    """

    def __init__(self, client, data: dict) -> None:
        from .user import User

        self.id: int = int(data.get("id"))
        self.name: str = data.get("string")
        self.icon: Union[str, None] = data.get("icon")
        self.description: str = data.get("description")
        self.summary: str = data.get("summary")
        self.bot: Union[User, None] = User(client, data.get(
            "bot")) if data.get("bot") is not None else None
