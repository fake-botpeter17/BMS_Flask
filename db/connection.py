from pymongo import MongoClient
from pymongo.synchronous.database import Database
from utils.exceptions import DatabaseInitializationError
from dotenv import load_dotenv
from os import getenv

load_dotenv()

try:
    client: MongoClient = MongoClient(getenv("DB_URL"))
except Exception as e:
    raise DatabaseInitializationError(f"Database Connection Failed: {e}")

else:
    client.admin.command('ping')


db_name: str = getenv("DB_NAME")

def getDB() -> Database:
    return client[db_name]