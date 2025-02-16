class Cache:
    def __init__(self):
        self.cache = {}

    def get(self, key: str):
        return self.cache.get(key)

    def set(self, key: str, value: str):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()
