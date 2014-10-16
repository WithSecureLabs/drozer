import functools
import unittest

from drozer.modules import collection, loader

class ModuleCollectionTestCase(unittest.TestCase):

    def testItShouldLoadModules(self):
        modules = collection.ModuleCollection(loader.ModuleLoader())

        assert len(modules.all()) > 0

    def testItShouldReloadModules(self):
        modules = collection.ModuleCollection(loader.ModuleLoader())
        modules.all()
        modules.reload()

        assert len(modules.all()) > 0


def CollectionTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ModuleCollectionTestCase("testItShouldLoadModules"))
    suite.addTest(ModuleCollectionTestCase("testItShouldReloadModules"))

    return suite
  

if __name__ == "__main__":
    unittest.TextTestRunner().run(CollectionTestSuite())
