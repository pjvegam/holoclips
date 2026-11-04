import tomllib

import pytest

from channel_repository import CHANNELS_FILE, ChannelRepository
from models import Channel


@pytest.fixture
def groups():
    with open(CHANNELS_FILE, "rb") as file:
        return tomllib.load(file)


def test_loads_channels_from_every_group(tmp_path):
    channels_file = tmp_path / "channels.toml"
    channels_file.write_text(
        '[a]\nUC1 = { name = "uno", weight = 2.0 }\n[b]\nUC2 = { name = "dos", weight = 3.0 }\n',
        encoding="utf-8",
    )
    repo = ChannelRepository(channels_file)
    assert repo.get_all_channel_ids() == ["UC1", "UC2"]
    assert repo.get_channel_by_id("UC2") == Channel(name="dos", weight=3.0)
    assert repo.get_channel_weight("UC2") == 3.0


def test_unknown_channel_has_default_weight():
    repo = ChannelRepository()
    assert repo.get_channel_by_id("desconocido") is None
    assert repo.get_channel_weight("desconocido") == 1.0


def test_channels_file_has_no_repeated_ids(groups):
    ids = [channel_id for group in groups.values() for channel_id in group]
    assert len(ids) == len(set(ids))


def test_channels_file_has_valid_entries(groups):
    for group in groups.values():
        for channel_id, channel in group.items():
            assert channel_id.startswith("UC"), channel_id
            assert len(channel_id) == 24, channel_id
            assert channel["name"], channel_id
            assert channel["weight"] > 0, channel_id
