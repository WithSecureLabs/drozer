import ConfigParser
import unittest

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman import Remote

class RemoteTestCase(unittest.TestCase):
    
    def mockConfigWithRemotes(self, remotes):
        config = ConfigParser.SafeConfigParser()
        
        config.add_section('remotes')
        for url in remotes:
            config.set('remotes', url, url)
        
        return config
    
    def mockConfigWithoutRemotes(self):
        return ConfigParser.SafeConfigParser()
    
    def testItShouldRetrieveNoRemotes(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes([])
        
        assert Remote.all() == []
    
    def testItShouldRetrieveASingleRemote(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes(['http://www.mercury.com'])
        
        assert Remote.all() == ['http://www.mercury.com']
    
    def testItShouldRetrieveAllWithoutAConfigFile(self):
        Configuration._Configuration__config = self.mockConfigWithoutRemotes()
        
        assert Remote.all() == []
    
def RemoteTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(RemoteTestCase("testItShouldRetrieveNoRemotes"))
    suite.addTest(RemoteTestCase("testItShouldRetrieveASingleRemote"))
    suite.addTest(RemoteTestCase("testItShouldRetrieveAllWithoutAConfigFile"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(RemoteTestSuite())
    