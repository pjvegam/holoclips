from datetime import UTC, datetime, timedelta, timezone

import pytest
from helpers import make_clip


def test_views_per_hour_ignores_channel_weight():
    available_at = datetime.now(UTC) - timedelta(hours=10)
    clip = make_clip(views=100, weight=2.0, available_at=available_at)
    assert clip.views_per_hour == pytest.approx(10.0, rel=1e-3)


def test_score_applies_channel_weight():
    available_at = datetime.now(UTC) - timedelta(hours=10)
    clip = make_clip(views=100, weight=2.0, available_at=available_at)
    assert clip.score == pytest.approx(20.0, rel=1e-3)


@pytest.mark.parametrize("views", [0, -1])
def test_views_per_hour_is_zero_without_views(views):
    clip = make_clip(views=views, available_at=datetime.now(UTC) - timedelta(hours=10))
    assert clip.views_per_hour == 0


def test_views_per_hour_is_zero_for_future_clip():
    clip = make_clip(views=100, available_at=datetime.now(UTC) + timedelta(hours=1))
    assert clip.views_per_hour == 0


@pytest.mark.parametrize("utc_offset", [-3, 0, 9])
def test_age_does_not_depend_on_time_zone(utc_offset):
    zone = timezone(timedelta(hours=utc_offset))
    available_at = datetime.now(zone) - timedelta(hours=10)
    clip = make_clip(views=100, available_at=available_at)
    assert clip.views_per_hour == pytest.approx(10.0, rel=1e-3)
