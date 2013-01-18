import base64

from mwr.cinnibar.reflection.reflection_exception import ReflectionException
from mwr.cinnibar.reflection.types.reflected_type import ReflectedType
from mwr.cinnibar.reflection.types.reflected_string import ReflectedString

from mwr.droidhg.api.protobuf_pb2 import Message

class ReflectedBinary(ReflectedString):
    
    def base64_encode(self):
        """
        Get a Base64-encoded representation of the underlying Binary data.
        """
    
        return base64.b64encode(self._native)
        