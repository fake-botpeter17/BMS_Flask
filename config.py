from os import getenv
from dotenv import load_dotenv
from json import loads
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

load_dotenv()

class Config:
    DEBUG = False
    TESTING = False
    DB_URL = getenv("DB_URL")
    DB_NAME = getenv("DB_NAME")
    REDIS_PARAMS = loads(getenv("REDIS_PARAMS"))


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass
