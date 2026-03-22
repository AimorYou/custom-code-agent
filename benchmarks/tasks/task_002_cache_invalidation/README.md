# cachebox

A lightweight LRU cache with a pluggable storage backend and a service layer that ties them together. Designed for applications that need a simple caching strategy in front of a key-value store.

## Installation

No external dependencies. Just copy the `src/` directory into your project.

## Quick start

```python
from src.service import DataService

svc = DataService()

svc.set("user:1", {"name": "Alice", "role": "admin"})
print(svc.get("user:1"))  # {'name': 'Alice', 'role': 'admin'}

svc.set("user:1", {"name": "Alice", "role": "editor"})
print(svc.get("user:1"))  # updated value
```

## Module overview

### `cache.py` -- LRU cache

`LRUCache` is an in-memory least-recently-used cache built on top of `OrderedDict`.

```python
from src.cache import LRUCache

cache = LRUCache(capacity=256)
cache.put("key", "value")
cache.get("key")        # "value"
cache.invalidate("key") # remove from cache
cache.clear()           # drop everything
```

### `storage.py` -- Storage backend

`Storage` is a simple key-value store that acts as the persistent layer.

```python
from src.storage import Storage

store = Storage()
store.set("key", "value")
store.get("key")  # "value"
```

### `service.py` -- Service layer

`DataService` combines the cache and storage into a single interface. Reads go through the cache first; writes update storage and invalidate the cache.

## Running tests

```bash
python -m pytest tests/ -v
```

## License

MIT
