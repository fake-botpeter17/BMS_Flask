from redis import Redis
from config import Config

r = Redis(**Config.REDIS_PARAMS)

def set_key(key: str, value: str, expire: int = 3600):
    """Set a key in Redis with optional expiration in seconds"""
    r.set(key, value, ex=expire)

def get_key(key: str):
    """Get a key from Redis"""
    return r.get(key)

def delete_key(key: str):
    """Delete a key from Redis"""
    r.delete(key)