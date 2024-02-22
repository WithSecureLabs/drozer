import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectedObjectTestCase(unittest.TestCase):

    def setUp(self):
        self.reflector = MockReflector(None)

    def testItShouldGetAPropertyValue(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildPrimitiveReply(Message.Primitive.INT, 42))

        object.getProperty
        
        assert isinstance(self.reflector.sent, Message)
        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.GET_PROPERTY
        assert self.reflector.sent.reflection_request.get_property.property == "getProperty"

    def testItShouldRaiseReflectionExceptionIfGettingNonExistentProperty(self):
        assert False, "not implemented"

    def testItShouldSetAPropertyValue(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildPrimitiveReply(Message.Primitive.INT, 42))

        object.setProperty = 42
        
        assert isinstance(self.reflector.sent, Message)
        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.SET_PROPERTY
        assert self.reflector.sent.reflection_request.set_property.property == "setProperty"

    def testItShouldRaiseReflectionExceptionIfSettingNonExistentProperty(self):
        assert False, "not implemented"

    def testItShouldInvokeAMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        object.callMe()
        
        assert isinstance(self.reflector.sent, Message)
        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.INVOKE
        assert self.reflector.sent.reflection_request.invoke.object.reference == 987654321
        assert self.reflector.sent.reflection_request.invoke.method == "callMe"

    def testItShouldInvokeAMethodWithArguments(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))
        
        object.callMe(1, "Joe")
        
        assert isinstance(self.reflector.sent, Message)
        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.INVOKE
        assert self.reflector.sent.reflection_request.invoke.object.reference == 987654321
        assert self.reflector.sent.reflection_request.invoke.method == "callMe"
        assert len(self.reflector.sent.reflection_request.invoke.argument) == 2
        assert self.reflector.sent.reflection_request.invoke.argument[0].type == Message.Argument.PRIMITIVE
        assert self.reflector.sent.reflection_request.invoke.argument[0].primitive.type == Message.Primitive.INT
        assert self.reflector.sent.reflection_request.invoke.argument[0].primitive.int == 1
        assert self.reflector.sent.reflection_request.invoke.argument[1].type == Message.Argument.STRING
        assert self.reflector.sent.reflection_request.invoke.argument[1].string == "Joe"

    def testItShouldGetAPrimitiveReturnedByAMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildPrimitiveReply(Message.Primitive.INT, 1))
        
        response = object.callMe()

        assert isinstance(response, reflection.types.ReflectedPrimitive)
        assert response.type() == "int"
        assert response.native() == 1

    def testItShouldGetAnObjectReturnedByAMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))
        
        response = object.callMe()

        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldRaiseReflectionExceptionIfInvokingNonExistentMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildErrorReply("no method callMe"))
        
        try:
            object.callMe()

            assert False, "should have raised NameError"
        except reflection.ReflectionException as e:
            assert e.message == "no method callMe"

    def testItShouldRaiseReflectionExceptionIfInvokingMethodWithInappropriateArguments(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(None)
        self.reflector.replyWith(self.reflector.buildErrorReply("no method callMe compatible with those arguments"))
        
        try:
            object.callMe()

            assert False, "should have raised NameError"
        except reflection.ReflectionException as e:
            assert e.message == "no method callMe compatible with those arguments"


def ReflectedObjectTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectedObjectTestCase("testItShouldGetAPropertyValue"))
    #suite.addTest(ReflectedObjectTestCase("testItShouldRaiseReflectionExceptionIfGettingNonExistentProperty"))
    suite.addTest(ReflectedObjectTestCase("testItShouldSetAPropertyValue"))
    #suite.addTest(ReflectedObjectTestCase("testItShouldRaiseReflectionExceptionIfSettingNonExistentProperty"))
    suite.addTest(ReflectedObjectTestCase("testItShouldInvokeAMethod"))
    suite.addTest(ReflectedObjectTestCase("testItShouldInvokeAMethodWithArguments"))
    suite.addTest(ReflectedObjectTestCase("testItShouldGetAPrimitiveReturnedByAMethod"))
    suite.addTest(ReflectedObjectTestCase("testItShouldGetAnObjectReturnedByAMethod"))
    suite.addTest(ReflectedObjectTestCase("testItShouldRaiseReflectionExceptionIfInvokingNonExistentMethod"))
    suite.addTest(ReflectedObjectTestCase("testItShouldRaiseReflectionExceptionIfInvokingMethodWithInappropriateArguments"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectedObjectTestSuite())
