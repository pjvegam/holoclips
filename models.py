from dataclasses import dataclass
from datetime import datetime


@dataclass
class Channel:
    name: str
    weight: float

@dataclass
class Clip:
    id: str
    title: str
    available_at: datetime
    duration: int = 0
    views: int = 0
    channel_weight: float = 1.0

    @property
    def weighted_views(self) -> float:
        return self.views * self.channel_weight

    @property
    def views_per_hour(self) -> float:
        current_time = datetime.now()

        if self.views <= 0:
            return 0

        hours_available = (current_time - self.available_at).total_seconds() / 3600
        if hours_available <= 0:
            return 0

        return self.weighted_views / hours_available
