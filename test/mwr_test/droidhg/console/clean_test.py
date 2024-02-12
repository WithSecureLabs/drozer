import unittest

#from mwr_test.droidhg.console import clean_mock_reflector

import test.mwr_test.droidhg.console clean_mock_reflector

from mwr.droidhg.console import clean

class CleanTestCase(unittest.TestCase):

    def setUp(self):
        self.reflector = clean_mock_reflector.MockReflector()

    def testException(self):
        
        with self.assertRaises(AttributeError):
            clean.clean(None)

    def testDeletesAPKFiles(self):

        clean.clean(self.reflector)

        cache = self.reflector.klass.context.cache.files

        self.assertEqual(cache[1].toString(), "---", "APK File not deleted: %s" %cache[1].toString())
        self.assertEqual(cache[3].toString(), "---", "APK File not deleted: %s" %cache[3].toString())

    def testDeletesDEXFiles(self):
        
        clean.clean(self.reflector)

        cache = self.reflector.klass.context.cache.files

        self.assertEqual(cache[0].toString(), "---", "DEX File not deleted: %s" %cache[0].toString())
        self.assertEqual(cache[2].toString(), "---", "DEX File not deleted: %s" %cache[2].toString())

    def testDeletesBothFiles(self):

        clean.clean(self.reflector)

        cache = self.reflector.klass.context.cache.files

        self.assertEqual(cache[0].toString(), "---", "DEX File not deleted: %s" %cache[0].toString())
        self.assertEqual(cache[2].toString(), "---", "DEX File not deleted: %s" %cache[2].toString())
        self.assertEqual(cache[1].toString(), "---", "APK File not deleted: %s" %cache[1].toString())
        self.assertEqual(cache[3].toString(), "---", "APK File not deleted: %s" %cache[3].toString())

    def testDoesNotDeleteOtherFiles(self):

        clean.clean(self.reflector)

        cache = self.reflector.klass.context.cache.files

        self.assertNotEqual(cache[4].toString(), "---", "non DEX File deleted: %s" %cache[4].toString())
        self.assertNotEqual(cache[5].toString(), "---", "non DEX File deleted: %s" %cache[5].toString())
        self.assertNotEqual(cache[6].toString(), "---", "non APK File deleted: %s" %cache[6].toString())
        self.assertNotEqual(cache[7].toString(), "---", "non DEX File deleted: %s" %cache[7].toString())
        self.assertNotEqual(cache[8].toString(), "---", "non APK File deleted: %s" %cache[8].toString())

    def testDeletedFilesCount(self):

        cleaned = clean.clean(self.reflector)        

        self.assertEqual(cleaned, 4, "Incorrect Value Returned: %d" %cleaned)

def CleanTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(CleanTestCase("testDeletedFilesCount"))
    suite.addTest(CleanTestCase("testDoesNotDeleteOtherFiles"))
    suite.addTest(CleanTestCase("testDeletesBothFiles"))
    suite.addTest(CleanTestCase("testDeletesDEXFiles"))
    suite.addTest(CleanTestCase("testDeletesAPKFiles"))
    suite.addTest(CleanTestCase("testException"))
        
if __name__ == '__main__':
    unittest.main()

