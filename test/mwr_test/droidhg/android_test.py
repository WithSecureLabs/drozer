import functools
import unittest

from mwr.cinnibar.reflection.types import ReflectedObject

from mwr.droidhg.android import Intent

class IntentTestCase(unittest.TestCase):

    class MockModule:
        
        def __init__(self, reflector):
            self.__reflector = reflector

        def new(self, class_name):
            return self.__reflector.construct(class_name)
        
        def arg(self, native, obj_type=None):
            return native

    class MockReflector:

        def __init__(self):
            self.construct_returns = None
            self.constructed = None
            self.deleted_all = False
            self.get_property_returns = None
            self.gotten_property = None
            self.invoked = []
            self.resolve_returns = None
            self.resolved = None

        def construct(self, klass):
            self.constructed = klass

            return self.construct_returns

        def deleteAll(self):
            self.deleted_all = True
        
        def getProperty(self, ref, property_name):
            self.gotten_property = (ref, property_name)

            if self.get_property_returns == None:
                return functools.partial(self._invoker, property_name)
            else:
                return self.get_property_returns

        def invoke(self, ref, method_name, *args):
            self.invoked.append((ref, method_name, args))

        def resolve(self, class_name):
            self.resolved = class_name

            return self.resolve_returns

        def _invoker(self, method_name, *args, **kwargs):
            return self.invoke(self, method_name, *args, **kwargs)

    def setUp(self):
        pass

    # fromParser
    #    - action
    #    - category
    #    - component
    #    - data_uri
    #    - extras
    #    - flags
    #    - mimetype

    def testItShouldBuildTheAction(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(action="com.android.intent.VIEW")

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setAction"
        assert reflector.invoked[-1][2][0] == "com.android.intent.VIEW"

    # buildIn
    #    - category
    #    - component
    #    - data_uri

    def testItShouldAddBooleanExtras(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(extras=[('boolean', 'myBool', "True")])

        intent.buildIn(module)
        
        assert reflector.invoked[0][1] == "putBoolean"
        assert reflector.invoked[0][2][0] == 'myBool'
        assert reflector.invoked[0][2][1] == True
        assert reflector.invoked[1][1] == "putExtras"

    def testItShouldAddFloatExtras(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(extras=[("float", "myFloat", 3.14)])

        intent.buildIn(module)
        
        assert reflector.invoked[0][1] == "putFloat"
        assert reflector.invoked[0][2][0] == "myFloat"
        assert reflector.invoked[0][2][1] == 3.14
        assert reflector.invoked[1][1] == "putExtras"

    def testItShouldAddIntegerExtras(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(extras=[("integer", "myInt", 42)])

        intent.buildIn(module)
        
        assert reflector.invoked[0][1] == "putInt"
        assert reflector.invoked[0][2][0] == "myInt"
        assert reflector.invoked[0][2][1] == 42
        assert reflector.invoked[1][1] == "putExtras"

    def testItShouldAddStringExtras(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(extras=[("string", "myString", "Hello, World!")])

        intent.buildIn(module)

        assert reflector.invoked[0][1] == "putString"
        assert reflector.invoked[0][2][0] == "myString"
        assert reflector.invoked[0][2][1] == "Hello, World!"
        assert reflector.invoked[1][1] == "putExtras"

    def testItShouldBuildTheFlagsFromBinary(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(flags=["0x10000000"])

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setFlags"
        assert reflector.invoked[-1][2][0] == 0x10000000

    def testItShouldBuildTheFlagsFromSymbol(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(flags=["ACTIVITY_NEW_TASK"])

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setFlags"
        assert reflector.invoked[-1][2][0] == 0x10000000

    def testItShouldBuildTheFlagsFromBinaries(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(flags=["0x10000000", "0x00010000"])

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setFlags"
        assert reflector.invoked[-1][2][0] == 0x10010000

    def testItShouldBuildTheFlagsFromSymbols(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(flags=["ACTIVITY_NEW_TASK", "ACTIVITY_NO_ANIMATION"])

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setFlags"
        assert reflector.invoked[-1][2][0] == 0x10010000

    def testItShouldBuildTheFlagsFromBinaryAndSymbols(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(flags=["ACTIVITY_NEW_TASK", "0x00010000"])

        intent.buildIn(module)
        
        assert reflector.invoked[-1][1] == "setFlags"
        assert reflector.invoked[-1][2][0] == 0x10010000
    
    #    - mimetype

    def testItShouldBeValidIfTheActionIsSet(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(action="android.intent.action.VIEW")
        
        assert intent.isValid()

    def testItShouldBeValidIfTheComponentIsSet(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent(component="com.android.browser com.android.browser.BrowserActivity")
        
        assert intent.isValid()

    def testItShouldNotBeValidIfNoActionOrComponentIsSet(self):
        reflector = IntentTestCase.MockReflector()
        reflector.construct_returns = ReflectedObject(999, reflector=reflector)
        module = IntentTestCase.MockModule(reflector)

        intent = Intent()
        
        assert not intent.isValid()
    

def IntentTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(IntentTestCase("testItShouldBuildTheAction"))
    suite.addTest(IntentTestCase("testItShouldAddBooleanExtras"))
    suite.addTest(IntentTestCase("testItShouldAddFloatExtras"))
    suite.addTest(IntentTestCase("testItShouldAddIntegerExtras"))
    suite.addTest(IntentTestCase("testItShouldAddStringExtras"))
    suite.addTest(IntentTestCase("testItShouldBuildTheFlagsFromBinary"))
    suite.addTest(IntentTestCase("testItShouldBuildTheFlagsFromSymbol"))
    suite.addTest(IntentTestCase("testItShouldBuildTheFlagsFromBinaries"))
    suite.addTest(IntentTestCase("testItShouldBuildTheFlagsFromSymbols"))
    suite.addTest(IntentTestCase("testItShouldBuildTheFlagsFromBinaryAndSymbols"))
    suite.addTest(IntentTestCase("testItShouldBeValidIfTheActionIsSet"))
    suite.addTest(IntentTestCase("testItShouldBeValidIfTheComponentIsSet"))
    suite.addTest(IntentTestCase("testItShouldNotBeValidIfNoActionOrComponentIsSet"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(IntentTestSuite())
