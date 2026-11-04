from datetime import datetime, timedelta
from types import SimpleNamespace

import pytest
from helpers import FakeChannelRepository, make_clip, make_clip_data

from clip_service import ClipService
from youtube_service import YouTubeApiError


@pytest.fixture
def clip_service():
    repo = FakeChannelRepository({"tracked_low": 1.0, "tracked_high": 3.0})
    return ClipService(api_service=None, channel_repo=repo, youtube_service=None)


@pytest.mark.parametrize(
    ("duration", "kept"),
    [(59, False), (60, True), (600, True), (601, False)],
)
def test_process_clip_filters_by_duration(clip_service, duration, kept):
    clips = {}
    clip_service._process_clip(make_clip_data(duration=duration, sources=["tracked_low"]), clips)
    assert ("clip" in clips) is kept


def test_process_clip_ignores_untracked_channels(clip_service):
    clips = {}
    data = make_clip_data(sources=["other"], refers=["other"], mentions=["other"])
    clip_service._process_clip(data, clips)
    assert clips == {}


@pytest.mark.parametrize("field", ["sources", "refers", "mentions"])
def test_process_clip_uses_every_channel_reference(clip_service, field):
    clips = {}
    clip_service._process_clip(make_clip_data(**{field: ["tracked_high"]}), clips)
    assert clips["clip"].channel_weight == 3.0


def test_process_clip_keeps_highest_weight(clip_service):
    clips = {}
    data = make_clip_data(sources=["tracked_low"], mentions=["tracked_high"])
    clip_service._process_clip(data, clips)
    assert clips["clip"].channel_weight == 3.0


def test_process_clip_repeated_clip_keeps_highest_weight(clip_service):
    clips = {}
    clip_service._process_clip(make_clip_data(sources=["tracked_high"]), clips)
    clip_service._process_clip(make_clip_data(sources=["tracked_low"]), clips)
    assert clips["clip"].channel_weight == 3.0


def test_fetch_clips_skips_missing_and_survives_failed_pages():
    pages = {
        0: [
            make_clip_data("ok", sources=["tracked_low"]),
            make_clip_data("gone", sources=["tracked_low"], status="missing"),
        ],
        100: RuntimeError("holodex caido"),
    }

    def get_clips(from_date, to_date, limit, offset):
        page = pages.get(offset, [])
        if isinstance(page, Exception):
            raise page
        return page

    service = ClipService(
        api_service=SimpleNamespace(get_clips=get_clips),
        channel_repo=FakeChannelRepository({"tracked_low": 1.0}),
        youtube_service=None,
    )
    assert list(service.fetch_clips_for_date(datetime(2026, 1, 1))) == ["ok"]


def test_enrich_marks_clips_without_views_as_unavailable(clip_service):
    clips = {"a": make_clip("a"), "b": make_clip("b")}
    clip_service.youtube_service = SimpleNamespace(get_videos_views=lambda ids: {"a": 7})
    clip_service.enrich_clips_with_views(clips)
    assert clips["a"].views == 7
    assert clips["b"].views == -1


def test_enrich_propagates_api_errors(clip_service):
    def fail(ids):
        raise YouTubeApiError("cuota agotada")

    clip_service.youtube_service = SimpleNamespace(get_videos_views=fail)
    with pytest.raises(YouTubeApiError):
        clip_service.enrich_clips_with_views({"a": make_clip("a")})


def test_get_top_clips_returns_best_ones_in_ascending_order(clip_service):
    available_at = datetime.now() - timedelta(hours=10)
    clips = {
        name: make_clip(name, views=views, available_at=available_at)
        for name, views in [("low", 10), ("mid", 20), ("high", 30), ("unavailable", -1)]
    }
    top = clip_service.get_top_clips(clips, 2)
    assert [clip.id for clip in top] == ["mid", "high"]


def test_get_top_clips_ranks_with_channel_weight(clip_service):
    available_at = datetime.now() - timedelta(hours=10)
    clips = {
        "popular": make_clip("popular", views=100, weight=1.0, available_at=available_at),
        "weighted": make_clip("weighted", views=50, weight=3.0, available_at=available_at),
    }
    top = clip_service.get_top_clips(clips, 1)
    assert [clip.id for clip in top] == ["weighted"]
