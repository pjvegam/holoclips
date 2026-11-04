# youtube_service.py
from typing import Dict, List
import logging
import time
import requests


class YouTubeApiError(Exception):
    """The YouTube API could not return the requested view counts."""


class YouTubeService:
    BASE_URL = 'https://www.googleapis.com/youtube/v3/videos'
    BATCH_SIZE = 50  # Maximo de IDs por llamada a videos.list
    MAX_ATTEMPTS = 3

    def __init__(self, api_key: str):
        # La key va en cabecera para que no aparezca en URLs ni en los logs
        self.headers = {'X-Goog-Api-Key': api_key}

    def get_videos_views(self, video_ids: List[str]) -> Dict[str, int]:
        """Get view counts by video ID. Unavailable videos are left out of the result.

        Raises YouTubeApiError if a batch fails: a partial result would produce a wrong top.
        """
        views = {}
        for i in range(0, len(video_ids), self.BATCH_SIZE):
            views.update(self._fetch_batch(video_ids[i:i + self.BATCH_SIZE]))
        return views

    def _fetch_batch(self, video_ids: List[str]) -> Dict[str, int]:
        """Fetch view counts for up to BATCH_SIZE videos (1 quota unit), retrying transient errors."""
        params = {'part': 'statistics', 'id': ','.join(video_ids)}

        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            try:
                response = requests.get(self.BASE_URL, headers=self.headers, params=params, timeout=10)
            except requests.RequestException as e:
                error = str(e)
            else:
                if response.status_code == 200:
                    return self._parse_views(response)

                error = self._describe_error(response)
                # Key invalida, cuota agotada, etc: reintentar no lo va a arreglar
                if response.status_code != 429 and response.status_code < 500:
                    raise YouTubeApiError(error)

            if attempt < self.MAX_ATTEMPTS:
                delay = 2 ** (attempt - 1)
                logging.warning(f"YouTube API falló (intento {attempt}/{self.MAX_ATTEMPTS}), "
                                f"reintentando en {delay}s: {error}")
                time.sleep(delay)

        raise YouTubeApiError(f"sin respuesta tras {self.MAX_ATTEMPTS} intentos: {error}")

    @staticmethod
    def _parse_views(response: requests.Response) -> Dict[str, int]:
        views = {}
        for item in response.json().get('items', []):
            view_count = item['statistics'].get('viewCount')
            if view_count is not None:
                views[item['id']] = int(view_count)
        return views

    @staticmethod
    def _describe_error(response: requests.Response) -> str:
        """Build a short error message from the API's JSON error body."""
        try:
            message = response.json()['error']['message']
        except (ValueError, KeyError, TypeError):
            message = response.text[:200]
        return f"{response.status_code} - {message}"
