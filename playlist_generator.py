import os

from config import Config
from models import Clip


class PlaylistGenerator:
    def __init__(self, project_path: str | None = None):
        self.project_path = (
            project_path or Config.PROJECT_PATH or os.path.dirname(os.path.abspath(__file__))
        )

    def create_playlist(self, clips: list[Clip], filename: str = "clips.m3u") -> str:
        """Create an M3U playlist file with the given clips."""
        filepath = os.path.join(self.project_path, filename)

        with open(filepath, "w") as file:
            for clip in clips:
                file.write(f"https://www.youtube.com/watch?v={clip.id}\n")

        return filepath
