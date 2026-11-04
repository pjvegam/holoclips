from datetime import datetime, timedelta

import pytest
from helpers import make_clip


def test_views_per_hour_applies_weight_and_age():
    available_at = datetime.now() - timedelta(hours=10)
    clip = make_clip(views=100, weight=2.0, available_at=available_at)
    assert clip.views_per_hour == pytest.approx(20.0, rel=1e-3)


@pytest.mark.parametrize("views", [0, -1])
def test_views_per_hour_is_zero_without_views(views):
    clip = make_clip(views=views, available_at=datetime.now() - timedelta(hours=10))
    assert clip.views_per_hour == 0


def test_views_per_hour_is_zero_for_future_clip():
    clip = make_clip(views=100, available_at=datetime.now() + timedelta(hours=1))
    assert clip.views_per_hour == 0
