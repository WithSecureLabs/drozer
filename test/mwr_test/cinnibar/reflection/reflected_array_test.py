import unittest

from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

from mwr_test.mocks.reflection import MockReflector

class ReflectedArrayTestCase(unittest.TestCase):

    def setUp(self):
        self.a1 = reflection.types.ReflectedArray([1, 2, 3, 4, 5])
        self.a2 = reflection.types.ReflectedArray([6, 7, 8, 9, 10])

    def testItShouldAddTwoReflectedArrays(self):
        aa = self.a1 + self.a2

        assert aa == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def testItShouldAddAReflectedAndANativeArray(self):
        aa = self.a1 + [6, 7, 8, 9, 10]

        assert aa == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def testItShouldShowAReflectedTypeIsInTheArray(self):
        assert reflection.types.ReflectedPrimitive.fromNative(3, reflector=None) in self.a1

    def testItShouldShowANativeTypeIsInTheArray(self):
        assert 3 in self.a1

    def testItShouldShowAReflectedTypeIsNotInTheArray(self):
        assert not reflection.types.ReflectedPrimitive.fromNative(7, reflector=None) in self.a1

    def testItShouldShowANativeTypeIsNotInTheArray(self):
        assert not 7 in self.a1

    def testItShouldDeleteAnItemFromTheArray(self):
        del self.a1[0]

        assert len(self.a1) == 4

    def testItShouldDeleteASliceFromTheArray(self):
        del self.a1[2:4]

        assert len(self.a1) == 3

    def testItShouldShowAReflectedArrayIsEqualToAnother(self):
        assert self.a1 == reflection.types.ReflectedArray([1, 2, 3, 4, 5])

    def testItShouldShowAReflectedArrayIsEqualToANativeOne(self):
        assert self.a1 == [1, 2, 3, 4, 5]

    def testItShouldShowAReflectedArrayIsNotEqualToAnother(self):
        assert not self.a1 == self.a2

    def testItShouldShowAReflectedArrayIsNotEqualToANativeOne(self):
        assert not self.a1 == [6, 7, 8, 9, 10]

    def testItShouldGetAnItemFromTheArray(self):
        assert self.a1[0] == 1
        assert self.a1[2] == 3
        assert self.a1[4] == 5

    def testItShouldGetASliceFromTheArray(self):
        assert self.a1[2:4] == [3, 4]

    def testItShouldIterateThroughTheArray(self):
        s1 = ""

        for i in self.a1:
            s1 += str(i)

        assert s1 == "12345"

    def testItShouldGetTheSizeOfTheArray(self):
        assert len(self.a1) == 5

    def testItShouldMultiplyTheArray(self):
        aa = self.a1 * 2

        assert len(aa) == 10
        assert len(self.a1) == 5

    def testItShouldShowAReflectedArrayIsNotEqualToAnother(self):
        assert self.a1 != self.a2

    def testItShouldShowAReflectedArrayIsNotEqualToANativeOne(self):
        assert self.a1 != [6, 7, 8, 9, 10]

    def testItShouldShowAReflectedArrayIsNotNotEqualToAnother(self):
        assert not self.a1 != reflection.types.ReflectedArray([1, 2, 3, 4, 5])

    def testItShouldShowAReflectedArrayIsNotNotEqualToANativeOne(self):
        assert not self.a1 != [1, 2, 3, 4, 5]

    def testItShouldReduceElementsOfTheArray(self):
        assert reduce(lambda x,y: x+y, self.a1) == 15

    def testItShouldSetAnItemInTheArray(self):
        self.a1[4] = 9

        assert self.a1._native == [1, 2, 3, 4, 9]

    def testItShouldSetASliceInTheArray(self):
        self.a1[2:4] = [9, 8]

        assert self.a1._native == [1, 2, 9, 8, 5]

    def testItShouldAppendToTheArray(self):
        self.a1.append(6)

        assert len(self.a1) == 6

    def testItShouldCountElementsInTheArrayWithAReflectedValue(self):
        assert self.a1.count(reflection.types.ReflectedPrimitive.fromNative(3, reflector=None)) == 1

    def testItShouldCountElementsInTheArrayWithANativeValue(self):
        assert self.a1.count(reflection.types.ReflectedPrimitive.fromNative(7, reflector=None)) == 0

    def testItShouldExtendTheArrayWithAReflectedArray(self):
        self.a1.extend(self.a2)

        assert self.a1 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def testItShouldExtendTheArrayWithANativeArray(self):
        self.a1.extend([6, 7, 8, 9, 10])

        assert self.a1 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def testItShouldGetTheIndexOfAnItemInTheArray(self):
        assert self.a1.index(3) == 2

    def testItShouldGetTheIndexOfAnItemNotInTheArray(self):
        try:
            self.a1.index(7)

            assert False, "expected ValueError"
        except ValueError:
            pass

    def testItShouldInsertIntoTheArray(self):
        self.a1.insert(2, 7)

        assert self.a1 == [1, 2, 7, 3, 4, 5]

    def testItShouldPopFromTheArrayHead(self):
        assert self.a1.pop(0) == 1
        assert self.a1 == [2, 3, 4, 5]

    def testItShouldPopFromTheArrayTail(self):
        assert self.a1.pop() == 5
        assert self.a1 == [1, 2, 3, 4]

    def testItShouldRemoveAValueFromTheArray(self):
        self.a1.remove(3)

        assert self.a1 == [1, 2, 4, 5]

    def testItShouldRemoveANonExistantValueFromTheArray(self):
        try:
            self.a1.remove(7)

            assert False, "expected ValueError"
        except ValueError:
            pass

    def testItShouldSortTheArray(self):
        aa = reflection.types.ReflectedArray([3, 4, 1, 5, 2])

        assert aa.sort() == [1, 2, 3, 4, 5]


def ReflectedArrayTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(ReflectedArrayTestCase("testItShouldAddTwoReflectedArrays"))
    suite.addTest(ReflectedArrayTestCase("testItShouldAddAReflectedAndANativeArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedTypeIsInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowANativeTypeIsInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedTypeIsNotInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowANativeTypeIsNotInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldDeleteAnItemFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldDeleteASliceFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsEqualToAnother"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsEqualToANativeOne"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotEqualToAnother"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotEqualToANativeOne"))
    suite.addTest(ReflectedArrayTestCase("testItShouldGetAnItemFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldGetASliceFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldIterateThroughTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldGetTheSizeOfTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldMultiplyTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotEqualToAnother"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotEqualToANativeOne"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotNotEqualToAnother"))
    suite.addTest(ReflectedArrayTestCase("testItShouldShowAReflectedArrayIsNotNotEqualToANativeOne"))
    suite.addTest(ReflectedArrayTestCase("testItShouldReduceElementsOfTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldSetAnItemInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldSetASliceInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldAppendToTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldCountElementsInTheArrayWithAReflectedValue"))
    suite.addTest(ReflectedArrayTestCase("testItShouldCountElementsInTheArrayWithANativeValue"))
    suite.addTest(ReflectedArrayTestCase("testItShouldExtendTheArrayWithAReflectedArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldExtendTheArrayWithANativeArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldGetTheIndexOfAnItemInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldGetTheIndexOfAnItemNotInTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldInsertIntoTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldPopFromTheArrayHead"))
    suite.addTest(ReflectedArrayTestCase("testItShouldPopFromTheArrayTail"))
    suite.addTest(ReflectedArrayTestCase("testItShouldRemoveAValueFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldRemoveANonExistantValueFromTheArray"))
    suite.addTest(ReflectedArrayTestCase("testItShouldSortTheArray"))
    
    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(ReflectedArrayTestSuite())
    