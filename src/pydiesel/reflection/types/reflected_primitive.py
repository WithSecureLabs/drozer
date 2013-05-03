from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_type import ReflectedType

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
        drozer protocol that contains a primitive type.
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
        Get an Argument representation of the primitive, as defined in the drozer
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
        