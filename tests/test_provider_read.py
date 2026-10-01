import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class ProviderReadTests(unittest.TestCase):
    def setUp(self):
        path = Path(__file__).resolve().parents[1] / "src/drozer/modules/common/provider.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        provider = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Provider")
        proxy = next(n for n in provider.body if isinstance(n, ast.ClassDef) and n.name == "ContentResolverProxy")
        proxy.body = [n for n in proxy.body if isinstance(n, ast.FunctionDef) and n.name == "read"]
        namespace = {"Provider": SimpleNamespace(UnableToOpenFileException=IOError)}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[proxy], type_ignores=[])), str(path), "exec"), namespace)
        self.proxy = namespace["ContentResolverProxy"]()
        self.stream = SimpleNamespace(close=Mock())
        self.reader = SimpleNamespace(read=Mock(return_value=SimpleNamespace(base64_encode=lambda: b"YWJj")))
        self.proxy._ContentResolverProxy__module = SimpleNamespace(loadClass=Mock(return_value=self.reader))
        self.resolver = SimpleNamespace(openInputStream=Mock(return_value=self.stream))
        self.proxy._ContentResolverProxy__content_resolver = self.resolver
        self.proxy._ContentResolverProxy__get_client = lambda uri: self.resolver
        self.proxy._ContentResolverProxy__must_release_client = False
        self.proxy.parseUri = lambda uri: uri

    def test_fallback_reads_existing_stream_as_base64(self):
        self.assertEqual(self.proxy.read("content://example"), "YWJj")
        self.reader.read.assert_called_once_with(self.stream)
        self.stream.close.assert_called_once_with()

    def test_fallback_closes_stream_after_read_failure(self):
        self.reader.read.side_effect = RuntimeError("read failed")
        with self.assertRaisesRegex(RuntimeError, "read failed"):
            self.proxy.read("content://example")
        self.stream.close.assert_called_once_with()

    def test_missing_stream_keeps_existing_error(self):
        self.resolver.openInputStream.return_value = None
        with self.assertRaises(IOError):
            self.proxy.read("content://example")


if __name__ == "__main__":
    unittest.main()
