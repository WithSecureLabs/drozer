import unittest

from mwr.cinnibar.api import builders
from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.reflection.types import ReflectedType

class ReflectionResponseFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = builders.ReflectionResponseFactory

    def testItShouldBuildAnErrorMessage(self):
        message = self.factory.error("errorMessage").builder

        assert message.type == Message.REFLECTION_RESPONSE
        assert message.reflection_response.status == Message.ReflectionResponse.ERROR
        assert message.reflection_response.errormessage == "errorMessage"

    def testItShouldBuildAFatalMessage(self):
        message = self.factory.fatal("errorMessage").builder

        assert message.type == Message.REFLECTION_RESPONSE
        assert message.reflection_response.status == Message.ReflectionResponse.FATAL
        assert message.reflection_response.errormessage == "errorMessage"

    def testItShouldMakeAnError(self):
        factory = self.factory.fatal("errorMessage")
        factory.isError()
        message = factory.builder

        assert message.reflection_response.status == Message.ReflectionResponse.ERROR

    def testItShouldMakeAFatal(self):
        factory = self.factory.error("errorMessage")
        factory.isFatal()
        message = factory.builder

        assert message.reflection_response.status == Message.ReflectionResponse.FATAL

    def testItShouldMakeSuccess(self):
        factory = self.factory.error("errorMessage")
        factory.isSuccess()
        message = factory.builder

        assert message.reflection_response.status == Message.ReflectionResponse.SUCCESS

    def testItShouldSetTheErrorMessage(self):
        factory = self.factory.error("errorMessage")
        factory.setErrorMessage("otherMessage")
        message = factory.builder

        assert message.reflection_response.errormessage == "otherMessage"


def ReflectionResponseFactoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldBuildAnErrorMessage"))
    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldBuildAFatalMessage"))
    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldMakeAnError"))
    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldMakeAFatal"))
    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldMakeSuccess"))
    suite.addTest(ReflectionResponseFactoryTestCase("testItShouldSetTheErrorMessage"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectionResponseFactoryTestSuite())
    