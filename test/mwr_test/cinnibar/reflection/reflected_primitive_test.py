import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectedIntegerPrimitiveTestCase(unittest.TestCase):

    def setUp(self):
        self.np0 = 0
        self.np1 = 1
        self.np2 = 2
        self.np3 = 3

        self.rp0 = reflection.types.ReflectedPrimitive('int', 0)
        self.rp1 = reflection.types.ReflectedPrimitive('int', 1)
        self.rp2 = reflection.types.ReflectedPrimitive('int', 2)
        self.rp3 = reflection.types.ReflectedPrimitive('int', 3)
        pass

    #'__abs__', '__add__',  '__delattr__', 

    def testItShouldAddTwoReflectedPrimitives(self):
        assert self.rp1 + self.rp2 == 3

    def testItShouldAddAReflectedAndANativePrimitive(self):
        assert self.rp1 + self.np2 == 3

    #'__class__', '__coerce__'

    def testItShouldDivideAReflectedPrimitiveByAnother(self):
        assert self.rp3 / self.rp2 == 1     # Integer division

    def testItShouldDeviceAReflectedPrimitiveByANative(self):
        assert self.rp3 / self.np2 == 1     # Integer division

    def testItShouldGetTheIntegerAndModulusOfAReflectedPrimitiveByAnother(self):
        assert divmod(self.rp3, self.rp2) == (1, 1)

    def testItShouldGetTheIntegerAndModulusOfAReflectedPrimitiveByANative(self):
        assert divmod(self.rp3, self.np2) == (1, 1)

    def testItShouldShowTwoReflectedPrimitiveAreEqual(self):
        assert self.rp2 == reflection.types.ReflectedPrimitive('int', 2)

    def testItShouldShowTwoReflectedPrimitivesAreNotEqual(self):
        assert not self.rp2 == self.rp1

    def testItShouldShowAReflectedPrimitiveEqualsANative(self):
        assert self.rp2 == self.np2

    def testItShouldNotShowAReflectedPrimitiveEqualsANative(self):
        assert not self.rp2 == self.np1

    def testItShouldForceAReflectedPrimitiveToAFloat(self):
        assert type(float(self.rp2)) == type(3.14)

    def testItShouldIntegerDivideAReflectedPrimitiveByAnother(self):
        assert self.rp3 / self.rp2 == 1     # Integer division

    def testItShouldIntegerDivideAReflectedPrimitiveByANative(self):
        assert self.rp3 / self.np2 == 1     # Integer division

    def testItShouldShowAReflectedPrimitiveIsGreaterThanOrEqualToAnother(self):
        assert self.rp3 >= self.rp2
        assert self.rp2 >= self.rp2

    def testItShouldNotShowAReflectedPrimitiveIsGreaterThanOrEqualToAnother(self):
        assert not self.rp1 >= self.rp2

    def testItShouldShowAReflectedPrimitiveIsGreaterThanOrEqualToANative(self):
        assert self.rp3 >= self.np2
        assert self.rp2 >= self.np2

    def testItShouldNotShowAReflectedPrimitiveIsGreaterThanOrEqualToANative(self):
        assert not self.rp1 >= self.np2

    def testItShouldShowAReflectedPrimitiveIsGreaterThanAnother(self):
        assert self.rp3 > self.rp2

    def testItShouldShowAReflectedPrimitiveIsNotGreaterThanAnother(self):
        assert not self.rp2 > self.rp2
        assert not self.rp1 > self.rp2

    def testItShouldShowAReflectedPrimitiveIsGreaterThanANative(self):
        assert self.rp3 > self.np2

    def testItShouldNotShowAReflectedPrimitiveIsGreaterThanANative(self):
        assert not self.rp2 > self.np2
        assert not self.rp1 > self.np2

    def testItShouldForceAReflectedPrimitiveToAnInteger(self):
        assert type(int(self.rp2)) == type(2)

    def testItShouldShowAReflectedPrimitiveIsLessThanOrEqualToAnother(self):
        assert self.rp1 <= self.rp2
        assert self.rp2 <= self.rp2

    def testItShouldNotShowAReflectedPrimitiveIsLessThanOrEqualToAnother(self):
        assert not self.rp3 <= self.rp2

    def testItShouldShowAReflectedPrimitiveIsLessThanOrEqualToANative(self):
        assert self.rp1 <= self.np2
        assert self.rp2 <= self.np2

    def testItShouldNotShowAReflectedPrimitiveIsLessThanOrEqualToANative(self):
        assert not self.rp3 <= self.np2

    def testItShouldForceAReflectedPrimitiveToALong(self):
        assert type(long(self.rp2)) == type(long(42))

    def testItShouldShowAReflectedPrimitiveIsLessThanAnother(self):
        assert self.rp1 < self.rp2

    def testItShouldShowAReflectedPrimitiveIsNotLessThanAnother(self):
        assert not self.rp2 < self.rp2
        assert not self.rp3 < self.rp2

    def testItShouldShowAReflectedPrimitiveIsLessThanANative(self):
        assert self.rp1 < self.np2

    def testItShouldNotShowAReflectedPrimitiveIsLessThanANative(self):
        assert not self.rp2 < self.np2
        assert not self.rp3 < self.np2

    def testItShouldGetTheModulusOfAReflectedPrimitiveByAnother(self):
        assert self.rp3 % self.rp2 == 1

    def testItShouldGetTheModulusOfAReflectedPrimitiveByANative(self):
        assert self.rp3 % self.np2 == 1

    def testItShouldMultipleAReflectedPrimitiveByAnother(self):
        assert self.rp2 * self.rp3 == 6

    def testItShouldMultiplyAReflectedPrimitiveByANative(self):
        assert self.rp2 * self.np3 == 6

    def testItShouldShowAReflectedPrimitiveIsNotEqualToAnother(self):
        assert self.rp2 != self.rp3

    def testItShouldNotShowAReflectedPrimitiveIsNotEqualToAnother(self):
        assert not self.rp2 != self.rp2

    def testItShouldShowAReflectedPrimitiveIsNotEqualToANative(self):
        assert self.rp2 != self.np3

    def testItShouldNotShowAReflectedPrimitiveIsNotEqualToANative(self):
        assert not self.rp2 != self.np2

    def testItShouldNegateAReflectedPrimitive(self):
        assert -self.rp2 == -2

    def testItShouldShowAReflectedPrimitiveIsNonZero(self):
        assert self.rp2.__nonzero__()

    def testItShouldNotShowAReflectedPrimitiveIsNonZero(self):
        assert not self.rp0.__nonzero__()

    def testItShouldSupportUnaryPositive(self):
        assert +self.rp2 == 2

    def testItShouldRaiseAReflectedPrimitiveToAReflectedPower(self):
        assert pow(self.rp2, self.rp3) == 8

    def testItShouldRaiseAReflectedPrimitiveToANativePower(self):
        assert pow(self.rp2, self.np3) == 8

    def testItShouldRaiseAReflectedPrimitiveToAPowerWithAReflectedModulus(self):
        assert pow(self.rp2, self.rp3, self.rp3) == 2

    def testItShouldRaiseAReflectedPrimitiveToAPowerWithANativeModulus(self):
        assert pow(self.rp2, self.rp3, self.np3) == 2

    def testItShouldAddAReflectedPrimitiveToANative(self):
        assert self.np2 + self.rp2 == 4

    def testItShouldDivideANativeByAReflectedPrimitive(self):
        assert self.np3 / self.rp2 == 1

    def testItShouldIntegerAndModulusOfDividingANativeByAReflectedPrimitive(self):
        assert divmod(self.np3, self.rp2) == (1, 1)

    def testItShouldIntegerDivideANativeByAReflectedPrimitive(self):
        assert self.np3 / self.rp2 == 1

    def testItShouldGetTheModulusOfDividingANativeByAReflectedPrimitive(self):
        assert self.np3 % self.rp2 == 1

    def testItShouldMultiplyANativeByAReflectedPrimitive(self):
        assert self.np3 * self.rp2 == 6

    def testItShouldRaiseANativeToAReflectedPrimitivePower(self):
        assert pow(self.np2, self.rp3) == 8

    # Weirdly, Python doesn't support the modulus when using __rpow__. I'd call
    # this a language bug... but I suspect the Python people would claim it's a
    # feature.
    #
    #def testItShouldRaiseANativeToAReflectedPrimitivePowerWithAReflectedModulus(self):
    #    assert pow(self.np2, self.rp3, self.rp3) == 2
    #
    #def testItShouldRaiseANativeToAReflectedPrimitivePowerWithANativeModulus(self):
    #    assert pow(self.np2, self.rp3, self.np3) == 2

    def testItShouldSubtractAReflectedPrimitiveFromANative(self):
        assert self.np3 - self.rp2 == 1

    def testItShouldGetAStringRepresentation(self):
        assert str(self.rp3) == "3"

    def testItShouldSubtractAReflectedPrimitiveFromAnother(self):
        assert self.rp3 - self.rp2 == 1

    def testItShouldSubtractANativeFromAReflectedPrimitive(self):
        assert self.rp3 - self.np2 == 1

def ReflectedPrimitiveTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldAddTwoReflectedPrimitives"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldAddAReflectedAndANativePrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldDivideAReflectedPrimitiveByAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldDeviceAReflectedPrimitiveByANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetTheIntegerAndModulusOfAReflectedPrimitiveByAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetTheIntegerAndModulusOfAReflectedPrimitiveByANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowTwoReflectedPrimitiveAreEqual"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowTwoReflectedPrimitivesAreNotEqual"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveEqualsANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveEqualsANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldForceAReflectedPrimitiveToAFloat"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldIntegerDivideAReflectedPrimitiveByAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldIntegerDivideAReflectedPrimitiveByANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsGreaterThanOrEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsGreaterThanOrEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsGreaterThanOrEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsGreaterThanOrEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsGreaterThanAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsNotGreaterThanAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsGreaterThanANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsGreaterThanANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldForceAReflectedPrimitiveToAnInteger"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsLessThanOrEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsLessThanOrEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsLessThanOrEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsLessThanOrEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldForceAReflectedPrimitiveToALong"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsLessThanAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsNotLessThanAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsLessThanANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsLessThanANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetTheModulusOfAReflectedPrimitiveByAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetTheModulusOfAReflectedPrimitiveByANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldMultipleAReflectedPrimitiveByAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldMultiplyAReflectedPrimitiveByANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsNotEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsNotEqualToAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsNotEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsNotEqualToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNegateAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldShowAReflectedPrimitiveIsNonZero"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldNotShowAReflectedPrimitiveIsNonZero"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldSupportUnaryPositive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseAReflectedPrimitiveToAReflectedPower"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseAReflectedPrimitiveToANativePower"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseAReflectedPrimitiveToAPowerWithAReflectedModulus"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseAReflectedPrimitiveToAPowerWithANativeModulus"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldAddAReflectedPrimitiveToANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldDivideANativeByAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldIntegerAndModulusOfDividingANativeByAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldIntegerDivideANativeByAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetTheModulusOfDividingANativeByAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldMultiplyANativeByAReflectedPrimitive"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseANativeToAReflectedPrimitivePower"))
    #suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseANativeToAReflectedPrimitivePowerWithAReflectedModulus"))
    #suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldRaiseANativeToAReflectedPrimitivePowerWithANativeModulus"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldSubtractAReflectedPrimitiveFromANative"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldGetAStringRepresentation"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldSubtractAReflectedPrimitiveFromAnother"))
    suite.addTest(ReflectedIntegerPrimitiveTestCase("testItShouldSubtractANativeFromAReflectedPrimitive"))
    
    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectedPrimitiveTestSuite())
    