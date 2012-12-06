import ConfigParser
import unittest

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman import Repository

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
    
def RepositoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(RepositoryTestCase("testItShouldRetrieveNoAdditionalRepositories"))
    suite.addTest(RepositoryTestCase("testItShouldRetrieveAnAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldRetrieveAllWithoutAConfigFile"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathAsDefault"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithAnAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithTwoAdditionalRepository"))
    suite.addTest(RepositoryTestCase("testItShouldBuildDroidhgModulesPathWithoutAConfigFile"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(RepositoryTestSuite())
    