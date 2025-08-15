from json import dump, load
from pymongo.asynchronous.collection import AsyncCollection
from typing import Iterable
from pathlib import Path
from .connection import getDB
from utils.types import Item
from utils.misc import run_periodically

inventory: AsyncCollection = getDB()["items"]
cache_file = Path("resources", "inventory.json")


def process_items(items: Iterable[Item], admin: bool) -> dict[int, dict]:
    exclude = [] if admin else ["cp"]
    result = {}
    for item in items:
        result[item.id] = item.model_dump(exclude=exclude)
    return result


def cache_items():
    items_res = inventory.find({}, {"_id": False})
    items = map(lambda item: Item(**item), items_res)
    items_processed = process_items(items)
    if not cache_file.exists():
        cache_file.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as f:
        dump(items_processed, fp=f, indent=4)


def get_items(admin: bool):
    if not cache_file.exists():
        cache_items()
    with open(cache_file) as f:
        res = load(f)
    return process_items(res, admin)


items_cacher_event, items_cacher_thread = run_periodically(cache_items)
