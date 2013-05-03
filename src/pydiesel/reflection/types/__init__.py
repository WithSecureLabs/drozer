
__all__ = [ "ReflectedArray",
           "ReflectedBinary",
           "ReflectedNull",
           "ReflectedObject",
           "ReflectedPrimitive",
           "ReflectedString",
           "ReflectedType" ]

from pydiesel.reflection.types.reflected_array import ReflectedArray
from pydiesel.reflection.types.reflected_binary import ReflectedBinary
from pydiesel.reflection.types.reflected_null import ReflectedNull
from pydiesel.reflection.types.reflected_object import ReflectedObject
from pydiesel.reflection.types.reflected_primitive import ReflectedPrimitive
from pydiesel.reflection.types.reflected_string import ReflectedString
from pydiesel.reflection.types.reflected_type import ReflectedType

ReflectedType.reflected_array = ReflectedArray
ReflectedType.reflected_binary = ReflectedBinary
ReflectedType.reflected_null = ReflectedNull
ReflectedType.reflected_object = ReflectedObject
ReflectedType.reflected_primitive = ReflectedPrimitive
ReflectedType.reflected_string = ReflectedString
