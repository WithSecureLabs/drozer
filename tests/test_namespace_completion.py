import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class NamespaceCompletionTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / "src/drozer/console/session.py"
        tree = ast.parse(source.read_text(encoding="utf-8"))
        session = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "Session")
        method = next(node for node in session.body if isinstance(node, ast.FunctionDef) and node.name == "__namespaces")
        isolated = ast.ClassDef(name="Session", bases=[], keywords=[], body=[method], decorator_list=[])
        namespace = {}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[isolated], type_ignores=[])), str(source), "exec"), namespace)
        self.session = namespace["Session"]()
        self.session.modules = SimpleNamespace(all=Mock(return_value=["app.package.info", "app.provider.info"]))
        self.session.permissions = Mock(return_value=["permission"])
        self.session._Session__base = "app."
        self.session._Session__module = lambda key: SimpleNamespace(namespace=lambda: key[1:].rsplit(".", 1)[0])

    def test_current_scope_uses_selected_modules(self):
        self.assertEqual(self.session._Session__namespaces(), {"app.package", "app.provider"})
        self.session.modules.all.assert_called_once_with(permissions=["permission"], prefix="app.")

    def test_global_scope_ignores_current_prefix(self):
        self.assertEqual(self.session._Session__namespaces(global_scope=True), {"app.package", "app.provider"})
        self.session.modules.all.assert_called_once_with(permissions=["permission"], prefix=None)

    def test_empty_scope_has_no_namespaces(self):
        self.session.modules.all.return_value = []
        self.assertEqual(self.session._Session__namespaces(), set())


if __name__ == "__main__":
    unittest.main()
