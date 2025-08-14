from pymongo import MongoClient
from pymongo.synchronous.database import Database
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from os import getenv

load_dotenv()

try:
    client: MongoClient = MongoClient(getenv("DB_URL"))
    print("Done!")
except ConnectionFailure:
    raise Exception()

else:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")


db_name: str = getenv("DB_NAME")

def getDB() -> Database:
    print(db_name)
    return client[db_name]