from pymongo import MongoClient
from pymongo.synchronous.database import Database
from utils.exceptions import DatabaseInitializationError
from pymongo.synchronous.collection import Collection
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

inventory: Collection = getDB()["items"]
users: Collection = getDB()["users"]
bills: Collection = getDB()["bills"]