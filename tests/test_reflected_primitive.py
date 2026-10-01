import operator
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pysolar.reflection.types.reflected_primitive import ReflectedPrimitive


class PrimitiveTests(unittest.TestCase):
    def value(self, number):
        return ReflectedPrimitive("int", number)

    def test_truth_values(self):
        for value in (False, 0, 0.0, True, 1, -1):
            self.assertEqual(bool(self.value(value)), bool(value))

    def test_comparisons_match_native_values(self):
        for operation in (operator.eq, operator.ne, operator.ge, operator.gt, operator.le, operator.lt):
            for left, right in ((0, 0), (0, 1), (1, 0), (2, 2)):
                with self.subTest(operation=operation.__name__, left=left, right=right):
                    self.assertEqual(operation(self.value(left), self.value(right)), operation(left, right))

    def test_division_in_both_directions(self):
        self.assertEqual(self.value(6) / 4, 1.5)
        self.assertEqual(6 / self.value(4), 1.5)
        self.assertEqual(self.value(6) / self.value(4), 1.5)

    def test_native_and_reflected_bitwise_or(self):
        self.assertEqual((self.value(1) | 2).native(), 3)
        self.assertEqual((self.value(1) | self.value(2)).native(), 3)

    def test_zero_power_operand_is_unwrapped(self):
        self.assertEqual(self.value(2) ** self.value(0), 1)
        self.assertEqual(self.value(0) ** self.value(2), 0)
        self.assertEqual(pow(self.value(2), self.value(3), self.value(5)), 3)


if __name__ == "__main__":
    unittest.main()
