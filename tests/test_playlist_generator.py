from helpers import make_clip

from playlist_generator import PlaylistGenerator


def test_writes_clips_in_order(tmp_path):
    clips = [make_clip("first"), make_clip("second")]
    path = PlaylistGenerator(str(tmp_path)).create_playlist(clips)
    assert (tmp_path / "clips.m3u").read_text().splitlines() == [
        "https://www.youtube.com/watch?v=first",
        "https://www.youtube.com/watch?v=second",
    ]
    assert path == str(tmp_path / "clips.m3u")
