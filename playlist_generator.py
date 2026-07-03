import os
from typing import List
from models import Clip
from config import Config

class PlaylistGenerator:
    def __init__(self, project_path: str = None):
        self.project_path = project_path or Config.PROJECT_PATH

    def create_playlist(self, clips: List[Clip], filename: str = "clips.m3u") -> str:
        """Create an M3U playlist file with the given clips."""
        filepath = os.path.join(self.project_path, filename)

        with open(filepath, "w") as file:
            for clip in clips:
                file.write(f"https://www.youtube.com/watch?v={clip.id}\n")

        return filepath