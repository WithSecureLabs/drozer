
__all__ = [ "ReflectedArray",
           "ReflectedBinary",
           "ReflectedNull",
           "ReflectedObject",
           "ReflectedPrimitive",
           "ReflectedString",
           "ReflectedType" ]

from pysolar.reflection.types.reflected_array import ReflectedArray
from pysolar.reflection.types.reflected_binary import ReflectedBinary
from pysolar.reflection.types.reflected_null import ReflectedNull
from pysolar.reflection.types.reflected_object import ReflectedObject
from pysolar.reflection.types.reflected_primitive import ReflectedPrimitive
from pysolar.reflection.types.reflected_string import ReflectedString
from pysolar.reflection.types.reflected_type import ReflectedType

ReflectedType.reflected_array = ReflectedArray
ReflectedType.reflected_binary = ReflectedBinary
ReflectedType.reflected_null = ReflectedNull
ReflectedType.reflected_object = ReflectedObject
ReflectedType.reflected_primitive = ReflectedPrimitive
ReflectedType.reflected_string = ReflectedString
