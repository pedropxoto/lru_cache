from node import Node
import time
import threading
from typing import Any


class Cache:
    _cache: dict[int, Node]
    _head: Node
    _tail: Node
    _capacity: int
    _lock: threading.RLock

    def __init__(self, capacity: int):
        self._head = Node(0, 0, 0, 0)
        self._tail = Node(0, 0, 0, 0)
        self._initial_setup()
        self._capacity = capacity
        self._lock = threading.RLock()

    def put(self, key: int, value: Any, ttl: float, priority: int) -> None:
        if value is None:
            raise ValueError("None is not allowed as a value")
        expiry_time: float = time.time()+ttl
        with self._lock:
            if key in self._cache:
                existing_node: Node = self._cache[key]
                existing_node.value = value
                existing_node.expiry_time = expiry_time
                existing_node.priority = priority
                self._move_to_head(existing_node)
            else:
                new_node: Node = Node(key, value, expiry_time, priority)
                self._cache[key] = new_node
                self._add_to_front(new_node)

            if len(self._cache) > self._capacity:
                self._evict()

    def get(self, key: int) -> Any:
        if key not in self._cache:
            return None

        with self._lock:
            node = self._cache[key]
            self._move_to_head(node)

            return node.value

    def clear(self) -> None:
        self._initial_setup()

    def _initial_setup(self) -> None:
        self._cache = {}
        self._head.next_node = self._tail
        self._tail.previous_node = self._head

    def _move_to_head(self, node: Node) -> None:
        self._remove_node(node)

        self._add_to_front(node)

        node.next_node = self._head
        self._head = node

    def _remove_from_cache(self, node: Node) -> None:
        del self._cache[node.key]
        self._remove_node(node)

    @staticmethod
    def _remove_node(node: Node) -> None:
        node.previous_node.next_node = node.next_node
        node.next_node.previous_node = node.previous_node

    def _add_to_front(self, node: Node) -> None:
        node.next_node = self._head.next_node
        node.previous_node = self._head
        self._head.next_node.previous_node = node
        self._head.next_node = node

    def _evict(self) -> None:
        self._remove_expired_items()
        if len(self._cache) > self._capacity:
            self._remove_least_priority_item()

    def _remove_expired_items(self) -> None:
        current_time: float = time.time()
        current: Node = self._tail.previous_node
        while current != self._head:
            current = current.previous_node
            if current.next_node.expiry_time <= current_time:
                self._remove_from_cache(current.next_node)

    def _remove_least_priority_item(self) -> None:
        current: Node = self._tail.previous_node
        least_priority_node: Node = current
        while current != self._head:
            if current.priority < least_priority_node.priority:
                least_priority_node = current
            current = current.previous_node
        self._remove_from_cache(least_priority_node)

    def __len__(self) -> int:
        return len(self._cache)

    def __contains__(self, key: int):
        return key in self._cache

    def __str__(self):
        current: Node = self._head.next_node
        cache_items: list[str] = []
        while current != self._tail:
            cache_items.append(f" ({current.key},{current.value})")
            current = current.next_node
        return "Cache (Key, Value): " + " <->".join(cache_items)
