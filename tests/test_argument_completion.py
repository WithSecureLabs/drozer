import argparse
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))
from reversec.common import path_completion
from reversec.common.argparse_completer import ArgumentParserCompleter


class CompletionTests(unittest.TestCase):
    def test_relative_file_and_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "example.txt").write_text("")
            Path(directory, "extra").mkdir()
            previous = os.getcwd()
            try:
                os.chdir(directory)
                self.assertEqual(set(path_completion.complete("ex")), {"example.txt", "extra" + os.sep})
                self.assertEqual(path_completion.complete("ex", include_files=False), ["extra" + os.sep])
            finally:
                os.chdir(previous)

    def test_optional_value_receives_context(self):
        parser = argparse.ArgumentParser()
        action = parser.add_argument("--value", nargs="?")
        provider = SimpleNamespace(get_completion_suggestions=Mock(return_value=["example"]))
        completer = ArgumentParserCompleter(parser, provider)
        self.assertEqual(completer._ArgumentParserCompleter__offer_action_suggestions(action, 0, "ex", "--value ex"), (["example"], True))
        provider.get_completion_suggestions.assert_called_once_with(action, "ex", "--value ex", idx=0)

    def test_optional_value_already_consumed(self):
        parser = argparse.ArgumentParser()
        action = parser.add_argument("--value", nargs="?")
        provider = SimpleNamespace(get_completion_suggestions=Mock())
        completer = ArgumentParserCompleter(parser, provider)
        self.assertEqual(completer._ArgumentParserCompleter__offer_action_suggestions(action, 1, "", "--value example "), ([], True))
        provider.get_completion_suggestions.assert_not_called()


if __name__ == "__main__":
    unittest.main()
