import base64
from functools import partial

from mwr.droidhg.api.protobuf_pb2 import Message
from mwr.droidhg.reflection.exceptions import ReflectionException

class ReflectedType(object):
    """
    A ReflectedType models a variable shared with a Java VM through reflection.

    The ReflectedType class is used to keep track of meta-data that would
    otherwise be lost in Python, such as the strong type required by Java.

    A ReflectedType is never instantiated directly, rather #fromArgument and
    #fromNative should be used to cast types provided in API messages or from
    the local system respectively. These methods will return a subclass of
    ReflectedType, which provides suitable methods to allow it to be used as
    a native object.
    """

    def __init__(self, reflector=None):
        self._reflector = reflector

    @classmethod
    def fromArgument(cls, argument, reflector):
        """
        Creates a new ReflectedType, given an Argument message as defined in
        the Mercury protocol.
        """

        if isinstance(argument, ReflectedType):
            return argument
        elif argument.type == Message.Argument.ARRAY:
            return ReflectedArray.fromArgument(argument, reflector=reflector)
        elif argument.type == Message.Argument.OBJECT:
            return ReflectedObject(argument.object.reference, reflector=reflector)
        elif argument.type == Message.Argument.DATA:
            return ReflectedBinary(argument.data, reflector=reflector)
        elif argument.type == Message.Argument.NULL:
            return ReflectedNull(reflector=reflector)
        elif argument.type == Message.Argument.PRIMITIVE:
            return ReflectedPrimitive.fromArgument(argument, reflector)
        elif argument.type == Message.Argument.STRING:
            return ReflectedString(argument.string, reflector=reflector)
        else:
            return None

    @classmethod
    def fromNative(cls, obj, reflector, obj_type=None):
        """
        Creates a new ReflectedType, given a native variable. An optional type
        can be specified to indicate which Java data type should be used, where
        it cannot be inferred from the Python type.
        """

        if obj_type == None and isinstance(obj, ReflectedType) or obj_type == "object":
            return obj
        elif obj_type == None and isinstance(obj, long) or obj_type == "long":
            return ReflectedPrimitive("long", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, int) or obj_type == "int":
            return ReflectedPrimitive("int", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, float) or obj_type == "float":
            return ReflectedPrimitive("float", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, bool) or obj_type == "boolean":
            return ReflectedPrimitive("boolean", obj, reflector=reflector)
        elif obj_type == None and (isinstance(obj, str) or isinstance(obj, unicode)) or obj_type == "string":
            return ReflectedString(obj, reflector=reflector)
        elif obj_type == "double":
            return ReflectedPrimitive("double", obj, reflector=reflector)
        elif obj is None:
            return ReflectedNull(reflector=reflector)
        elif hasattr(obj, '__iter__'):
            return ReflectedArray(obj, reflector=reflector)
        else:
            return None

    def _gettype(self, obj):
        """
        Returns a string, indicating the type of a ReflectedType.
        """

        if isinstance(obj, ReflectedPrimitive):
            return obj.primitive_type
        elif isinstance(obj, ReflectedArray):
            return 'array'
        elif isinstance(obj, ReflectedString):
            return 'string'
        elif isinstance(obj, ReflectedObject):
            return 'object'
        elif obj == None:
            return 'null'
        else:
            return 'unknown'


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
        Builds a new ReflectedArray, given an Argument as defined in the Mercury
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
        Get the native representation of the Array.
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
        Get an Argument representation of the Array, as defined in the Mercury
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

class ReflectedNull(ReflectedType):
    """
    A ReflectedType that represents Java null.
    """
    
    def _pb(self):
        """
        Get an Argument representation of the null, as defined in the Mercury
        protocol.
        """
        return Message.Argument(type=Message.Argument.NULL)

    def __eq__(self, other):
        if(other == None):
            return True
        else:
            return ReflectedType.__eq__(self, other)

    def __ne__(self, other):
        if(other == None):
            return False
        else:
            return ReflectedType.__ne__(self, other)

    def __str__(self):
        return "null"

class ReflectedObject(ReflectedType):
    """
    A ReflectedType that represents a Java Object.
    """

    def __init__(self, ref, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)

        self._ref = ref
        self._class = None
        self._field_names = set()
        self._not_field_names = set(['_ref', 'getField'])

    def __getattr__(self, attr):
        if attr.startswith('_'):
            return object.__getattribute__(self, attr)

        if attr in self._field_names:
            return self._reflector.getProperty(self, attr)

        if attr not in self._not_field_names:
            try:
                return self._reflector.getProperty(self, attr)
            except ReflectionException:
                self._not_field_names.add(attr)

        return partial(self._invoker, attr)

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            object.__setattr__(self, attr, value)
            return

        if attr in self._field_names:
            return self._reflector.setProperty(self, attr, ReflectedType.fromNative(value, reflector=self._reflector))

        if attr not in self._not_field_names:
            try:
                return self._reflector.setProperty(self, attr, ReflectedType.fromNative(value, reflector=self._reflector))
            except ReflectionException:
                self._not_field_names.add(attr)

    def _invoker(self, method_name, *args, **kwargs):
        """
        Invokes methods on the object, in the Java VM, proxying through the
        reflector's invoke() method.
        """

        result = self._reflector.invoke(self, method_name, *map(lambda arg: ReflectedType.fromNative(arg, reflector=self._reflector), args), **kwargs)

        return result

    def _pb(self):
        """
        Get an Argument representation of the Object, as defined in the Mercury
        protocol.
        """

        argument = Message.Argument(type=Message.Argument.OBJECT)

        argument.object.reference = self._ref

        return argument

    def __str__(self):
        return "#<Object {}>".format(self._ref)

class ReflectedPrimitive(ReflectedType):
    """
    A ReflectedType that represents a Primitive.
    """
    
    def __init__(self, primitive_type, native, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)

        self._type = primitive_type
        self._native = native
        # TODO: validate these values

    @classmethod
    def fromArgument(cls, argument, reflector):
        """
        Builds a new ReflectedPrimitive, given an Argument as defined in the
        Mercury protocol that contains a primitive type.
        """

        if argument.primitive.type == Message.Primitive.BOOL:
            return ReflectedPrimitive("boolean", argument.primitive.bool, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.BYTE:
            return ReflectedPrimitive("byte", argument.primitive.byte, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.CHAR:
            return ReflectedPrimitive("char", argument.primitive.char, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.DOUBLE:
            return ReflectedPrimitive("double", argument.primitive.double, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.FLOAT:
            return ReflectedPrimitive("float", argument.primitive.float, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.INT:
            return ReflectedPrimitive("int", argument.primitive.int, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.LONG:
            return ReflectedPrimitive("long", argument.primitive.long, reflector=reflector)
        elif argument.primitive.type == Message.Primitive.SHORT:
            return ReflectedPrimitive("short", argument.primitive.short, reflector=reflector)
        else:
            return None

    def native(self):
        """
        Get the native representation of the primitive.
        """

        return self._native

    def _pb(self):
        """
        Get an Argument representation of the primitive, as defined in the Mercury
        protocol.
        """

        argument = Message.Argument(type=Message.Argument.PRIMITIVE)

        if self._type == "boolean":
            argument.primitive.type = Message.Primitive.BOOL
            argument.primitive.bool = self._native
        elif self._type == "byte":
            argument.primitive.type = Message.Primitive.BYTE
            argument.primitive.byte = self._native
        elif self._type == "char":
            argument.primitive.type = Message.Primitive.CHAR
            argument.primitive.char = self._native
        elif self._type == "double":
            argument.primitive.type = Message.Primitive.DOUBLE
            argument.primitive.double = self._native
        elif self._type == "float":
            argument.primitive.type = Message.Primitive.FLOAT
            argument.primitive.float = self._native
        elif self._type == "int":
            argument.primitive.type = Message.Primitive.INT
            argument.primitive.int = self._native
        elif self._type == "long":
            argument.primitive.type = Message.Primitive.LONG
            argument.primitive.long = self._native
        elif self._type == "short":
            argument.primitive.type = Message.Primitive.SHORT
            argument.primitive.short = self._native

        return argument

    def type(self):
        """
        Get the Java type of the primitive.
        """

        return self._type

    def __add__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return self._native + other._native
        else:
            return self._native + other

    def __and__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return ReflectedPrimitive(self._type, self._native & other._native)
        else:
            return ReflectedPrimitive(self._type, self._native & other)

    def __div__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return self._native / other._native
        else:
            return self._native / other

    def __divmod__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return divmod(self._native, other._native)
        else:
            return divmod(self._native, other)

    def __eq__(self, other):
        return isinstance(other, ReflectedPrimitive) and self._native == other._native or self._native == other

    def __float__(self):
        return float(self._native)

    def __ge__(self, other):
        return isinstance(other, ReflectedPrimitive) and self._native >= other._native or self._native >= other

    def __gt__(self, other):
        return isinstance(other, ReflectedPrimitive) and self._native > other._native or self._native > other

    def __int__(self):
        return int(self._native)

    def __le__(self, other):
        return isinstance(other, ReflectedPrimitive) and self._native <= other._native or self._native <= other

    def __long__(self):
        return long(self._native)

    def __lt__(self, other):
        return isinstance(other, ReflectedPrimitive) and self._native < other._native or self._native < other

    def __mod__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return self._native % other._native
        else:
            return self._native % other

    def __mul__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return self._native * other._native
        else:
            return self._native * other

    def __ne__(self, other):
        return self._native != other

    def __neg__(self):
        return -self._native

    def __nonzero__(self):
        return self._native.__nonzero__()

    def __or__(self, other):
        return ReflectedPrimitive(self._type, self._native | other._native)

    def __pos__(self):
        return self
    
    def __pow__(self, power, modulus=None):
        power = isinstance(power, ReflectedPrimitive) and power._native or power
        modulus = isinstance(modulus, ReflectedPrimitive) and modulus._native or modulus

        if modulus == None:
            return pow(self._native, power)
        else:
            return pow(self._native, power, modulus)

    def __radd__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return other._native + self._native
        else:
            return other + self._native

    def __rdiv__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return other._native / self._native
        else:
            return other / self._native

    def __rdivmod__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return divmod(other._native, self._native)
        else:
            return divmod(other, self._native)
    
    def __repr__(self):
        return repr(self._native)

    def __rmod__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return other._native % self._native
        else:
            return other % self._native

    def __rmul__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return other._native * self._native
        else:
            return other * self._native

    def __rpow__(self, mantissa, modulus=None):
        mantissa = isinstance(mantissa, ReflectedPrimitive) and mantissa._native or mantissa
        modulus = isinstance(modulus, ReflectedPrimitive) and modulus._native or modulus

        if modulus == None:
            return pow(mantissa, self._native)
        else:
            return pow(mantissa, self._native, modulus)

    def __rsub__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return other._native - self._native
        else:
            return other - self._native
    
    def __sub__(self, other):
        if isinstance(other, ReflectedPrimitive):
            return self._native - other._native
        else:
            return self._native - other

    def __str__(self):
        return "{}".format(self._native)

class ReflectedString(ReflectedType):
    """
    A ReflectedType that represents a String.
    """
    
    def __init__(self, native, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)

        self._native = native

    def capitalize(self):
        """
        Return a copy of word with only its first character capitalized.
        """

        return self._native.capitalize()

    def center(self, width, fillchar=" "):
        """
        Center a string in a field of given width.
        """

        return self._native.center(width, fillchar)

    def count(self, sub, start=0, end=-1):
        """
        Return the number of non-overlapping occurrences of substring sub in the
        range [start, end]. Optional arguments start and end are interpreted as
        in slice notation.
        """

        return self._native.count(sub, start, end)

    def endswith(self, suffix, start=0, end=None):
        """
        Return True if the string ends with the specified suffix, otherwise return
        False. suffix can also be a tuple of suffixes to look for. With optional
        start, test beginning at that position. With optional end, stop comparing
        at that position.
        """

        return self._native.endswith(suffix, start, end == None and len(self._native) or end)

    def expandtabs(self, tabsize=8):
        """
        Return a copy of the string where all tab characters are replaced by one
        or more spaces, depending on the current column and the given tab size.
        The column number is reset to zero after each newline occurring in the
        string. If tabsize is not given, a tab size of 8 characters is assumed.
        This doesn't understand other non-printing characters or escape sequences.
        """

        return self._native.expandtabs(tabsize)

    def find(self, sub, start=0, end=-1):
        """
        Return the lowest index in the string where substring sub is found,
        such that sub is contained in the slice s[start:end]. Optional
        arguments start and end are interpreted as in slice notation. Return
        -1 if sub is not found.
        """

        return self._native.find(sub, start, end)

    def format(self, *attrs):
        """
        Perform a string formatting operation.
        """

        return self._native.format(*attrs)

    def index(self, sub, start=0, end=-1):
        """
        Like find(), but raise ValueError when the substring is not found.
        """

        return self._native.index(sub, start, end)

    def isalnum(self):
        """
        Return true if all characters in the string are alphanumeric and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isalnum()

    def isalpha(self):
        """
        Return true if all characters in the string are alphabetic and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isalpha()

    def isdigit(self):
        """
        Return true if all characters in the string are digits and there
        is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isdigit()

    def islower(self):
        """
        Return true if all cased characters [4] in the string are lowercase and
        there is at least one cased character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.islower()

    def isspace(self):
        """
        Return true if there are only whitespace characters in the string and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isspace()

    def istitle(self):
        """
        Return true if the string is a titlecased string and there is at least
        one character, for example uppercase characters may only follow uncased
        characters and lowercase characters only cased ones. Return false
        otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.istitle()

    def isupper(self):
        """
        Return true if all cased characters [4] in the string are uppercase and
        there is at least one cased character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isupper()

    def join(self, iterable):
        """
        Return a string which is the concatenation of the strings in the iterable
        iterable. The separator between elements is the string providing this
        method.
        """

        return self._native.join(map(lambda s: str(s), iterable))

    def ljust(self, width, fillchar=" "):
        """
        Return the string left justified in a string of length width. Padding
        is done using the specified fillchar (default is a space). The original
        string is returned if width is less than or equal to len(s).
        """

        return self._native.ljust(width, fillchar)

    def lower(self):
        """
        Return a copy of the string with all the cased characters converted to
        lowercase.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.lower()

    def lstrip(self, chars=None):
        """
        Return a copy of the string with leading characters removed. The chars
        argument is a string specifying the set of characters to be removed.
        If omitted or None, the chars argument defaults to removing whitespace.
        """

        return self._native.lstrip(chars)

    def native(self):
        """
        Get the native representation of the String.
        """

        return self._native

    def partition(self, sep):
        """
        Split the string at the first occurrence of sep, and return a 3-tuple
        containing the part before the separator, the separator itself, and
        the part after the separator. If the separator is not found, return
        a 3-tuple containing the string itself, followed by two empty strings.
        """

        return self._native.partition(sep)

    def replace(self, old, new, count=-1):
        """
        Return a copy of the string with all occurrences of substring old
        replaced by new. If the optional argument count is given, only the
        first count occurrences are replaced.
        """

        return self._native.replace(old, new, count)

    def rfind(self, sub, start=0, end=-1):
        """
        Return the highest index in the string where substring sub is found,
        such that sub is contained within s[start:end]. Optional arguments
        start and end are interpreted as in slice notation. Return -1 on
        failure.
        """

        return self._native.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=-1):
        """
        Like rfind() but raises ValueError when the substring sub is not found.
        """

        return self._native.rindex(sub, start, end)

    def rjust(self, width, fillchar=" "):
        """
        Return the string right justified in a string of length width. Padding
        is done using the specified fillchar (default is a space). The original
        string is returned if width is less than or equal to len(s).
        """

        return self._native.rjust(width, fillchar)

    def rpartition(self, sep):
        """
        Split the string at the last occurrence of sep, and return a 3-tuple
        containing the part before the separator, the separator itself, and the
        part after the separator. If the separator is not found, return a 3-tuple
        containing two empty strings, followed by the string itself.
        """

        return self._native.rpartition(sep)

    def rsplit(self, sep=None, maxsplit=-1):
        """
        Return a list of the words in the string, using sep as the delimiter
        string. If maxsplit is given, at most maxsplit splits are done, the
        rightmost ones. If sep is not specified or None, any whitespace string
        is a separator. Except for splitting from the right, rsplit() behaves
        like split() which is described in detail below.
        """

        return self._native.rsplit(sep, maxsplit)

    def rstrip(self, chars=None):
        """
        Return a copy of the string with trailing characters removed. The chars
        argument is a string specifying the set of characters to be removed.
        If omitted or None, the chars argument defaults to removing whitespace.
        """

        return self._native.rstrip(chars)

    def split(self, *args, **kwargs):
        """
        Wrapper around the String#split method.
        """

        return self._native.split(*args, **kwargs)

    def splitlines(self, keepends=False):
        """
        Return a list of the lines in the string, breaking at line boundaries.
        This method uses the universal newlines approach to splitting lines.
        Line breaks are not included in the resulting list unless keepends is
        given and true.
        """

        return self._native.splitlines(keepends)

    def startswith(self, prefix, start=0, end=-1):
        """
        Return True if string starts with the prefix, otherwise return False.
        prefix can also be a tuple of prefixes to look for. With optional start,
        test string beginning at that position. With optional end, stop
        comparing string at that position.
        """

        return self._native.startswith(prefix, start, end)

    def strip(self, *args, **kwargs):
        """
        Wrapper around the String#strip method.
        """

        return self._native.strip(*args, **kwargs)

    def swapcase(self):
        """
        Return a copy of the string with uppercase characters converted to
        lowercase and vice versa.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.swapcase()

    def title(self):
        """
        Return a titlecased version of the string where words start with an
        uppercase character and the remaining characters are lowercase.

        The algorithm uses a simple language-independent definition of a word as
        groups of consecutive letters. The definition works in many contexts but
        it means that apostrophes in contractions and possessives form word
        boundaries, which may not be the desired result.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.title()

    #def translate(self, table, deletechars=None)
    #    """
    #    Return a copy of the string where all characters occurring in the optional
    #    argument deletechars are removed, and the remaining characters have been
    #    mapped through the given translation table, which must be a string of
    #    length 256.
    #    """

    def upper(self):
        """
        Wrapper around the String#upper method.
        """

        return self._native.upper()

    def zfill(self, width):
        """
        Return the numeric string left filled with zeros in a string of length
        width. A sign prefix is handled correctly. The original string is returned
        if width is less than or equal to len(s).
        """

        return self._native.zfill(width)

    def _pb(self):
        """
        Get the Argument representation of the String, as defined in the Mercury
        protocol.
        """

        return Message.Argument(type=Message.Argument.STRING, string=self._native)

    def __add__(self, other):
        return isinstance(other, ReflectedString) and self._native + other._native or self._native + other

    def __contains__(self, other):
        if isinstance(other, ReflectedString):
            return other._native in self._native
        else:
            return other in self._native

    def __eq__(self, other):
        return isinstance(other, ReflectedString) and self._native == other._native or self._native == other

    def __getitem__(self, key):
        return self._native[key]

    def __len__(self):
        return self._native.__len__()

    def __ne__(self, other):
        return isinstance(other, ReflectedString) and self._native != other._native or self._native != other

    def __repr__(self):
        return repr(self._native)

    def __str__(self):
        return self._native

class ReflectedBinary(ReflectedString):
    
    def base64_encode(self):
        """
        Get a Base64-encoded representation of the underlying Binary data.
        """
    
        return base64.b64encode(self._native)
        