import base64

from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.reflection.reflection_exception import ReflectionException
from mwr.cinnibar.reflection.types.reflected_type import ReflectedType
from mwr.cinnibar.reflection.types.reflected_string import ReflectedString

class ReflectedBinary(ReflectedString):
    
    def base64_encode(self):
        """
        Get a Base64-encoded representation of the underlying Binary data.
        """
    
        return base64.b64encode(self._native)
    
    def _pb(self):
        """
        Get the Argument representation of the String, as defined in the Mercury
        protocol.
        """

        return Message.Argument(type=Message.Argument.DATA, data=self._native)
        