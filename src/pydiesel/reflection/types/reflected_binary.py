import base64

from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_string import ReflectedString
from pydiesel.reflection.types.reflected_type import ReflectedType

class ReflectedBinary(ReflectedString):
    
    def base64_encode(self):
        """
        Get a Base64-encoded representation of the underlying Binary data.
        """
    
        return base64.b64encode(self._native)
    
    def _pb(self):
        """
        Get the Argument representation of the String, as defined in the drozer
        protocol.
        """

        return Message.Argument(type=Message.Argument.DATA, data=self._native)

    def __str__(self):
        return self._native

