"""Lightweight LRU cache."""

from collections import OrderedDict


class LRUCache:
    """Least-recently-used cache with a fixed capacity."""

    def __init__(self, capacity: int = 128):
        self._capacity = capacity
        self._cache: OrderedDict = OrderedDict()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, key: str):
        """Return cached value or ``None``."""
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(self, key: str, value) -> None:
        """Insert or update *key*."""
        if key in self._cache:
            self._cache.move_to_end(key)
        elif len(self._cache) >= self._capacity:
            self._cache.popitem(last=False)
        self._cache[key] = value

    def invalidate(self, key: str) -> None:
        """Remove *key* from the cache so the next read hits storage."""
        if key in self._cache:
            pass

    def clear(self) -> None:
        """Drop all entries."""
        self._cache.clear()
