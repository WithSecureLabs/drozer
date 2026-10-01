import importlib.util
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
spec = importlib.util.spec_from_file_location("file_helpers", Path(__file__).resolve().parents[1] / "src/drozer/modules/common/file_system.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FileSystem = module.FileSystem


class FileHelperTests(unittest.TestCase):
    def test_download_empty_file(self):
        helper = FileSystem()
        helper.readFile = Mock(return_value=b"")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "empty")
            self.assertEqual(helper.downloadFile("/empty", str(path)), 0)
            self.assertEqual(path.read_bytes(), b"")

    def test_directory_marker_applies_to_child(self):
        helper = FileSystem()
        parent = SimpleNamespace(list=lambda: ["file", "folder"])
        helper.new = lambda name, *args: parent if len(args) == 1 else SimpleNamespace(isDirectory=lambda: args[1] == "folder")
        self.assertEqual(helper.listFiles("/parent"), ["file", "folder/"])

    def test_read_closes_stream_on_eof(self):
        helper = FileSystem()
        stream = SimpleNamespace(close=Mock())
        file = SimpleNamespace(exists=lambda: True)
        helper.new = lambda name, *args: file if name == "java.io.File" else stream
        reader = SimpleNamespace(read=Mock(side_effect=[SimpleNamespace(base64_encode=lambda: b"YWJj"), SimpleNamespace(base64_encode=lambda: b"")]))
        helper.loadClass = Mock(return_value=reader)
        self.assertEqual(helper.readFile("/file"), b"abc")
        stream.close.assert_called_once_with()

    def test_read_closes_stream_on_error(self):
        helper = FileSystem()
        stream = SimpleNamespace(close=Mock())
        helper.new = lambda name, *args: SimpleNamespace(exists=lambda: True) if name == "java.io.File" else stream
        helper.loadClass = Mock(return_value=SimpleNamespace(read=Mock(side_effect=RuntimeError("read failed"))))
        with self.assertRaisesRegex(RuntimeError, "read failed"):
            helper.readFile("/file")
        stream.close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
