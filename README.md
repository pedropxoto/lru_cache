# LRU Cache with TTL and Priority

This project implements a Python LRU (Least Recently Used) cache, enhanced with TTL (time to live) expiration and a priority-based eviction strategy.

## Features
- **TTL**:: old items get expired
- **Priority-based eviction**: removes low-priority items first
- **Thread-safe**: uses `Locks` to handle concurrency

---

## Available Methods

### `get(key: int) -> Any`
- Returns the value of the item with the given key, if present and  Moves the accessed item to the front.
- Returns `None` if the key is not present. 

### `put(key: int, value: Any, ttl: float, priority: int) -> None`
- Inserts a new item or updates an existing one.
- The item expires after time to live (ttl) number of seconds.
- If the cache is full:
  - Expired items are evicted first.
  - If no expired items, items with the lowest priority are removed.
  - If multiple items share the lowest priority, the least recently used one is removed.

### `clear() -> None`
- Clears all items from the cache.

### `__str__() -> str`
- Returns a string representing the cache contents.
### `__contains__() -> bool`
- Returns `True` if the key is stored in the cache.

### `__len__() -> bool`
- Returns the number of items stored in the cache.
---

## 🚀 Quick Start

```python
from src.cache import Cache

cache = Cache(capacity=3)

cache.put(1, "apple", time.time()+120, priority=2)
cache.put(2, "banana", time.time()+120, priority=3)

print(cache.get(1))
print(cache)
print(len(cache))
