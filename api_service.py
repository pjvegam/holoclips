from datetime import datetime

import requests


class HolodexApiError(Exception):
    """The Holodex API could not return the requested clips."""


class HolodexApiService:
    BASE_URL = "https://holodex.net/api/v2/videos"
    MAX_LIMIT = 50  # Maximo documentado para limit

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"X-APIKEY": api_key}

    def get_clips(
        self,
        from_date: datetime,
        to_date: datetime,
        langs: list[str] | None = None,
        limit: int = MAX_LIMIT,
        offset: int = 0,
    ) -> list[dict]:
        """Fetch clips from the Holodex API. Raises HolodexApiError if the request fails."""
        if langs is None:
            langs = ["en", "es"]

        params = {
            "lang": ",".join(langs),
            "type": "clip",
            "from": from_date.isoformat(),
            "to": to_date.isoformat(),
            "include": "sources,mentions,refers",
            "offset": offset,
            "limit": limit,
        }

        try:
            response = requests.get(self.BASE_URL, headers=self.headers, params=params, timeout=20)
        except requests.RequestException as e:
            raise HolodexApiError(str(e)) from e

        if response.status_code != 200:
            raise HolodexApiError(f"{response.status_code} - {response.text[:200]}")

        return response.json()
