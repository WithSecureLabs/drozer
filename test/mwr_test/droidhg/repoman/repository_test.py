import ConfigParser
import os
import shutil
import unittest

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman.repositories import Repository, NotEmptyException, UnknownRepository

class RepositoryTestCase(unittest.TestCase):
    
    def mockConfigWithRepos(self, repositories):
        config = ConfigParser.SafeConfigParser()
        
        config.add_section('repositories')
        for repo in repositories:
            config.set('repositories', repo, repo)
        
        return config
    
    def mockConfigWithoutRepos(self):
        return ConfigParser.SafeConfigParser()
    
    def testItShouldRetrieveNoAdditionalRepositories(self):
        Configuration._Configuration__config = self.mockConfigWithRepos([])
        
        assert Repository.all() == []
    
    def testItShouldRetrieveAnAdditionalRepository(self):
        Configuration._Configuration__config = self.mockConfigWithRepos(['/usr/local/mercury/modules'])
        
        assert Repository.all() == ['/usr/local/mercury/modules']
    
    def testItShouldRetrieveAllWithoutAConfigFile(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        assert Repository.all() == []
    
    def testItShouldBuildDroidhgModulesPathAsDefault(self):
        Configuration._Configuration__config = self.mockConfigWithRepos([])
        
        assert Repository.droidhg_modules_path() == ""
    
    def testItShouldBuildDroidhgModulesPathWithAnAdditionalRepository(self):
        Configuration._Configuration__config = self.mockConfigWithRepos(['/usr/local/mercury/modules'])
        
        assert Repository.droidhg_modules_path() == "/usr/local/mercury/modules"
        
    def testItShouldBuildDroidhgModulesPathWithTwoAdditionalRepository(self):
        Configuration._Configuration__config = self.mockConfigWithRepos(['/usr/local/mercury/modules', '/tmp/modules'])
        
        assert Repository.droidhg_modules_path() == "/usr/local/mercury/modules:/tmp/modules"
        
    def testItShouldBuildDroidhgModulesPathWithoutAConfigFile(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        assert Repository.droidhg_modules_path() == ""
    
    def testItShouldCreateAModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        Repository.create("./tmp")
        
        assert os.path.exists("./tmp")
        assert os.path.exists("./tmp/__init__.py")
        assert os.path.exists("./tmp/.mercury_repository")
        
        assert Repository.all() == ["./tmp"]
        
        shutil.rmtree("./tmp")
    
    def testItShouldNotCreateARepositoryOverAnExistingRecord(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        Repository.create("./tmp")
        
        try:
            Repository.create("./tmp")
            assert False, "expected NotEmptyException"
        except NotEmptyException:
            pass
        
        shutil.rmtree("./tmp")
    
    def testItShouldNotCreateARepositoryOverAnExistingFolder(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        os.mkdir("./tmp")
        
        try:
            Repository.create("./tmp")
            assert False, "expected NotEmptyException"
        except NotEmptyException:
            pass
        
        shutil.rmtree("./tmp")
    
    def testItShouldDeleteAModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        Repository.create("./tmp")
        Repository.delete("./tmp")
        
        assert not os.path.exists("./tmp")
        
        assert Repository.all() == []
    
    def testItShouldNotDeleteAnUnknownRepository(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        os.mkdir("./tmp")
        
        try:
            Repository.delete("./tmp")
            
            assert False, "expected UnknownRepository"
        except UnknownRepository:
            pass
        
        assert os.path.exists("./tmp")
        
        shutil.rmtree("./tmp")
    
    def testItShouldEnableAModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        Repository.create("./tmp")
        
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        Repository.enable("./tmp")
        
        assert Repository.all() == ["./tmp"]
        
        shutil.rmtree("./tmp")
    
    def testItShouldNotEnableAFolderThatIsnNotAModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithoutRepos()
        
        os.mkdir("./tmp")
        
        try:
            Repository.enable("./tmp")
            
            assert False, "expected UnknownRepository"
        except UnknownRepository:
            pass
        
        assert Repository.all() == []
        
        shutil.rmtree("./tmp")
    
    def testItShouldDisableAModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithRepos([])
        
        Repository.create("./tmp")
        Repository.disable("./tmp")
        
        assert os.path.exists("./tmp")
        assert os.path.exists("./tmp/__init__.py")
        assert os.path.exists("./tmp/.mercury_repository")
        
        assert Repository.all() == []
        
        shutil.rmtree("./tmp")
    
    def testItShouldNotDisableAnUnknownModuleRepository(self):
        Configuration._Configuration__config = self.mockConfigWithRepos([])
        
        try:
            Repository.disable("./tmp")
            
            assert False, "expected UnknownRepository"
        except UnknownRepository:
            pass
    
def RepositoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(RepositoryTestCase("testItShouldRetrieveNoAdditionalRepositories"))
    suite.addTest(RepositoryTestCase("testItShouldRetrieveAnAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldRetrieveAllWithoutAConfigFile"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathAsDefault"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithAnAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithTwoAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithoutAConfigFile"))
    suite.addTest(RepositoryTestCase("testItShouldCreateAModuleRepository"))
    suite.addTest(RepositoryTestCase("testItShouldNotCreateARepositoryOverAnExistingRecord"))
    suite.addTest(RepositoryTestCase("testItShouldNotCreateARepositoryOverAnExistingFolder"))
    suite.addTest(RepositoryTestCase("testItShouldDeleteAModuleRepository"))
    suite.addTest(RepositoryTestCase("testItShouldNotDeleteAnUnknownRepository"))
    suite.addTest(RepositoryTestCase("testItShouldEnableAModuleRepository"))
    suite.addTest(RepositoryTestCase("testItShouldNotEnableAFolderThatIsnNotAModuleRepository"))
    suite.addTest(RepositoryTestCase("testItShouldDisableAModuleRepository"))
    suite.addTest(RepositoryTestCase("testItShouldNotDisableAnUnknownModuleRepository"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(RepositoryTestSuite())
    