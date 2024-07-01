from unittest import TestCase

from unimodel import UniversalValue


class TestUniversalValue(TestCase):
    def test_initialization(self):
        uv = UniversalValue(original="test")
        self.assertEqual(uv.original, "test")
        self.assertEqual(uv._value, "test")

    def test_lazy_evaluation(self):
        class LazyUniversalValue(UniversalValue):
            @staticmethod
            def creator(original):
                return original.upper()

        luv = LazyUniversalValue(original="lazy")
        self.assertIsNone(luv._value)
        self.assertEqual(luv.value, "LAZY")
        self.assertEqual(luv._value, "LAZY")

    def test_callable_behavior(self):
        class CallableUniversalValue(UniversalValue):
            @staticmethod
            def creator(original, suffix):
                return original + suffix

        cuv = CallableUniversalValue(original="callable")
        self.assertEqual(cuv("Suffix"), "callableSuffix")

    def test_repr_and_str(self):
        uv = UniversalValue(original="test")
        self.assertEqual(repr(uv), "UniversalValue(test)")
        self.assertEqual(str(uv), "test")

        class CallableUniversalValue(UniversalValue):
            @staticmethod
            def creator(original):
                return original.upper()

        cuv = CallableUniversalValue(original="reprstr")

        self.assertEqual(repr(cuv), "CallableUniversalValue(REPRSTR)")
        self.assertEqual(str(cuv), "REPRSTR")

    def test_getattr(self):
        uv = UniversalValue(original="test")
        self.assertEqual(uv.upper(), "TEST")
        with self.assertRaises(AttributeError):
            uv.nonexistent

    def test_getitem(self):
        uv = UniversalValue(original="test")
        self.assertEqual(uv[1], "e")

    def test_eq(self):
        uv1 = UniversalValue(original="test")
        uv2 = UniversalValue(original="test")
        uv3 = UniversalValue(original="different")

        self.assertEqual(uv1, uv2)
        self.assertNotEqual(uv1, uv3)
        self.assertEqual(uv1, "test")
        self.assertNotEqual(uv1, "different")

    def test_len(self):
        uv = UniversalValue(original="test")
        self.assertEqual(len(uv), 4)
