from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class EmbedBuilder:
    """Embed builder class.

    Args:
        data (dict, None): The data for the embed.

    Attributes:
        color (int): Embed color.
        title (str): Embed title.
        description (str): Embed description.
        url (str): Embed title url.
        author (dict): Embed author.
        image (dict): Embed image.
        thumbnail (dict): Embed thumbnail.
        timestamp (str): Embed timestamp in iso format.
        fields (list): List of fields.
        footer (dict): Embed footer.
        embed (dict): Builded embed.
    """

    def __init__(self, data: Optional[dict] = None) -> None:
        if data is None:
            data = {}

        self.color: int = data.get("color", 0)
        self.title: str = data.get("title", "")
        self.description: str = data.get("description", "")
        self.url: str = data.get("url", "")
        self.author: dict = data.get("author", {})
        self.image: dict = data.get("image", {})
        self.thumbnail: dict = data.get("thumbnail", {})
        self.timestamp: str = data.get("timestamp", "")
        self.fields: list = data.get("fields", [])
        self.footer: dict = data.get("footer", {})

        self.embed: dict = {}

    def __call__(self):
        self.embed = {}

        if self.title:
            self.embed["title"] = self.title

        if self.url:
            self.embed["url"] = self.url

        if self.color:
            self.embed["color"] = self.color

        if self.description:
            self.embed["description"] = self.description

        if self.author:
            self.embed["author"] = self.author

        if self.thumbnail:
            self.embed["thumbnail"] = self.thumbnail

        if self.image:
            self.embed["image"] = self.image

        if self.timestamp:
            self.embed["timestamp"] = self.timestamp

        if self.footer:
            self.embed["footer"] = self.footer

        if self.footer:
            self.embed["footer"] = self.footer

        if self.fields:
            self.embed["fields"] = self.fields

        return self.embed

    def set_author(self, **kwargs):
        """Set author to the embed.

        Args:
            text (str, None): Author text.
            icon_url (str, None): Author icon url.
            url (str, None): Author url.
        """

        self.author = {}

        if "text" in kwargs:
            self.author["name"] = kwargs["text"]

        if "icon_url" in kwargs:
            self.author["icon_url"] = kwargs["icon_url"]

        if "url" in kwargs:
            self.author["url"] = kwargs["url"]

    def set_footer(self, text: str, icon_url: Optional[str] = None):
        """Set footer to the embed.

        Args:
            text (str): Footer text.
            icon_url (str, None): Footer icon urk.
        """

        self.footer = {
            "text": text,
            "icon_url": icon_url
        }

        if icon_url is None:
            del self.footer["icon_url"]

    def set_image(self, url: str):
        """Set image to the embed.

        Args:
            url (str): Image url.
        """

        self.image = {"url": url}

    def set_thumbnail(self, url: str):
        """Set thumbnail to the embed.

        Args:
            url (str): Thumbnail url.
        """

        self.thumbnail = {"url": url}

    def set_timestamp(self):
        """Add current timestamp to the embed."""

        self.timestamp = datetime.utcnow().isoformat()

    def add_field(self, name: str, value: str, inline: bool = True):
        """Add new field to the embed.

        Args:
            name (str): Field name.
            value (str): Field value.
            inline (bool): Field inline value (defaul true).
        """

        if not self.fields:
            self.fields = []

        self.fields.append({
            "name": name,
            "value": value,
            "inline": inline
        })
