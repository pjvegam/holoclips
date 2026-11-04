from datetime import UTC, datetime

from models import Clip


class FakeChannelRepository:
    def __init__(self, weights):
        self.weights = weights

    def get_all_channel_ids(self):
        return list(self.weights)

    def get_channel_weight(self, channel_id):
        return self.weights.get(channel_id, 1.0)


def make_clip(clip_id="clip", views=0, weight=1.0, available_at=None):
    return Clip(
        id=clip_id,
        title=clip_id,
        available_at=available_at or datetime(2026, 1, 1),
        views=views,
        channel_weight=weight,
    )


def make_clip_data(clip_id="clip", duration=120, sources=(), refers=(), mentions=(), status="past"):
    return {
        "id": clip_id,
        "title": clip_id,
        "status": status,
        "available_at": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "duration": duration,
        "sources": [{"channel": {"id": channel_id}} for channel_id in sources],
        "refers": [{"channel": {"id": channel_id}} for channel_id in refers],
        "mentions": [{"id": channel_id} for channel_id in mentions],
    }
