import json
import os

CACHE_FILE = "cache.json"


class ResponseCache:

    def __init__(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=2)