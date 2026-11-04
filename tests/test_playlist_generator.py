import os

from helpers import make_clip

import playlist_generator
from playlist_generator import PlaylistGenerator


def test_writes_clips_in_order(tmp_path):
    clips = [make_clip("first"), make_clip("second")]
    path = PlaylistGenerator(str(tmp_path)).create_playlist(clips)
    assert (tmp_path / "clips.m3u").read_text().splitlines() == [
        "https://www.youtube.com/watch?v=first",
        "https://www.youtube.com/watch?v=second",
    ]
    assert path == str(tmp_path / "clips.m3u")


def test_defaults_to_project_folder_without_project_path(monkeypatch):
    monkeypatch.setattr(playlist_generator.Config, "PROJECT_PATH", None)
    expected = os.path.dirname(os.path.abspath(playlist_generator.__file__))
    assert PlaylistGenerator().project_path == expected


def test_uses_configured_project_path(monkeypatch, tmp_path):
    monkeypatch.setattr(playlist_generator.Config, "PROJECT_PATH", str(tmp_path))
    assert PlaylistGenerator().project_path == str(tmp_path)
