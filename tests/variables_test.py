from unittest import TestCase

from unimodel import Variables


class TestVariables(TestCase):
    def test_initialization(self):
        v = Variables(a=1, b=2)
        self.assertEqual(v.a, 1)
        self.assertEqual(v.b, 2)

    def test_dict_like_behavior(self):
        v = Variables(a=1, b=2)
        self.assertEqual(v["a"], 1)
        self.assertEqual(v["b"], 2)
        v["c"] = 3
        self.assertEqual(v.c, 3)
        del v["a"]
        self.assertFalse(hasattr(v, "a"))

    def test_attribute_like_behavior(self):
        v = Variables(a=1, b=2)
        self.assertEqual(v.a, 1)
        self.assertEqual(v.b, 2)
        v.c = 3
        self.assertEqual(v["c"], 3)
        del v.c
        self.assertFalse("c" in v)

    def test_contains(self):
        v = Variables(a=1, b=2)
        self.assertTrue("a" in v)
        self.assertFalse("c" in v)

    def test_iteration(self):
        v = Variables(a=1, b=2)
        keys = set()
        for key in v:
            keys.add(key)
        self.assertEqual(keys, {"a", "b"})

    def test_items(self):
        v = Variables(a=1, b=2)
        items = set(v.items())
        self.assertEqual(items, {("a", 1), ("b", 2)})

    def test_keys(self):
        v = Variables(a=1, b=2)
        keys = set(v.keys())
        self.assertEqual(keys, {"a", "b"})

    def test_values(self):
        v = Variables(a=1, b=2)
        values = set(v.values())
        self.assertEqual(values, {1, 2})

    def test_to_dict(self):
        v = Variables(a=1, b=2)
        self.assertEqual(v.to_dict(), {"a": 1, "b": 2})
