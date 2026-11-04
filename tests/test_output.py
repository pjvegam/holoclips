from datetime import UTC, datetime, timedelta

from helpers import make_clip

import output


def test_table_lists_best_clip_first_and_shows_real_views_per_hour(capsys):
    available_at = datetime.now(UTC) - timedelta(hours=10)
    clips = [
        make_clip("worse", views=100, weight=1.0, available_at=available_at),
        make_clip("better", views=100, weight=3.0, available_at=available_at),
    ]
    output.print_top_clips_table(clips)

    rows = [line for line in capsys.readouterr().out.splitlines() if line[:1] in ("1", "2")]
    assert rows[0].startswith("1") and rows[0].endswith("better")
    assert rows[1].startswith("2") and rows[1].endswith("worse")
    # Ambos tienen las mismas vistas por hora; solo cambia el score
    assert "10.0" in rows[0]
    assert "30.0" in rows[0]


def test_table_truncates_long_titles(capsys):
    clip = make_clip(available_at=datetime.now(UTC) - timedelta(hours=1))
    clip.title = "x" * 80
    output.print_top_clips_table([clip])
    assert "x" * 54 + "…" in capsys.readouterr().out


def test_play_with_mpv_runs_resolved_executable(monkeypatch):
    calls = []
    monkeypatch.setattr(output.shutil, "which", lambda name: f"/bin/{name}")
    monkeypatch.setattr(output.subprocess, "run", lambda cmd, check: calls.append(cmd))
    assert output.play_with_mpv("lista.m3u") is True
    assert calls == [["/bin/mpv", output.MPV_PLAYER_CLIENT_OPTION, "lista.m3u"]]


def test_mpv_avoids_player_client_that_gets_http_403():
    assert "player_client=web_safari" in output.MPV_PLAYER_CLIENT_OPTION


def test_play_with_mpv_reports_missing_executable(monkeypatch):
    monkeypatch.setattr(output.shutil, "which", lambda name: None)
    assert output.play_with_mpv("lista.m3u") is False


def test_open_in_browser_keeps_order_and_waits_between_tabs(monkeypatch):
    opened = []
    sleeps = []
    monkeypatch.setattr(output.webbrowser, "open_new_tab", opened.append)
    monkeypatch.setattr(output.time, "sleep", sleeps.append)
    output.open_in_browser([make_clip("a"), make_clip("b"), make_clip("c")])
    assert opened == [f"https://www.youtube.com/watch?v={clip_id}" for clip_id in "abc"]
    assert sleeps == [0.8, 0.8]
