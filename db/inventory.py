from json import dumps
from connection import getDB
from pymongo.asynchronous.collection import AsyncCollection
from utils.types import Item
# from utils.misc import run_periodically


inventory: AsyncCollection = getDB()["items"]


def process_items(items: map[Item]) -> dict[int, dict]:
    result = {}
    for item in items:
        result[item.id] = item.model_dump()
    return result


def cache_items():
    items_res = inventory.find({}, {"_id": False})
    items = map(Item, items_res)
    items_processed = process_items(items)
    
    print(dumps(items_processed, indent=4))


cache_items()
