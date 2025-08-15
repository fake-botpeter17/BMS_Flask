from json import dump, load
from pymongo.asynchronous.collection import AsyncCollection
from typing import Iterable
from os import makedirs
from os.path import join
from .connection import getDB
from utils.types import Item
from utils.misc import run_periodically

inventory: AsyncCollection = getDB()["items"]

def process_items(items: Iterable[Item]) -> dict[int, dict]:
    result = {}
    for item in items:
        result[item.id] = item.model_dump()
    return result


def cache_items():
    items_res = inventory.find({}, {"_id": False})
    items = map(lambda item: Item(**item), items_res)
    items_processed = process_items(items)
    makedirs('resources', exist_ok=True)
    with open(join('resources','inventory.json'), 'w') as f:
        dump(items_processed, fp=f, indent=4)


def get_items():
    with open(join('resources','inventory.json')) as f:
        res = load(f)
    return process_items(res)

items_cacher_event, items_cacher_thread = run_periodically(cache_items)
