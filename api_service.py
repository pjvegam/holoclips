from datetime import datetime

import requests


class HolodexApiService:
    BASE_URL = 'https://holodex.net/api/v2/videos'

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {'X-APIKEY': api_key}

    def get_clips(self, from_date: datetime, to_date: datetime,
                  langs: list[str] = None, limit: int = 100, offset: int = 0) -> list[dict]:
        """Fetch clips from the Holodex API."""
        if langs is None:
            langs = ['en', 'es']

        params = {
            'lang': ','.join(langs),
            'type': 'clip',
            'from': from_date.isoformat(),
            'to': to_date.isoformat(),
            'include': 'sources,mentions,refers',
            'offset': offset,
            'limit': limit,
        }

        response = requests.get(self.BASE_URL, headers=self.headers, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

        return response.json()
