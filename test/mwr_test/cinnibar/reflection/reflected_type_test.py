import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectedTypeTestCase(unittest.TestCase):

    def setUp(self):
        self.reflector = reflection.Reflector(None)

    def testItShouldBuildPrimitiveFromArgument(self):
        argument = Message.Argument(type=Message.Argument.PRIMITIVE)
        argument.primitive.type = Message.Primitive.BOOL
        argument.primitive.bool = True

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedPrimitive)
        assert type.type() == "boolean"
        assert type.native() == True

    def testItShouldBuildStringFromArgument(self):
        argument = Message.Argument(type=Message.Argument.STRING)
        argument.string = "Hello, World!"

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedString)
        assert type.native() == "Hello, World!"

    def testItShouldBuildPrimitiveArrayFromArgument(self):
        argument = Message.Argument(type=Message.Argument.ARRAY)
        argument.array.type = Message.Array.PRIMITIVE

        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.PRIMITIVE)
            element.primitive.type = Message.Primitive.BOOL
            element.primitive.bool = True

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        assert len(type.native()) == 3

        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedPrimitive)
            assert type.native()[i].type() == "boolean"

    def testItShouldBuildStringArrayFromArgument(self):
        argument = Message.Argument(type=Message.Argument.ARRAY)
        argument.array.type = Message.Array.STRING

        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.STRING)
            element.string = "Hello, World! (" + str(i) + ")"

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        assert len(type.native()) == 3

        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedString)
            assert type.native()[i].native() == "Hello, World! (" + str(i) + ")"

    def testItShouldBuildNestedArrayFromArgument(self):
        argument = Message.Argument(type=Message.Argument.ARRAY)
        argument.array.type = Message.Array.ARRAY

        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.ARRAY)

            for j in range(0,i):
                subelement = element.array.element.add(type=Message.Argument.PRIMITIVE)
                subelement.primitive.type = Message.Primitive.BOOL
                subelement.primitive.bool = True

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        assert len(type.native()) == 3

        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedArray)
            assert len(type.native()[i].native()) == i

    def testItShouldBuildObjectArrayFromArgument(self):
        argument = Message.Argument(type=Message.Argument.ARRAY)
        argument.array.type = Message.Array.OBJECT
        
        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.OBJECT)
            element.object.reference = i

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        assert len(type.native()) == 3

        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedObject)
            assert type.native()[i]._ref == i

    def testItShouldRaiseTypeErrorIfArrayIsMixedTypes(self):
        argument = Message.Argument(type=Message.Argument.ARRAY)
        argument.array.type = Message.Array.PRIMITIVE

        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.PRIMITIVE)
            element.primitive.type = Message.Primitive.BOOL
            element.primitive.bool = True
        for i in range(0,3):
            element = argument.array.element.add(type=Message.Argument.OBJECT)
            element.object.reference = i

        try:
            type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

            assert False, "should have caused a TypeError building a mixed array"
        except TypeError as e:
            assert e.message == "mismatched array element types"

    def testItShouldBuildObjectFromArgument(self):
        argument = Message.Argument(type=Message.Argument.OBJECT)
        argument.object.reference = 987654321

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedObject)
        assert type._ref == 987654321

    def testItShouldBuildNullFromArgument(self):
        argument = Message.Argument(type=Message.Argument.NULL)

        type = reflection.types.ReflectedType.fromArgument(argument, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedNull)

    def testItShouldBuildBooleanFromNative(self):
        type = reflection.types.ReflectedType.fromNative(True, reflector=self.reflector, obj_type="boolean")
        
        # we must use type-hinting for booleans, otherwise Python gets a little
        # bit confused, because it doesn't support them properly

        assert isinstance(type, reflection.types.ReflectedPrimitive)
        assert type.type() == "boolean"
        assert type.native() == True

    def testItShouldBuildFloatFromNative(self):
        type = reflection.types.ReflectedType.fromNative(1.5, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedPrimitive)
        assert type.type() == "float"
        assert type.native() == 1.5

    def testItShouldBuildIntFromNative(self):
        type = reflection.types.ReflectedType.fromNative(1, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedPrimitive)
        assert type.type() == "int"
        assert type.native() == 1

    def testItShouldBuildLongFromNative(self):
        type = reflection.types.ReflectedType.fromNative(long(1), reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedPrimitive)
        assert type.type() == "long"
        assert type.native() == long(1)
    
    def testItShouldBuildNullFromNative(self):
        type = reflection.types.ReflectedType.fromNative(None, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedNull)

    def testItShouldBuildPrimitiveArrayFromNative(self):
        type = reflection.types.ReflectedType.fromNative([1, 2, 3], reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedPrimitive)
            assert type.native()[i].type() == "int"
            assert type.native()[i].native() == i+1

    def testItShouldBuildStringArrayFromNative(self):
        trial = ["Hello", "There", "World"]
        type = reflection.types.ReflectedType.fromNative(trial, reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedString)
            assert type.native()[i].native() == trial[i]

    def testItShouldBuildNestedArrayFromNative(self):
        type = reflection.types.ReflectedType.fromNative([[], [1], [1,2]], reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedArray)
        for i in range(0,3):
            assert isinstance(type.native()[i], reflection.types.ReflectedArray)
            assert len(type.native()[i].native()) == i

    def testItShouldBuildStringFromNative(self):
        type = reflection.types.ReflectedType.fromNative("Hello, World!", reflector=self.reflector)

        assert isinstance(type, reflection.types.ReflectedString)
        assert type.native() == "Hello, World!"
        

def ReflectedTypeTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectedTypeTestCase("testItShouldBuildPrimitiveFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildStringFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildPrimitiveArrayFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildStringArrayFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildNestedArrayFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildObjectArrayFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldRaiseTypeErrorIfArrayIsMixedTypes"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildObjectFromArgument"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildNullFromArgument"))

    suite.addTest(ReflectedTypeTestCase("testItShouldBuildBooleanFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildFloatFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildIntFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildLongFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildNullFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildPrimitiveArrayFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildStringArrayFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildNestedArrayFromNative"))
    suite.addTest(ReflectedTypeTestCase("testItShouldBuildStringFromNative"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectionTypesTestSuite())
