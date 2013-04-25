import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectedStringTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def testItShouldAddTwoReflectedStrings(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = reflection.types.ReflectedString(" World")

        assert s1 + s2 == "Hello World"

    def testItShouldAddAReflectedAndANativeString(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = " World"

        assert s1 + s2 == "Hello World"

    def testItShouldShowAReflectedStringContainsAReflectedString(self):
        s1 = reflection.types.ReflectedString("Hello World")
        s2 = reflection.types.ReflectedString("Hello")

        assert s2 in s1

    def testItShouldShowAReflectedStringDoesNotContainAReflectedString(self):
        s1 = reflection.types.ReflectedString("Hello World")
        s2 = reflection.types.ReflectedString("Fred")

        assert not s2 in s1

    def testItShouldShowAReflectedStringContainsANativeString(self):
        s1 = reflection.types.ReflectedString("Hello World")
        s2 = "Hello"

        assert s2 in s1

    def testItShouldShowAReflectedStringDoesNotContainANativeString(self):
        s1 = reflection.types.ReflectedString("Hello World")
        s2 = "Fred"

        assert not s2 in s1

    def testItShouldEqualAReflectedString(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = reflection.types.ReflectedString("Hello")

        assert s1 == s2

    def testItShouldNotEqualAReflectedString(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = reflection.types.ReflectedString("World")

        assert s1 != s2

    def testItShouldEqualANativeString(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = "Hello"

        assert s1 == s2

    def testItShouldNotEqualANativeString(self):
        s1 = reflection.types.ReflectedString("Hello")
        s2 = "World"

        assert s1 != s2

    def testItShouldSupportFormats(self):
        s1 = reflection.types.ReflectedString("Insert {} Here...")

        assert s1.format("something") == "Insert something Here..."

    # TODO: '__ge__',

    def testItShouldSupportIndexing(self):
        s1 = reflection.types.ReflectedString("Hello, World!")

        assert s1[2] == "l"

    # TODO: '__gt__', '__le__'

    def testItShouldGetTheLength(self):
        s1 = reflection.types.ReflectedString("Hello, World!")

        assert len(s1) == 13
    
    # TODO: '__lt__', '__mod__', '__mul__', '__ne__', '__reduce__', '__reduce_ex__',

    def testItShouldGetTheRepresentation(self):
        s1 = reflection.types.ReflectedString("Hello, World!")

        assert repr(s1) == repr("Hello, World!")

    # TODO: '__rmod__', '__rmul__', '__sizeof__',

    def testItShouldCastToString(self):
        s1 = reflection.types.ReflectedString("Hello, World!")

        assert str(s1) == "Hello, World!"

    def testItShouldCapitalize(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.capitalize() == "Word"

    def testItShouldCenter(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.center(8) == "  word  "

    def testItShouldCount(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.count("w") == 1

    def testItShouldEndWith(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.endswith("d")

    def testItShouldNotEndWith(self):
        s1 = reflection.types.ReflectedString("word")

        assert not s1.endswith("z")

    def testItShouldExpandTabs(self):
        s1 = reflection.types.ReflectedString("\tword")
        
        assert s1.expandtabs() == "        word"

    def testItShouldFind(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.find("o") == 1

    def testItShouldNotFind(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.find("z") == -1

    def testItShouldGetIndex(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.index("o") == 1

    def testItShouldNotGetIndex(self):
        s1 = reflection.types.ReflectedString("word")

        try:
            s1.index("z")

            assert False, "expected ValueError"
        except ValueError:
            pass

    def testItShouldBeALNum(self):
        assert reflection.types.ReflectedString("word").isalnum()
        assert reflection.types.ReflectedString("word2").isalnum()
        assert reflection.types.ReflectedString("123").isalnum()

    def testItShouldNotBeALNum(self):
        assert not reflection.types.ReflectedString("Hello!").isalnum()

    def testItShouldBeAlpha(self):
        assert reflection.types.ReflectedString("word").isalpha()

    def testItShouldNotBeAlpha(self):
        assert not reflection.types.ReflectedString("word2").isalpha()
        assert not reflection.types.ReflectedString("123").isalpha()

    def testItShouldBeADigit(self):
        assert reflection.types.ReflectedString("123").isdigit()

    def testItShouldNotBeADigit(self):
        assert not reflection.types.ReflectedString("word").isdigit()
        assert not reflection.types.ReflectedString("word2").isdigit()

    def testItShouldBeLower(self):
        assert reflection.types.ReflectedString("word").islower()

    def testItShouldNotBeLower(self):
        assert not reflection.types.ReflectedString("Word").islower()
        assert not reflection.types.ReflectedString("123").islower()
        assert not reflection.types.ReflectedString(" ").islower()

    def testItShouldSpace(self):
        assert reflection.types.ReflectedString(" ").isspace()

    def testItShouldNotBeSpace(self):
        assert not reflection.types.ReflectedString("word").isspace()
        assert not reflection.types.ReflectedString("Word").isspace()
        assert not reflection.types.ReflectedString("123").isspace()

    def testItShouldBeTitle(self):
        assert reflection.types.ReflectedString("Title Case").istitle()

    def testItShouldNotBeTitle(self):
        assert not reflection.types.ReflectedString("CamelCase").istitle()
        assert not reflection.types.ReflectedString("SCREAMING_SNAKE_CASE").istitle()
        assert not reflection.types.ReflectedString("Sentence case").istitle()
        assert not reflection.types.ReflectedString("snake_cake").istitle()
        assert not reflection.types.ReflectedString("UPPER CASE").istitle()

    def testItShouldBeUpper(self):
        assert reflection.types.ReflectedString("UPPER CASE").isupper()
        assert reflection.types.ReflectedString("SCREAMING_SNAKE_CASE").isupper()

    def testItShouldNotBeUpper(self):
        assert not reflection.types.ReflectedString("Title Case").isupper()
        assert not reflection.types.ReflectedString("CamelCase").isupper()
        assert not reflection.types.ReflectedString("Sentence case").isupper()
        assert not reflection.types.ReflectedString("snake_cake").isupper()

    def testItShouldJoin(self):
        s1 = reflection.types.ReflectedString("The quick")
        s2 = reflection.types.ReflectedString("brown fox jumped")
        s3 = "over the lazy dog."
        sp = reflection.types.ReflectedString(" ")

        assert sp.join([s1, s2, s3]) == "The quick brown fox jumped over the lazy dog."

    def testItShouldLJust(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.ljust(10) == "word      "

    def testItShouldLower(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.lower() == "the quick brown fox jumped over the lazy dog."

    def testItShouldLStrip(self):
        s1 = reflection.types.ReflectedString("  with whitespace  ")

        assert s1.lstrip() == "with whitespace  "

    def testItShouldPartition(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.partition("brown") == ("The quick ", "brown", " fox jumped over the lazy dog.")

    def testItShouldReplace(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.replace("dog", "zebra") == "The quick brown fox jumped over the lazy zebra."

    def testItShouldRFind(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.rfind("e") == 34

    def testItShouldNotRFind(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.rfind("hippo") == -1

    def testItShouldRIndex(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.rindex("e") == 34

    def testItShouldNotRIndex(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        try:
            s1.rindex("hippo")

            assert False, "expected ValueError"
        except ValueError:
            pass

    def testItShouldRJust(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.rjust(10) == "      word"

    def testItShouldRPartition(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.rpartition("e") == ("The quick brown fox jumped over th", "e", " lazy dog.")

    def testItShouldRSplit(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.rsplit("e", 1) == ["The quick brown fox jumped over th", " lazy dog."]

    def testItShouldRStrip(self):
        s1 = reflection.types.ReflectedString("  with whitespace  ")

        assert s1.rstrip() == "  with whitespace"

    def testItShouldSplit(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.split("e") == ["Th", " quick brown fox jump", "d ov", "r th", " lazy dog."]

    def testItShouldSplitLines(self):
        s1 = reflection.types.ReflectedString("The quick brown\nfox jumped over\nthe lazy dog.")

        assert s1.splitlines() == ["The quick brown", "fox jumped over", "the lazy dog."]

    def testItShouldStartWith(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.startswith("T")

    def testItShouldNotStartWith(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert not s1.startswith("Z")

    def testItShouldStrip(self):
        s1 = reflection.types.ReflectedString("  with whitespace  ")

        assert s1.strip() == "with whitespace"

    def testItShouldSwapCase(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.swapcase() == "tHE QUICK BROWN FOX JUMPED OVER THE LAZY DOG."

    def testItShouldTitle(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.title() == "The Quick Brown Fox Jumped Over The Lazy Dog."

    def testItShouldUpper(self):
        s1 = reflection.types.ReflectedString("The quick brown fox jumped over the lazy dog.")

        assert s1.upper() == "THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG."

    def testItShouldZFill(self):
        s1 = reflection.types.ReflectedString("word")

        assert s1.zfill(8) == "0000word"


def ReflectedStringTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectedStringTestCase("testItShouldAddTwoReflectedStrings"))
    suite.addTest(ReflectedStringTestCase("testItShouldAddAReflectedAndANativeString"))
    suite.addTest(ReflectedStringTestCase("testItShouldShowAReflectedStringContainsAReflectedString"))
    suite.addTest(ReflectedStringTestCase("testItShouldShowAReflectedStringDoesNotContainAReflectedString"))
    suite.addTest(ReflectedStringTestCase("testItShouldShowAReflectedStringContainsANativeString"))
    suite.addTest(ReflectedStringTestCase("testItShouldShowAReflectedStringDoesNotContainANativeString"))
    suite.addTest(ReflectedStringTestCase("testItShouldEqualAReflectedString"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotEqualAReflectedString"))
    suite.addTest(ReflectedStringTestCase("testItShouldEqualANativeString"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotEqualANativeString"))
    suite.addTest(ReflectedStringTestCase("testItShouldSupportFormats"))
    suite.addTest(ReflectedStringTestCase("testItShouldSupportIndexing"))
    suite.addTest(ReflectedStringTestCase("testItShouldGetTheLength"))
    suite.addTest(ReflectedStringTestCase("testItShouldGetTheRepresentation"))
    suite.addTest(ReflectedStringTestCase("testItShouldCastToString"))
    suite.addTest(ReflectedStringTestCase("testItShouldCapitalize"))
    suite.addTest(ReflectedStringTestCase("testItShouldCenter"))
    suite.addTest(ReflectedStringTestCase("testItShouldCount"))
    suite.addTest(ReflectedStringTestCase("testItShouldEndWith"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotEndWith"))
    suite.addTest(ReflectedStringTestCase("testItShouldExpandTabs"))
    suite.addTest(ReflectedStringTestCase("testItShouldFind"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotFind"))
    suite.addTest(ReflectedStringTestCase("testItShouldGetIndex"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotGetIndex"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeALNum"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeALNum"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeAlpha"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeAlpha"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeADigit"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeADigit"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeLower"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeLower"))
    suite.addTest(ReflectedStringTestCase("testItShouldSpace"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeSpace"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeTitle"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeTitle"))
    suite.addTest(ReflectedStringTestCase("testItShouldBeUpper"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotBeUpper"))
    suite.addTest(ReflectedStringTestCase("testItShouldJoin"))
    suite.addTest(ReflectedStringTestCase("testItShouldLJust"))
    suite.addTest(ReflectedStringTestCase("testItShouldLower"))
    suite.addTest(ReflectedStringTestCase("testItShouldLStrip"))
    suite.addTest(ReflectedStringTestCase("testItShouldPartition"))
    suite.addTest(ReflectedStringTestCase("testItShouldReplace"))
    suite.addTest(ReflectedStringTestCase("testItShouldRFind"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotRFind"))
    suite.addTest(ReflectedStringTestCase("testItShouldRIndex"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotRIndex"))
    suite.addTest(ReflectedStringTestCase("testItShouldRJust"))
    suite.addTest(ReflectedStringTestCase("testItShouldRPartition"))
    suite.addTest(ReflectedStringTestCase("testItShouldRSplit"))
    suite.addTest(ReflectedStringTestCase("testItShouldRStrip"))
    suite.addTest(ReflectedStringTestCase("testItShouldSplit"))
    suite.addTest(ReflectedStringTestCase("testItShouldSplitLines"))
    suite.addTest(ReflectedStringTestCase("testItShouldStartWith"))
    suite.addTest(ReflectedStringTestCase("testItShouldNotStartWith"))
    suite.addTest(ReflectedStringTestCase("testItShouldStrip"))
    suite.addTest(ReflectedStringTestCase("testItShouldSwapCase"))
    suite.addTest(ReflectedStringTestCase("testItShouldTitle"))
    suite.addTest(ReflectedStringTestCase("testItShouldUpper"))
    suite.addTest(ReflectedStringTestCase("testItShouldZFill"))
    
    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectedStringTestSuite())
