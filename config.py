import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY1 = os.getenv('API_KEY1')
    API_KEY2 = os.getenv('API_KEY2')
    PROJECT_PATH = os.getenv('PROJECT_PATH')