import argparse
import unittest

from mwr.common import argparse_completer

class ArgumentParserCompleterTestCase(unittest.TestCase):
    
    def setUp(self):
        self.parser = argparse.ArgumentParser(add_help=False)
        
        self.suggestions_for = None
    
    def get_completion_suggestions(self, action, text, **kwargs):
        self.suggestions_for = (action, text, kwargs)
    
    def testItShouldOfferToCompleteAFlag(self):
        self.parser.add_argument("--one", nargs=1)
        self.parser.add_argument("--two", nargs=1)
        self.parser.add_argument("--three", nargs=1)
        
        suggestions = argparse_completer\
            .ArgumentParserCompleter(self.parser, self)\
            .get_suggestions("", "", 0, 0)
        
        assert suggestions == ["--one", "--two", "--three"], suggestions
    
    def testItShouldOnlyOfferValidCompletionsForAFlag(self):
        self.parser.add_argument("--one", nargs=1)
        self.parser.add_argument("--two", nargs=1)
        self.parser.add_argument("--three", nargs=1)
        
        suggestions = argparse_completer\
            .ArgumentParserCompleter(self.parser, self)\
            .get_suggestions("--t", "--t", 0, 3)
        
        assert suggestions == ["--two", "--three"], suggestions
    
    def testItShouldNotOfferChoicesAfterAFlagsNArgs(self):
        self.parser.add_argument("--one", nargs=1)
        self.parser.add_argument("--two", nargs=2)
        self.parser.add_argument("--three", nargs=3)
        
        suggestions = argparse_completer\
            .ArgumentParserCompleter(self.parser, self)\
            .get_suggestions("", "--two 1 2 ", 10, 10)
        
        assert suggestions == ["--one", "--two", "--three"], suggestions
        assert self.suggestions_for == None
        
    def testItShouldPassTheIdWhenCompletingTheNthArg(self):
        self.parser.add_argument("--one", nargs=1)
        self.parser.add_argument("--two", nargs=2)
        self.parser.add_argument("--three", nargs=3)
        
        suggestions = argparse_completer\
            .ArgumentParserCompleter(self.parser, self)\
            .get_suggestions("", "--two 1 ", 8, 8)
        
        assert suggestions == [], suggestions
        assert self.suggestions_for[0].dest == "two"
        assert self.suggestions_for[2]['idx'] == 1
    
    def testItShouldNotCompleteAFlagBeforeAllPositionalArguments(self):
        self.parser.add_argument("positional", nargs=1)
        self.parser.add_argument("--one", nargs=1)
        self.parser.add_argument("--two", nargs=1)
        self.parser.add_argument("--three", nargs=1)
        
        suggestions = argparse_completer\
            .ArgumentParserCompleter(self.parser, self)\
            .get_suggestions("", "", 0, 0)
        
        assert suggestions == [], suggestions
        assert self.suggestions_for[0].dest == "positional"
    
    
def ArgumentParserCompleterTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ArgumentParserCompleterTestCase("testItShouldOfferToCompleteAFlag"))
    suite.addTest(ArgumentParserCompleterTestCase("testItShouldOnlyOfferValidCompletionsForAFlag"))
    suite.addTest(ArgumentParserCompleterTestCase("testItShouldNotOfferChoicesAfterAFlagsNArgs"))
    suite.addTest(ArgumentParserCompleterTestCase("testItShouldPassTheIdWhenCompletingTheNthArg"))
    suite.addTest(ArgumentParserCompleterTestCase("testItShouldNotCompleteAFlagBeforeAllPositionalArguments"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ArgumentParserCompleterTestSuite())
    