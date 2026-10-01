import io
import os
import tempfile
import unittest
import zipfile

from drozer.repoman.installer import AlreadyInstalledError, ModuleInstaller


class ModuleInstallerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.installer = ModuleInstaller(self.directory.name)

    def install(self, name, source, force=False):
        return self.installer._ModuleInstaller__install_module(
            lambda module: source, name, force
        )

    def archive(self, source):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("example.py", source)
        return buffer.getvalue()

    def test_zip_bytes_are_extracted(self):
        source = b"value = 1\n"
        self.assertTrue(self.install("example.zip", self.archive(source)))
        with open(os.path.join(self.directory.name, "example", "example.py"), "rb") as module:
            self.assertEqual(module.read(), source)
        self.assertFalse(os.path.exists(os.path.join(self.directory.name, "example.zip.py")))

    def test_zip_overwrite_requires_force(self):
        self.install("example.zip", self.archive(b"value = 1\n"))
        with self.assertRaises(AlreadyInstalledError):
            self.install("example.zip", self.archive(b"value = 2\n"))
        self.assertTrue(self.install("example.zip", self.archive(b"value = 2\n"), force=True))
        with open(os.path.join(self.directory.name, "example", "example.py"), "rb") as module:
            self.assertEqual(module.read(), b"value = 2\n")

    def test_raw_bytes_still_install(self):
        source = b"value = 1\n"
        self.assertTrue(self.install("example", source))
        with open(os.path.join(self.directory.name, "example.py"), "rb") as module:
            self.assertEqual(module.read(), source)


if __name__ == "__main__":
    unittest.main()
