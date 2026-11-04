import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    HOLODEX_API_KEY = os.getenv("HOLODEX_API_KEY")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    PROJECT_PATH = os.getenv("PROJECT_PATH")
