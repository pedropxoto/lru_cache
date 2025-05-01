from typing import Optional, Any


class Node:
    key: int
    value: Any
    expiry_time: float
    priority: int
    next_node: Optional['Node']
    previous_node: Optional['Node']

    def __init__(self, key: int, value: Any, expiry_time: float, priority: int):
        self.key = key
        self.value = value
        self.expiry_time = expiry_time
        self.priority = priority
        self.next_node = None
        self.previous_node = None
