import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectorTestCase(unittest.TestCase):

    def setUp(self):
        self.reflector = MockReflector(None)

    def testItShouldConstructAClass(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        response = self.reflector.construct(object)

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.CONSTRUCT
        assert self.reflector.sent.reflection_request.construct.object.reference == 987654321
        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldConstructAClassWithArguments(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        response = self.reflector.construct(object, reflection.types.ReflectedType.fromNative(1, reflector=self.reflector), reflection.types.ReflectedType.fromNative("Joe", reflector=self.reflector))

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.CONSTRUCT
        assert self.reflector.sent.reflection_request.construct.object.reference == 987654321
        assert len(self.reflector.sent.reflection_request.construct.argument) == 2
        assert self.reflector.sent.reflection_request.construct.argument[0].type == Message.Argument.PRIMITIVE
        assert self.reflector.sent.reflection_request.construct.argument[1].type == Message.Argument.STRING
        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldRaiseReflectionExceptionIfThereIsNoConstructor(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildErrorReply("no matching constructor for those parameters"))

        try:
            self.reflector.construct(object, reflection.types.ReflectedType.fromNative(1, reflector=self.reflector), reflection.types.ReflectedType.fromNative("Joe", reflector=self.reflector))

            assert False, "expected a ReflectionException"
        except reflection.ReflectionException as e:
            assert e.message == "no matching constructor for those parameters"

    def testItShouldDeleteFromTheObjectStore(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildSuccessReply())

        response = self.reflector.delete(object)

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.DELETE
        assert self.reflector.sent.reflection_request.delete.object.reference == 987654321
        assert response == True

    def testItShouldReturnFalseIfThereIsNoObjectToDelete(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildErrorReply("nothing to delete"))

        response = self.reflector.delete(object)

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.DELETE
        assert self.reflector.sent.reflection_request.delete.object.reference == 987654321
        assert response == False

    def testItShouldClearTheObjectStore(self):
        self.reflector.replyWith(self.reflector.buildSuccessReply())

        response = self.reflector.deleteAll()

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.DELETE_ALL
        assert response == True

    def testItShouldClearTheObjectStore(self):
        self.reflector.replyWith(self.reflector.buildSuccessReply())

        response = self.reflector.deleteAll()

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.DELETE_ALL
        assert response == True

    def testItShouldGetAnObjectProperty(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildPrimitiveReply(Message.Primitive.INT, 1))

        response = self.reflector.getProperty(object, "id")

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.GET_PROPERTY
        assert self.reflector.sent.reflection_request.get_property.object.reference == 987654321
        assert self.reflector.sent.reflection_request.get_property.property == "id"
        assert isinstance(response, reflection.types.ReflectedPrimitive)
        assert response.type() == 'int'
        assert response.native() == 1

    def testItShouldRaiseReflectionExceptionIfThereIsNoPropertyToGet(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildErrorReply("no property"))

        try:
            self.reflector.getProperty(object, "id")

            assert False, "expected a ReflectionException"
        except reflection.ReflectionException as e:
            assert e.message == "no property"

    def testItShouldInvokeAMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        response = self.reflector.invoke(object, "callMe")

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.INVOKE
        assert self.reflector.sent.reflection_request.invoke.object.reference == 987654321
        assert self.reflector.sent.reflection_request.invoke.method == "callMe"
        assert len(self.reflector.sent.reflection_request.invoke.argument) == 0
        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldInvokeAMethodWithArguments(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        response = self.reflector.invoke(object, "callMe", reflection.types.ReflectedType.fromNative(1, reflector=self.reflector), reflection.types.ReflectedType.fromNative("Joe", reflector=self.reflector))

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.INVOKE
        assert self.reflector.sent.reflection_request.invoke.object.reference == 987654321
        assert self.reflector.sent.reflection_request.invoke.method == "callMe"
        assert len(self.reflector.sent.reflection_request.invoke.argument) == 2
        assert self.reflector.sent.reflection_request.invoke.argument[0].type == Message.Argument.PRIMITIVE
        assert self.reflector.sent.reflection_request.invoke.argument[1].type == Message.Argument.STRING
        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldRaiseReflectionExceptionIfThereIsNoMatchingMethod(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildErrorReply("no matching method for those parameters"))

        try:
            self.reflector.construct(object, reflection.types.ReflectedType.fromNative(1, reflector=self.reflector), reflection.types.ReflectedType.fromNative("Joe", reflector=self.reflector))

            assert False, "expected a ReflectionException"
        except reflection.ReflectionException as e:
            assert e.message == "no matching method for those parameters"

    def testItShouldResolveAClass(self):
        self.reflector.replyWith(self.reflector.buildObjectReply(55512345))

        response = self.reflector.resolve("java.lang.String")

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.RESOLVE
        assert self.reflector.sent.reflection_request.resolve.classname == "java.lang.String"
        assert isinstance(response, reflection.types.ReflectedObject)
        assert response._ref == 55512345

    def testItShouldRaiseReflectionExceptionIfThereIsNoMatchingClass(self):
        self.reflector.replyWith(self.reflector.buildErrorReply("could not resolve"))

        try:
            response = self.reflector.resolve("java.lang.String")

            assert False, "expected a ReflectionException"
        except reflection.ReflectionException as e:
            assert e.message == "could not resolve"

    def testItShouldSetAnObjectProperty(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildPrimitiveReply(Message.Primitive.INT, 1))

        response = self.reflector.setProperty(object, "id", reflection.types.ReflectedType.fromNative(1, reflector=self.reflector))

        assert self.reflector.sent.type == Message.REFLECTION_REQUEST
        assert self.reflector.sent.reflection_request.type == Message.ReflectionRequest.SET_PROPERTY
        assert self.reflector.sent.reflection_request.set_property.object.reference == 987654321
        assert self.reflector.sent.reflection_request.set_property.property == "id"
        assert self.reflector.sent.reflection_request.set_property.value.primitive.type == Message.Primitive.INT
        assert self.reflector.sent.reflection_request.set_property.value.primitive.int == 1
        assert response.reflection_response.status == Message.ReflectionResponse.SUCCESS

    def testItShouldRaiseReflectionExceptionIfThereIsNoPropertyToSet(self):
        object = reflection.types.ReflectedObject(987654321, reflector=self.reflector)

        self.reflector.replyWith(self.reflector.buildErrorReply("could not set property"))

        try:
            self.reflector.setProperty(object, "id", reflection.types.ReflectedType.fromNative(1, reflector=self.reflector))

            assert False, "expected a ReflectionException"
        except reflection.ReflectionException as e:
            assert e.message == "could not set property"


def ReflectorTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectorTestCase("testItShouldConstructAClass"))
    suite.addTest(ReflectorTestCase("testItShouldConstructAClassWithArguments"))
    suite.addTest(ReflectorTestCase("testItShouldRaiseReflectionExceptionIfThereIsNoConstructor"))
    suite.addTest(ReflectorTestCase("testItShouldDeleteFromTheObjectStore"))
    suite.addTest(ReflectorTestCase("testItShouldReturnFalseIfThereIsNoObjectToDelete"))
    suite.addTest(ReflectorTestCase("testItShouldClearTheObjectStore"))
    suite.addTest(ReflectorTestCase("testItShouldGetAnObjectProperty"))
    suite.addTest(ReflectorTestCase("testItShouldRaiseReflectionExceptionIfThereIsNoPropertyToGet"))
    suite.addTest(ReflectorTestCase("testItShouldInvokeAMethod"))
    suite.addTest(ReflectorTestCase("testItShouldInvokeAMethodWithArguments"))
    suite.addTest(ReflectorTestCase("testItShouldRaiseReflectionExceptionIfThereIsNoMatchingMethod"))
    suite.addTest(ReflectorTestCase("testItShouldResolveAClass"))
    suite.addTest(ReflectorTestCase("testItShouldRaiseReflectionExceptionIfThereIsNoMatchingClass"))
    suite.addTest(ReflectorTestCase("testItShouldSetAnObjectProperty"))
    suite.addTest(ReflectorTestCase("testItShouldRaiseReflectionExceptionIfThereIsNoPropertyToSet"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectorTestSuite())
