from django.core.cache import cache


class Cache:
    def set(self, key: str, value):
        cache.set(key, value)

    def get(self, key: str):
        return cache.get(key)

    def delete(self, key: str):
        cache.delete(key)

    def incr(self, key: str, delta=1):
        cache.incr(key, delta)

    def decr(self, key: str, delta=1):
        cache.decr(key, delta)
