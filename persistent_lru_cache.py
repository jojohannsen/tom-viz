import functools
import os
import pickle
import atexit
from functools import wraps

CACHE_FILE = 'data/haiku_cache.pkl'  # You can set this to any file path you prefer

# Global variable to track if the last call was a cache hit
last_call_was_cache_hit = False

def persistent_lru_cache_with_key(maxsize=128, key_func=None, cache_file=CACHE_FILE):
    def decorator(func):
        # Load the cache from the file if it exists
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                cache = pickle.load(f)
        else:
            cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if len(cache) >= maxsize:
                cache.pop(next(iter(cache)))  # Simple LRU policy
            cache[key] = result
            return result

        # Save cache to disk at exit
        @atexit.register
        def save_cache():
            with open(cache_file, 'wb') as f:
                pickle.dump(cache, f)

        return wrapper
    return decorator

def last_call_was_cache_hit():
    global last_call_was_cache_hit
    return last_call_was_cache_hit
