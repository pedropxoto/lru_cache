import unittest
from src.cache import Cache


class TestCache(unittest.TestCase):

    def setUp(self):
        self.cache = Cache(3)
        for key in range(2):
            self.cache.put(key, key*2, 120, 2)

    def test_get_when_key_exists(self):
        self.assertEqual(self.cache.get(1), 2, "get didn't return the right value")

    def test_get_when_key_does_not_exist(self):
        self.assertIsNone(self.cache.get(2), "get didn't return the right value")

    def test_eviction_by_priority_when_capacity_exceeded(self):
        self.cache.put(2, 4, 120, 1)
        self.cache.put(3, 6, 120, 2)
        self.assertIsNone(self.cache.get(2), "eviction is not filtering by priority")

    def test_eviction_by_ttl_when_capacity_exceeded(self):
        cache = Cache(1)
        cache.put(1, 2, 0, 3)
        cache.put(2, 4, 30, 2)
        self.assertEqual(cache.get(2), 4)
        self.assertEqual(len(cache), 1)

    def test_reassign_value(self):
        self.cache.put(0, 4, 120, 2)
        self.assertEqual(self.cache.get(0), 4, "Value of the node was not reassigned")

    def test_cache_len(self):
        self.assertEqual(len(self.cache), 2)

    def test_if_cache_contain_key(self):
        self.assertFalse(2 in self.cache, "contain functionality is not working")
        self.assertTrue(1 in self.cache, "contain functionality is not working")

    def test_clear_cache(self):
        self.cache.clear()
        self.assertEqual(len(self.cache), 0, "clear function is not working")


if __name__ == "__main__":
    unittest.main()
