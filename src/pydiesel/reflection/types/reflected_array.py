from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_type import ReflectedType

class ReflectedArray(ReflectedType):
    """
    A ReflectedType that represents an Array, either of primitives or objects.
    """
    
    def __init__(self, objects, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)

        self._native = list(self.__validateAndConvert(objects))

    @classmethod
    def fromArgument(cls, argument, reflector):
        """
        Builds a new ReflectedArray, given an Argument as defined in the drozer
        protocol that contains an Array.
        """

        array = []

        for element in argument.array.element:
            array.append(ReflectedType.fromArgument(element, reflector))

        return ReflectedArray(array, reflector=reflector)

    def append(self, obj):
        self._native.append(ReflectedType.fromNative(obj, self._reflector))

        return self

    def count(self, obj):
        return self._native.count(obj)

    def extend(self, objects):
        if isinstance(objects, ReflectedArray):
            objects = objects._native

        self._native.extend(self.__validateAndConvert(objects))

        return self

    def index(self, i):
        return self._native.index(i)

    def insert(self, i, obj):
        self._native.insert(i, ReflectedType.fromNative(obj, self._reflector))

    def native(self):
        """
        Get the native representation of the drozer.
        """

        return self._native

    def pop(self, i=-1):
        return self._native.pop(i)

    def remove(self, obj):
        self._native.remove(obj)

    def sort(self):
        self._native.sort()

        return self

    def _pb(self):
        """
        Get an Argument representation of the Array, as defined in the drozer
        protocol.
        """

        argument = Message.Argument(type=Message.Argument.ARRAY)

        if self._native[0]._pb().type == Message.Argument.ARRAY:
            argument.array.type = Message.Array.ARRAY
        elif self._native[0]._pb().type == Message.Argument.NULL:
            argument.array.type = Message.Array.OBJECT
        elif self._native[0]._pb().type == Message.Argument.OBJECT:
            argument.array.type = Message.Array.OBJECT
        elif self._native[0]._pb().type == Message.Argument.STRING:
            argument.array.type = Message.Array.STRING
        elif self._native[0]._pb().type == Message.Argument.PRIMITIVE:
            argument.array.type = Message.Array.PRIMITIVE

        for e in self._native:
            element = argument.array.element.add()
            element.MergeFrom(ReflectedType.fromNative(e, reflector=self._reflector)._pb())

        return argument

    def __validateAndConvert(self, objects):
        """
        A utility method to help build a ReflectedArray from a collection of
        other objects.

        This enforces some validation, such as checking that all objects in an
        array are of consistent type.
        """

        if not hasattr(objects, '__iter__'):
            raise TypeError("objects is not iterable")

        list_type = None

        for obj in objects:
            if not list_type:
                list_type = type(obj)
            else:
                if type(obj) != list_type:
                    raise TypeError("mismatched array element types")

            yield ReflectedType.fromNative(obj, self._reflector)

    def __add__(self, other):
        return ReflectedArray(self._native).extend(other)

    def __delitem__(self, i):
        del self._native[i]

    def __delslice__(self, i, j):
        del self._native[i:j]

    def __eq__(self, other):
        if isinstance(other, ReflectedArray):
            return self._native == other._native
        else:
            return self._native == other

    def __getitem__(self, index):
        return self._native[index]

    def __getslice__(self, i, j):
        return self._native[i:j]

    def __iter__(self):
        return self._native.__iter__()

    def __len__(self):
        return self._native.__len__()

    def __ne__(self, other):
        if isinstance(other, ReflectedArray):
            return self._native != other._native
        else:
            return self._native != other

    def __mul__(self, other):
        if isinstance(other, ReflectedType):
            return self._native * other._native
        else:
            return self._native * other

    def __setitem__(self, index, obj):
        self._native[index] = ReflectedType.fromNative(obj, self._reflector)

    def __setslice__(self, i, j, seq):
        self._native[i:j] = seq

    def __str__(self):
        return "[{}]".format(", ".join(map(lambda e: str(e), self._native)))
        