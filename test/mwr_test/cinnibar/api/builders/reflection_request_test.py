import unittest

from mwr.cinnibar.api import builders
from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.reflection.types import ReflectedType

class ReflectionRequestFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = builders.ReflectionRequestFactory

    def testItShouldBuildAConstructMessage(self):
        message = self.factory.construct(987654321).builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.CONSTRUCT
        assert message.reflection_request.construct.object.reference == 987654321

    def testItShouldBuildADeleteMessage(self):
        message = self.factory.delete(987654321).builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.DELETE
        assert message.reflection_request.delete.object.reference == 987654321

    def testItShouldBuildADeleteAllMessage(self):
        message = self.factory.deleteAll().builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.DELETE_ALL

    def testItShouldBuildAGetPropertyMessage(self):
        message = self.factory.getProperty(987654321, "myProperty").builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.GET_PROPERTY
        assert message.reflection_request.get_property.object.reference == 987654321
        assert message.reflection_request.get_property.property == "myProperty"

    def testItShouldBuildAInvokeMessage(self):
        message = self.factory.invoke(987654321, "myMethod").builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.INVOKE
        assert message.reflection_request.invoke.object.reference == 987654321
        assert message.reflection_request.invoke.method == "myMethod"

    def testItShouldBuildAResolveMessage(self):
        message = self.factory.resolve("java.lang.String").builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.RESOLVE
        assert message.reflection_request.resolve.classname == "java.lang.String"

    def testItShouldBuildASetPropertyMessage(self):
        message = self.factory.setProperty(987654321, "myProperty", ReflectedType.fromNative(5, reflector=None)).builder

        assert message.type == Message.REFLECTION_REQUEST
        assert message.reflection_request.type == Message.ReflectionRequest.SET_PROPERTY
        assert message.reflection_request.set_property.object.reference == 987654321
        assert message.reflection_request.set_property.property == "myProperty"
        assert message.reflection_request.set_property.value.type == Message.Argument.PRIMITIVE
        assert message.reflection_request.set_property.value.primitive.type == Message.Primitive.INT
        assert message.reflection_request.set_property.value.primitive.int == 5

    def testItShouldSetArgumentsOfConstruct(self):
        factory = self.factory.construct(987654321)
        factory.setArguments([ReflectedType.fromNative(5, reflector=None), ReflectedType.fromNative("aString", reflector=None)])
        message = factory.builder
        
        assert message.reflection_request.construct.argument[0].type == Message.Argument.PRIMITIVE
        assert message.reflection_request.construct.argument[0].primitive.type == Message.Primitive.INT
        assert message.reflection_request.construct.argument[0].primitive.int == 5
        assert message.reflection_request.construct.argument[1].type == Message.Argument.STRING
        assert message.reflection_request.construct.argument[1].string == "aString"

    def testItShouldSetArgumentsOfInvoke(self):
        factory = self.factory.invoke(987654321, "myMethod")
        factory.setArguments([ReflectedType.fromNative(5, reflector=None), ReflectedType.fromNative("aString", reflector=None)])
        message = factory.builder
        
        assert message.reflection_request.invoke.argument[0].type == Message.Argument.PRIMITIVE
        assert message.reflection_request.invoke.argument[0].primitive.type == Message.Primitive.INT
        assert message.reflection_request.invoke.argument[0].primitive.int == 5
        assert message.reflection_request.invoke.argument[1].type == Message.Argument.STRING
        assert message.reflection_request.invoke.argument[1].string == "aString"

    def testItShouldSetId(self):
        factory = self.factory.construct(987654321)
        factory.setId(42)
        message = factory.builder

        assert message.id == 42

    def testItShouldSetSessionId(self):
        factory = self.factory.construct(987654321)
        factory.setSessionId("42")
        message = factory.builder

        assert message.reflection_request.session_id == "42"


def ReflectionRequestFactoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildAConstructMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildADeleteMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildADeleteAllMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildAGetPropertyMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildAInvokeMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildAResolveMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldBuildASetPropertyMessage"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldSetArgumentsOfConstruct"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldSetArgumentsOfInvoke"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldSetId"))
    suite.addTest(ReflectionRequestFactoryTestCase("testItShouldSetSessionId"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectionRequestFactoryTestSuite())
