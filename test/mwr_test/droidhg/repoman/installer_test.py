import ConfigParser
import os
import shutil
import unittest

from mwr.common import fs

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman.installer import ModuleInstaller
from mwr.droidhg.repoman.repositories import Repository

class ModuleInstallerTestCase(unittest.TestCase):
    
    def setUp(self):
        Configuration._Configuration__config = ConfigParser.SafeConfigParser()
        
        shutil.rmtree("./tmp", True)
        
        Repository.create("./tmp")
    
    def tearDown(self):
        shutil.rmtree("./tmp", True)
    
    def testItShouldInstallARawModuleFromALocalSource(self):
        fs.write("./tmp/a.local.module", "This is a local, raw module.")
        
        ModuleInstaller("./tmp").install(["./tmp/a.local.module"])
        
        assert os.path.exists("./tmp/a")
        assert os.path.exists("./tmp/a/__init__.py")
        assert os.path.exists("./tmp/a/local")
        assert os.path.exists("./tmp/a/local/__init__.py")
        assert os.path.exists("./tmp/a/local/module.py")
        
        assert fs.read("./tmp/a/local/module.py") == "This is a local, raw module."
        
    def testItShouldInstallAnArchiveModuleFromALocalSource(self):
        ModuleInstaller("./tmp").install(["./test/mwr_test/mocks/a.local.zip"])
        
        assert os.path.exists("./tmp/a")
        assert os.path.exists("./tmp/a/__init__.py")
        assert os.path.exists("./tmp/a/local")
        assert os.path.exists("./tmp/a/local/__init__.py")
        assert os.path.exists("./tmp/a/local/module.py")
        
        assert fs.read("./tmp/a/local/module.py") == "This is a local, archived module.\n"
        
    
def ModuleInstallerTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ModuleInstallerTestCase("testItShouldInstallARawModuleFromALocalSource"))
    suite.addTest(ModuleInstallerTestCase("testItShouldInstallAnArchiveModuleFromALocalSource"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ModuleInstallerTestSuite())
    