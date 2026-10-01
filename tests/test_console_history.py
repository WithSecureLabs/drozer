import io
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from reversec.common.cmd_ext import Cmd


class ConsoleHistoryTests(unittest.TestCase):
    def setUp(self):
        self.console = Cmd()
        self.console.stdout = io.StringIO()
        self.console.stderr = io.StringIO()

    def test_append_redirection_preserves_append_mode(self):
        output = self.console.stdout
        with patch("reversec.common.cmd_ext.system.Tee", return_value=io.StringIO()) as tee:
            self.assertEqual(self.console.precmd("echo value >> result.txt"), "echo value ")
            tee.assert_called_once_with(output, "result.txt", "a")

    def test_overwrite_redirection_preserves_write_mode(self):
        output = self.console.stdout
        with patch("reversec.common.cmd_ext.system.Tee", return_value=io.StringIO()) as tee:
            self.assertEqual(self.console.precmd("echo value > result.txt"), "echo value ")
            tee.assert_called_once_with(output, "result.txt", "w")

    def test_whole_command_recall_without_arguments(self):
        self.console.lastcmd = "help"
        self.assertEqual(self.console.precmd("!!"), "help")

    def test_missing_first_argument_has_clear_error(self):
        self.console.lastcmd = "help"
        self.assertEqual(self.console.precmd("echo !^"), "")
        self.assertIn("no previous argument", self.console.stderr.getvalue())

    def test_existing_first_argument_recall(self):
        self.console.lastcmd = "echo first last"
        self.assertEqual(self.console.precmd("echo !^"), "echo first")


if __name__ == "__main__":
    unittest.main()
