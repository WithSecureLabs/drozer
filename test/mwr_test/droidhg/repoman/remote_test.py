import ConfigParser
import unittest

from mwr.droidhg.configuration import Configuration
from mwr.droidhg.repoman.remotes import Remote, UnknownRemote

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
        # if there are no remotes specified, we should create a default one pointing
        # to the Github repository
        
        assert Remote.all() == ['https://raw.github.com/mwrlabs/mercury-modules/repository/']
    
    def testItShouldAddARemote(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes([])
        
        assert Remote.create("http://myremote.com/")
        assert Remote.all() == ["http://myremote.com/"]
    
    def testItShouldNotReAddARemote(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes(["http://myremote.com/"])
        
        assert not Remote.create("http://myremote.com/")
        assert Remote.all() == ["http://myremote.com/"]
        
    def testItShouldRemoveARemote(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes(["http://myremote.com/"])
        
        assert Remote.delete("http://myremote.com/")
        assert Remote.all() == []
        
    def testItShouldNotRemoteARemoteTheDoesNotExist(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes([])
        
        try:
            assert Remote.delete("http://myremote.com/")
            
            assert False, "expected UnknownRemote"
        except UnknownRemote:
            pass
    
    def testItShouldGetARemote(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes(["http://myremote.com/"])
        
        assert isinstance(Remote.get("http://myremote.com/"), Remote)
    
    def testItShouldGetNoneIfARemoteDoesNotExist(self):
        Configuration._Configuration__config = self.mockConfigWithRemotes([])
        
        assert Remote.get("http://myremote.com/") == None
    
    def testItShouldConstructAValidDownloadPathIfATrailingSlashIsGiven(self):
        assert Remote("http://myremote.com/").buildPath("INDEX") == "http://myremote.com/INDEX"
    
    def testItShouldConstructAValidDownloadPathIfNoTrailingSlashIsGiven(self):
        assert Remote("http://myremote.com").buildPath("INDEX") == "http://myremote.com/INDEX"
    
def RemoteTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(RemoteTestCase("testItShouldRetrieveNoRemotes"))
    suite.addTest(RemoteTestCase("testItShouldRetrieveASingleRemote"))
    suite.addTest(RemoteTestCase("testItShouldRetrieveAllWithoutAConfigFile"))
    suite.addTest(RemoteTestCase("testItShouldAddARemote"))
    suite.addTest(RemoteTestCase("testItShouldNotReAddARemote"))
    suite.addTest(RemoteTestCase("testItShouldRemoveARemote"))
    suite.addTest(RemoteTestCase("testItShouldNotRemoteARemoteTheDoesNotExist"))
    suite.addTest(RemoteTestCase("testItShouldGetARemote"))
    suite.addTest(RemoteTestCase("testItShouldGetNoneIfARemoteDoesNotExist"))
    suite.addTest(RemoteTestCase("testItShouldConstructAValidDownloadPathIfATrailingSlashIsGiven"))
    suite.addTest(RemoteTestCase("testItShouldConstructAValidDownloadPathIfNoTrailingSlashIsGiven"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(RemoteTestSuite())
    