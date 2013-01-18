from mwr.cinnibar.reflection.reflection_exception import ReflectionException
from mwr.cinnibar.reflection.types.reflected_type import ReflectedType

from mwr.droidhg.api.protobuf_pb2 import Message

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
        