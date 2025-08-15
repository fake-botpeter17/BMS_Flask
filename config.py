from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    DEBUG = False
    TESTING = False
    DB_URL = getenv("DB_URL")
    DB_NAME = getenv("DB_NAME")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass
