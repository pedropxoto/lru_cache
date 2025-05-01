import unittest
from src.node import Node


class TestNode(unittest.TestCase):
    def test_node_initialization(self):
        node: Node = Node(1, 2, 100, 0)
        self.assertEqual(node.key, 1, "The key is wrong")
        self.assertEqual(node.value, 2, "The value is wrong")
        self.assertEqual(node.expiry_time, 100, "expiry time is wrong")
        self.assertEqual(node.priority, 0, "the priority is wrong")


if __name__ == '__main__':
    unittest.main()
