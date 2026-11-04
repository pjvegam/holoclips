import json

import pytest
import requests

import youtube_service
from youtube_service import YouTubeApiError, YouTubeService


def response(status, body=None, text=""):
    result = requests.Response()
    result.status_code = status
    result._content = (json.dumps(body) if body is not None else text).encode()
    return result


def api_error(status, message):
    return response(status, {"error": {"message": message}})


OK = response(200, {"items": [{"id": "a", "statistics": {"viewCount": "7"}}]})


@pytest.fixture
def fake_api(monkeypatch):
    """Replace requests.get with a scripted sequence and record calls and sleeps."""

    def install(*script):
        steps = iter(script)
        calls = []
        sleeps = []

        def fake_get(url, headers, params, timeout):
            calls.append({"url": url, "headers": headers, "params": params})
            step = next(steps)
            if isinstance(step, Exception):
                raise step
            return step

        monkeypatch.setattr(youtube_service.requests, "get", fake_get)
        monkeypatch.setattr(youtube_service.time, "sleep", sleeps.append)
        return calls, sleeps

    return install


def test_parses_view_counts(fake_api):
    fake_api(OK)
    assert YouTubeService("key").get_videos_views(["a"]) == {"a": 7}


def test_leaves_out_videos_with_hidden_views(fake_api):
    fake_api(response(200, {"items": [{"id": "a", "statistics": {}}]}))
    assert YouTubeService("key").get_videos_views(["a"]) == {}


def test_splits_ids_in_batches_of_50(fake_api):
    calls, _ = fake_api(OK, OK, OK)
    YouTubeService("key").get_videos_views([f"id{i}" for i in range(120)])
    assert [len(call["params"]["id"].split(",")) for call in calls] == [50, 50, 20]


def test_sends_key_in_header_not_in_url_or_params(fake_api):
    calls, _ = fake_api(OK)
    YouTubeService("secret").get_videos_views(["a"])
    assert calls[0]["headers"]["X-Goog-Api-Key"] == "secret"
    assert "secret" not in calls[0]["url"]
    assert "secret" not in calls[0]["params"].values()


@pytest.mark.parametrize(
    "transient",
    [api_error(503, "caido"), api_error(429, "lento"), requests.Timeout("timeout")],
)
def test_retries_transient_errors_then_succeeds(fake_api, transient):
    calls, sleeps = fake_api(transient, OK)
    assert YouTubeService("key").get_videos_views(["a"]) == {"a": 7}
    assert len(calls) == 2
    assert sleeps == [1]


@pytest.mark.parametrize(
    "transient",
    [api_error(503, "caido"), response(500, text="<html>"), requests.ConnectionError("red")],
)
def test_gives_up_after_three_attempts(fake_api, transient):
    calls, sleeps = fake_api(transient, transient, transient)
    with pytest.raises(YouTubeApiError, match="3 intentos"):
        YouTubeService("key").get_videos_views(["a"])
    assert len(calls) == 3
    assert sleeps == [1, 2]


@pytest.mark.parametrize(
    ("status", "message"),
    [(400, "API key not valid"), (403, "exceeded your quota")],
)
def test_permanent_errors_stop_at_first_attempt_and_show_cause(fake_api, status, message):
    calls, sleeps = fake_api(api_error(status, message))
    with pytest.raises(YouTubeApiError, match=message):
        YouTubeService("key").get_videos_views(["a"])
    assert len(calls) == 1
    assert sleeps == []


def test_failed_batch_discards_partial_result(fake_api):
    calls, _ = fake_api(OK, api_error(403, "cuota"))
    with pytest.raises(YouTubeApiError):
        YouTubeService("key").get_videos_views([f"id{i}" for i in range(60)])
    assert len(calls) == 2
