import tomllib
from pathlib import Path

from models import Channel

CHANNELS_FILE = Path(__file__).with_name("channels.toml")


class ChannelRepository:
    def __init__(self, channels_file: Path = CHANNELS_FILE):
        with open(channels_file, "rb") as file:
            groups = tomllib.load(file)

        self.channels: dict[str, Channel] = {
            channel_id: Channel(**channel)
            for group in groups.values()
            for channel_id, channel in group.items()
        }

    def get_channel_by_id(self, channel_id: str) -> Channel | None:
        return self.channels.get(channel_id)

    def get_all_channel_ids(self) -> list:
        return list(self.channels.keys())

    def get_channel_weight(self, channel_id: str) -> float:
        channel = self.get_channel_by_id(channel_id)
        return channel.weight if channel else 1.0
