from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class Channel:
    name: str
    weight: float


@dataclass
class VideoInfo:
    views: int
    is_vertical: bool


@dataclass
class Clip:
    id: str
    title: str
    available_at: datetime
    duration: int = 0
    views: int = 0
    channel_weight: float = 1.0
    is_vertical: bool = False

    @property
    def views_per_hour(self) -> float:
        current_time = datetime.now(UTC)

        if self.views <= 0:
            return 0

        hours_available = (current_time - self.available_at).total_seconds() / 3600
        if hours_available <= 0:
            return 0

        return self.views / hours_available

    @property
    def score(self) -> float:
        """Ranking value: views per hour boosted by the channel weight."""
        return self.views_per_hour * self.channel_weight
