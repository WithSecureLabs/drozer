import unittest

from mwr.common import stream as coloured_stream

class ColouredStreamTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def testItShouldColourTextBlue(self):
        assert coloured_stream.format_colors("this text is [color blue]blue[/color]") == "this text is \033[94mblue\033[0m"

    def testItShouldColourTextGreen(self):
        assert coloured_stream.format_colors("this text is [color green]green[/color]") == "this text is \033[92mgreen\033[0m"

    def testItShouldColourTextPurple(self):
        assert coloured_stream.format_colors("this text is [color purple]purple[/color]") == "this text is \033[95mpurple\033[0m"

    def testItShouldColourTextRed(self):
        assert coloured_stream.format_colors("this text is [color red]red[/color]") == "this text is \033[91mred\033[0m"

    def testItShouldColourTextYellow(self):
        assert coloured_stream.format_colors("this text is [color yellow]yellow[/color]") == "this text is \033[93myellow\033[0m"

    def testItShouldRemoveColourBlue(self):
        assert coloured_stream.remove_colors("this text is [color blue]blue[/color]") == "this text is blue"

    def testItShouldRemoveColourGreen(self):
        assert coloured_stream.remove_colors("this text is [color green]green[/color]") == "this text is green"

    def testItShouldRemoveColourPurple(self):
        assert coloured_stream.remove_colors("this text is [color purple]purple[/color]") == "this text is purple"

    def testItShouldRemoveColourRed(self):
        assert coloured_stream.remove_colors("this text is [color red]red[/color]") == "this text is red"

    def testItShouldRemoveColourYellow(self):
        assert coloured_stream.remove_colors("this text is [color yellow]yellow[/color]") == "this text is yellow"


def ColouredStreamTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ColouredStreamTestCase("testItShouldColourTextBlue"))
    suite.addTest(ColouredStreamTestCase("testItShouldColourTextGreen"))
    suite.addTest(ColouredStreamTestCase("testItShouldColourTextPurple"))
    suite.addTest(ColouredStreamTestCase("testItShouldColourTextRed"))
    suite.addTest(ColouredStreamTestCase("testItShouldColourTextYellow"))
    suite.addTest(ColouredStreamTestCase("testItShouldRemoveColourBlue"))
    suite.addTest(ColouredStreamTestCase("testItShouldRemoveColourGreen"))
    suite.addTest(ColouredStreamTestCase("testItShouldRemoveColourPurple"))
    suite.addTest(ColouredStreamTestCase("testItShouldRemoveColourRed"))
    suite.addTest(ColouredStreamTestCase("testItShouldRemoveColourYellow"))

    return suite
