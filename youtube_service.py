# youtube_service.py
import re
import os
import time
import hashlib
import sqlite3
import shutil
import tempfile
import threading
import requests
import logging

_ORIGIN = 'https://www.youtube.com'

_AUTH_COOKIE_NAMES = {
    'SID', 'HSID', 'SSID', 'APISID', 'SAPISID',
    '__Secure-1PSID', '__Secure-3PSID',
    '__Secure-1PAPISID', '__Secure-3PAPISID',
    '__Secure-1PSIDTS', '__Secure-3PSIDTS',
}


def _generate_sapisidhash(sapisid: str) -> str:
    """Generate SAPISIDHASH auth header like yt-dlp does."""
    timestamp = int(time.time())
    hash_input = f"{timestamp} {sapisid} {_ORIGIN}"
    hash_value = hashlib.sha1(hash_input.encode()).hexdigest()
    return f"SAPISIDHASH {timestamp}_{hash_value}"


class YouTubeService:
    _HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Origin': _ORIGIN,
    }
    _cookies = None
    _sapisid = None
    _lock = threading.Lock()

    @classmethod
    def _load_firefox_cookies(cls):
        """Load YouTube auth cookies from Firefox's cookies.sqlite (one-time, thread-safe)."""
        if cls._cookies is not None:
            return cls._cookies

        with cls._lock:
            if cls._cookies is not None:
                return cls._cookies

            appdata = os.environ.get('APPDATA', '')
            profiles_dir = os.path.join(appdata, 'Mozilla', 'Firefox', 'Profiles')

            if not os.path.exists(profiles_dir):
                logging.warning("Firefox profiles directory not found")
                cls._cookies = {}
                return cls._cookies

            cookies_db = None
            for profile in os.listdir(profiles_dir):
                candidate = os.path.join(profiles_dir, profile, 'cookies.sqlite')
                if os.path.exists(candidate):
                    cookies_db = candidate
                    break

            if not cookies_db:
                logging.warning("Firefox cookies.sqlite not found")
                cls._cookies = {}
                return cls._cookies

            tmp = tempfile.mktemp(suffix='.sqlite')
            shutil.copy2(cookies_db, tmp)

            cookies = {}
            try:
                conn = sqlite3.connect(tmp)
                cursor = conn.execute(
                    "SELECT name, value FROM moz_cookies WHERE host LIKE '%.youtube.com%'"
                )
                for name, value in cursor.fetchall():
                    if name in _AUTH_COOKIE_NAMES:
                        cookies[name] = value
                    if name == 'SAPISID':
                        cls._sapisid = value
                conn.close()
            finally:
                os.unlink(tmp)

            cls._cookies = cookies
            logging.info(f"Loaded {len(cookies)} YouTube auth cookies from Firefox")
            return cls._cookies

    @classmethod
    def get_video_views(cls, video_id: str) -> int:
        """Get view count for a YouTube video."""
        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            cookies = cls._load_firefox_cookies()
            headers = dict(cls._HEADERS)
            if cls._sapisid:
                headers['Authorization'] = _generate_sapisidhash(cls._sapisid)

            response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            response.raise_for_status()
            match = re.search(r'"viewCount":"(\d+)"', response.text)
            if match:
                return int(match.group(1))
            logging.warning(f"No view count found for {video_id}")
            return -1
        except Exception as e:
            logging.error(f"Error getting views for {video_id}: {str(e)}")
            return -1
