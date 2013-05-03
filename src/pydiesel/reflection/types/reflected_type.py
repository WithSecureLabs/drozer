from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException

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
    
    reflected_array = None
    reflected_binary = None
    reflected_null = None
    reflected_object = None
    reflected_primitive = None
    reflected_string = None

    def __init__(self, reflector=None):
        self._reflector = reflector

    @classmethod
    def fromArgument(cls, argument, reflector):
        """
        Creates a new ReflectedType, given an Argument message as defined in
        the drozer protocol.
        """

        if isinstance(argument, ReflectedType):
            return argument
        elif argument.type == Message.Argument.ARRAY:
            return cls.reflected_array.fromArgument(argument, reflector=reflector)
        elif argument.type == Message.Argument.DATA:
            return cls.reflected_binary(argument.data, reflector=reflector)
        elif argument.type == Message.Argument.NULL:
            return cls.reflected_null(reflector=reflector)
        elif argument.type == Message.Argument.OBJECT:
            return cls.reflected_object(argument.object.reference, reflector=reflector)
        elif argument.type == Message.Argument.PRIMITIVE:
            return cls.reflected_primitive.fromArgument(argument, reflector)
        elif argument.type == Message.Argument.STRING:
            return cls.reflected_string(argument.string, reflector=reflector)
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
            return cls.reflected_primitive("long", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, int) or obj_type == "int":
            return cls.reflected_primitive("int", obj, reflector=reflector)
        elif obj_type == "byte" and isinstance(obj, int):
            return cls.reflected_primitive("byte", obj, reflector=reflector)
        elif obj_type == "char" and isinstance(obj, int):
            return cls.reflected_primitive("char", obj, reflector=reflector)
        elif obj_type == "short":
            return cls.reflected_primitive("short", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, float) or obj_type == "float":
            return cls.reflected_primitive("float", obj, reflector=reflector)
        elif obj_type == None and isinstance(obj, bool) or obj_type == "boolean":
            return cls.reflected_primitive("boolean", obj, reflector=reflector)
        elif obj_type == "data":
            return cls.reflected_binary(obj, reflector=reflector)
        elif obj_type == None and (isinstance(obj, str) or isinstance(obj, unicode)) or obj_type == "string":
            return cls.reflected_string(obj, reflector=reflector)
        elif obj_type == "double":
            return cls.reflected_primitive("double", obj, reflector=reflector)
        elif obj is None:
            return cls.reflected_null(reflector=reflector)
        elif hasattr(obj, '__iter__'):
            return cls.reflected_array(obj, reflector=reflector)
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
            