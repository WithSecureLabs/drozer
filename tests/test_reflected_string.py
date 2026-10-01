import ast
from pathlib import Path
import unittest


def load_string_type():
    path = Path(__file__).resolve().parents[1] / "src/pysolar/reflection/types/reflected_string.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    tree.body = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    namespace = {"ReflectedType": type("ReflectedType", (), {})}
    exec(compile(tree, str(path), "exec"), namespace)
    return namespace["ReflectedString"]


class ReflectedStringTests(unittest.TestCase):
    def setUp(self):
        self.string_type = load_string_type()

    def test_omitted_end_includes_last_character(self):
        value = self.string_type("abc")
        for name in ("count", "find", "index", "rfind", "rindex", "startswith", "endswith"):
            with self.subTest(method=name):
                self.assertEqual(getattr(value, name)("c", 2), getattr("abc", name)("c", 2))

    def test_explicit_end_preserves_slice_semantics(self):
        value = self.string_type("abc")
        for name in ("count", "find", "rfind", "startswith", "endswith"):
            for end in (None, -1, 0, 2, 3, 10):
                with self.subTest(method=name, end=end):
                    self.assertEqual(getattr(value, name)("c", 0, end), getattr("abc", name)("c", 0, end))
        for name in ("index", "rindex"):
            with self.assertRaises(ValueError):
                getattr(value, name)("c", 0, -1)

    def test_empty_strings_compare_and_concatenate(self):
        left, right = self.string_type(""), self.string_type("")
        self.assertTrue(left == right)
        self.assertFalse(left != right)
        self.assertEqual(left + right, "")

    def test_unequal_reflected_strings_do_not_recurse(self):
        left, right = self.string_type("abc"), self.string_type("xyz")
        self.assertFalse(left == right)
        self.assertTrue(left != right)

    def test_native_string_operations(self):
        value = self.string_type("abc")
        self.assertTrue(value == "abc")
        self.assertFalse(value != "abc")
        self.assertEqual(value + "def", "abcdef")


if __name__ == "__main__":
    unittest.main()
