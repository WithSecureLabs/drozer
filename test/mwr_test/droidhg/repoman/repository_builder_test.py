import ConfigParser
import os
import shutil
import unittest

from mwr.common import fs

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman.installer import ModuleInstaller
from mwr.droidhg.repoman.repositories import Repository
from mwr.droidhg.repoman.repository_builder import RepositoryBuilder

class RepositoryBuilderTestCase(unittest.TestCase):
    
    def setUp(self):
        Configuration._Configuration__config = ConfigParser.SafeConfigParser()
        
        shutil.rmtree("./tmp", True)
        shutil.rmtree("./repo", True)
        
        Repository.create("./tmp")
        fs.write("./tmp/a.local.module", "This is a local, raw module.")
        ModuleInstaller("./tmp").install(["./tmp/a.local.module"])
    
    def tearDown(self):
        shutil.rmtree("./tmp", True)
        shutil.rmtree("./repo", True)
    
    def testItShouldBuildAModuleRepository(self):
        RepositoryBuilder("./tmp", "./repo").build()
        
        assert os.path.exists("./repo")
        assert os.path.exists("./repo/INDEX.xml")
        assert os.path.exists("./repo/a.local.module")
        
        assert "a.local.module" in fs.read("./repo/INDEX.xml")
    
    def testItShouldBuildAModuleRepositoryWithPackage(self):
        fs.touch("./tmp/a/local/.mercury_package")
        
        RepositoryBuilder("./tmp", "./repo").build()
        
        assert os.path.exists("./repo")
        assert os.path.exists("./repo/INDEX.xml")
        assert os.path.exists("./repo/a.local")
        
        assert "a.local" in fs.read("./repo/INDEX.xml")
        assert fs.read("./repo/a.local")[0:4] == "\x50\x4b\x03\x04"

    
def RepositoryBuilderTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(RepositoryBuilderTestCase("testItShouldBuildAModuleRepository"))
    suite.addTest(RepositoryBuilderTestCase("testItShouldBuildAModuleRepositoryWithPackage"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(RepositoryBuilderTestSuite())
    