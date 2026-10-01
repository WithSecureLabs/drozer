import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pysolar.reflection.utils.class_builder import ClassBuilder


class ClassBuilderTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.source = Path(self.directory.name, "Example.java")
        self.source.write_text("class Example {}")
        self.builder = ClassBuilder(str(self.source), "d8", "javac", "android.jar")
        self.apk = self.source.parent / (hashlib.md5(self.source.read_bytes()).hexdigest() + ".apk")

    def test_cached_archive_uses_text_hash(self):
        self.apk.write_bytes(b"archive")
        with patch("pysolar.reflection.utils.class_builder.subprocess.call") as command:
            self.assertEqual(self.builder.build(), b"archive")
            command.assert_not_called()

    def test_build_packages_inner_classes_and_restores_directory(self):
        Path(self.directory.name, "Example$Inner.class").write_bytes(b"class")
        previous = os.getcwd()
        def command(*args, **kwargs):
            if len(calls) == 1:
                self.apk.write_bytes(b"archive")
            calls.append(args[0])
            return 0
        calls = []
        with patch("pysolar.reflection.utils.class_builder.subprocess.call", side_effect=command):
            self.assertEqual(self.builder.build(), b"archive")
        self.assertIn("Example$Inner.class", str(calls[1]))
        self.assertEqual(os.getcwd(), previous)

    def test_compile_failure_is_reported_and_restores_directory(self):
        previous = os.getcwd()
        with patch("pysolar.reflection.utils.class_builder.subprocess.call", return_value=1) as command:
            with self.assertRaisesRegex(RuntimeError, "Java sources"):
                self.builder.build()
            self.assertEqual(command.call_count, 1)
        self.assertEqual(os.getcwd(), previous)

    def test_packaging_failure_is_reported(self):
        previous = os.getcwd()
        with patch("pysolar.reflection.utils.class_builder.subprocess.call", side_effect=[0, 1]):
            with self.assertRaisesRegex(RuntimeError, "APK bundle"):
                self.builder.build()
        self.assertEqual(os.getcwd(), previous)


if __name__ == "__main__":
    unittest.main()
