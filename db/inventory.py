from pymongo.cursor import Cursor
from pymongo.synchronous.collection import Collection
from typing import Iterable, Generator
from pathlib import Path
from copy import deepcopy
from .connection import getDB
from utils.types import Item
from utils.misc import run_periodically, read_json_file, write_json_file

inventory: Collection = getDB()["items"]
cache_file: Path = Path("resources", "inventory.json")
cached_items: None | dict[int, Item] = None


def process_items(items: Iterable[Item]) -> dict[int, dict]:
    """
    Processes a sequence of Item objects and returns a dictionary with their ids as keys
    and their model_dump() output as values.

    Args:
        items (Iterable[Item]): A sequence of Item objects to be processed.

    Returns:
        dict[int, dict]: A dictionary with item ids as keys and their model_dump() output as values.
    """
    result: dict[int, dict] = {}
    for item in items:
        result[item.id] = item.model_dump()
    return result


def load_processed_items(isAdmin: bool) -> dict[int, dict]:
    """
    Load and process items from the cache file. If the items are already loaded,
    process them according to the isAdmin flag.

    Args:
        isAdmin (bool): A flag indicating whether the user is an admin.

    Returns:
        dict[int, dict]: A dictionary with item ids as keys and their processed model_dump() output as values.
    """
    global cached_items
    if cached_items:
        exclude: list[str] = [] if isAdmin else ["cp"]
        items: dict[int, Item] = deepcopy(cached_items)
        for key in items:
            item: Item = items[key]
            items[key]: dict = item.model_dump(exclude=exclude)
        return items
    data: dict[int, dict] = read_json_file(cache_file)
    for key in data:
        raw_item: dict = data[key]
        data[key]: Item = Item(**raw_item)
    cached_items: dict[int, dict] = data
    return load_processed_items(isAdmin)


def cache_items() -> None:
    """
    Cache items from the database in a JSON file.

    This function retrieves all items from the database, processes them using the process_items function,
    and writes the processed items to a JSON file. If the file does not exist, it creates the parent directory.

    Returns:
        None
    """
    items_res: Cursor = inventory.find({}, {"_id": False})
    items: Generator = map(lambda item: Item(**item), items_res)
    items_processed: dict[int, dict] = process_items(items)
    if not cache_file.exists():
        cache_file.parent.mkdir(parents=True, exist_ok=True)
    write_json_file(cache_file, items_processed, indent=4)


def get_items(isAdmin: bool) -> dict[int, dict]:
    """
    Get items from the cache.

    This function checks if the cache file exists. If it does not exist, it caches the items from the database.
    It then loads the processed items from the cache using the load_processed_items function.

    Args:
        isAdmin (bool): A flag indicating whether the user is an admin.

    Returns:
        dict[int, dict]: A dictionary with item ids as keys and their processed model_dump() output as values.
    """
    if not cache_file.exists():
        cache_items()
    res: dict[int, dict] = load_processed_items(isAdmin)
    return res


items_cacher_event, items_cacher_thread = run_periodically(cache_items)
