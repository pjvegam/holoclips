import logging
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest
from helpers import FakeChannelRepository, make_clip, make_clip_data

from api_service import HolodexApiError
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


def test_process_clip_keeps_holodex_time_zone(clip_service):
    clips = {}
    data = make_clip_data(sources=["tracked_low"], available_at="2026-11-04T18:00:03.000Z")
    clip_service._process_clip(data, clips)
    assert clips["clip"].available_at == datetime(2026, 11, 4, 18, 0, 3, tzinfo=UTC)


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


def service_with_pages(pages):
    """Build a ClipService over scripted Holodex pages (by offset), recording the requests."""
    requests_made = []

    def get_clips(from_date, to_date, limit, offset):
        requests_made.append({"limit": limit, "offset": offset})
        page = pages.get(offset, [])
        if isinstance(page, Exception):
            raise page
        return page

    service = ClipService(
        api_service=SimpleNamespace(get_clips=get_clips),
        channel_repo=FakeChannelRepository({"tracked_low": 1.0}),
        youtube_service=None,
    )
    return service, requests_made


def full_page(prefix):
    return [make_clip_data(f"{prefix}{i}", sources=["tracked_low"]) for i in range(50)]


def test_fetch_clips_skips_missing():
    service, _ = service_with_pages(
        {
            0: [
                make_clip_data("ok", sources=["tracked_low"]),
                make_clip_data("gone", sources=["tracked_low"], status="missing"),
            ]
        }
    )
    assert list(service.fetch_clips_for_date(datetime(2026, 1, 1))) == ["ok"]


def test_fetch_clips_stops_at_first_incomplete_page():
    short_page = [make_clip_data("last", sources=["tracked_low"])]
    service, requests_made = service_with_pages({0: full_page("a"), 50: short_page})
    clips = service.fetch_clips_for_date(datetime(2026, 1, 1))
    assert len(clips) == 51
    assert requests_made == [{"limit": 50, "offset": 0}, {"limit": 50, "offset": 50}]


def test_fetch_clips_stops_at_empty_page_after_exact_multiple():
    service, requests_made = service_with_pages({0: full_page("a"), 50: []})
    assert len(service.fetch_clips_for_date(datetime(2026, 1, 1))) == 50
    assert [request["offset"] for request in requests_made] == [0, 50]


def test_fetch_clips_warns_when_reaching_the_maximum(caplog):
    pages = {offset: full_page(f"p{offset}-") for offset in range(0, 500, 50)}
    service, requests_made = service_with_pages(pages)
    with caplog.at_level(logging.WARNING):
        assert len(service.fetch_clips_for_date(datetime(2026, 1, 1))) == 500
    assert len(requests_made) == 10
    assert "tope" in caplog.text


def test_fetch_clips_stops_when_a_page_fails():
    service, requests_made = service_with_pages(
        {0: full_page("a"), 50: HolodexApiError("holodex caido"), 100: []}
    )
    with pytest.raises(HolodexApiError):
        service.fetch_clips_for_date(datetime(2026, 1, 1))
    assert [request["offset"] for request in requests_made] == [0, 50]


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
    available_at = datetime.now(UTC) - timedelta(hours=10)
    clips = {
        name: make_clip(name, views=views, available_at=available_at)
        for name, views in [("low", 10), ("mid", 20), ("high", 30), ("unavailable", -1)]
    }
    top = clip_service.get_top_clips(clips, 2)
    assert [clip.id for clip in top] == ["mid", "high"]


def test_get_top_clips_ranks_with_channel_weight(clip_service):
    available_at = datetime.now(UTC) - timedelta(hours=10)
    clips = {
        "popular": make_clip("popular", views=100, weight=1.0, available_at=available_at),
        "weighted": make_clip("weighted", views=50, weight=3.0, available_at=available_at),
    }
    top = clip_service.get_top_clips(clips, 1)
    assert [clip.id for clip in top] == ["weighted"]
