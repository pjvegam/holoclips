# youtube_service.py
from typing import Dict, List
import requests
import logging


class YouTubeService:
    BASE_URL = 'https://www.googleapis.com/youtube/v3/videos'
    BATCH_SIZE = 50  # Maximo de IDs por llamada a videos.list

    def __init__(self, api_key: str):
        # La key va en cabecera para que no aparezca en URLs ni en los logs
        self.headers = {'X-Goog-Api-Key': api_key}

    def get_videos_views(self, video_ids: List[str]) -> Dict[str, int]:
        """Get view counts by video ID. Unavailable videos are left out of the result."""
        views = {}
        for i in range(0, len(video_ids), self.BATCH_SIZE):
            batch = video_ids[i:i + self.BATCH_SIZE]
            try:
                views.update(self._fetch_batch(batch))
            except Exception as e:
                logging.error(f"Error getting views for {len(batch)} videos: {str(e)}")
        return views

    def _fetch_batch(self, video_ids: List[str]) -> Dict[str, int]:
        """Fetch view counts for up to BATCH_SIZE videos (1 quota unit)."""
        params = {'part': 'statistics', 'id': ','.join(video_ids)}
        response = requests.get(self.BASE_URL, headers=self.headers, params=params, timeout=10)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        views = {}
        for item in response.json().get('items', []):
            view_count = item['statistics'].get('viewCount')
            if view_count is not None:
                views[item['id']] = int(view_count)
        return views
