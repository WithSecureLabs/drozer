import unittest

from mwr.droidhg.modules.base import ImportConflictResolver
from mwr.droidhg.modules.app import package

class ImportConflictResolverTestCase(unittest.TestCase):
    
    class MyModule(object):
        
        @classmethod
        def fqmn(cls):
            return "app.package.info"
    
    class MyOtherModule(object):
        
        @classmethod
        def fqmn(cls):
            return "app.package.info"
    
    def testItShouldKeepABuiltInOverAnExtension(self):
        assert ImportConflictResolver().resolve(package.Info, ImportConflictResolverTestCase.MyModule) == package.Info
    
    def testItShouldDiscardAnExtensionForABuiltIn(self):
        assert ImportConflictResolver().resolve(ImportConflictResolverTestCase.MyModule, package.Info) == package.Info
    
    def testItShouldKeepDeterministicallyKeepExtensions(self):
        assert ImportConflictResolver().resolve(ImportConflictResolverTestCase.MyModule, ImportConflictResolverTestCase.MyOtherModule) == ImportConflictResolverTestCase.MyModule
        assert ImportConflictResolver().resolve(ImportConflictResolverTestCase.MyOtherModule, ImportConflictResolverTestCase.MyModule) == ImportConflictResolverTestCase.MyModule


def ImportConflictResolverTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ImportConflictResolverTestCase("testItShouldKeepABuiltInOverAnExtension"))
    suite.addTest(ImportConflictResolverTestCase("testItShouldDiscardAnExtensionForABuiltIn"))
    suite.addTest(ImportConflictResolverTestCase("testItShouldKeepDeterministicallyKeepExtensions"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ImportConflictResolverTestSuite())
