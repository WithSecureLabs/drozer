from pydiesel.api.builders import ReflectionRequestFactory
from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types import ReflectedType

class Reflector:
    """
    The Reflector provides a high-level API to interact with the reflection
    service provided by the Agent.

    The Reflector handles building of Reflection Messages, delivery to the Agent
    and interpretation of the result.
    """

    def __init__(self, session):
        self.__session = session

    def construct(self, robj, *args):
        """
        Constructs a new instance of a class, with optional arguments, and
        returns the object instance.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.construct(robj._ref).setArguments(args))
        
        if response is None:
            raise ReflectionException("expected a response to CONSTRUCT")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return ReflectedType.fromArgument(response.reflection_response.result, reflector=self)
        else:
            raise ReflectionException(response.reflection_response.errormessage)

    def delete(self, robj):
        """
        Removes an object stored in the remote ObjectStore, and return a boolean
        status.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.delete(robj._ref))

        return response != None and response.reflection_response.status == Message.ReflectionResponse.SUCCESS

    def deleteAll(self):
        """
        Removes all objects stored in the remote ObjectStore.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.deleteAll())

        if response is None:
            raise ReflectionException("expected a response to DELETE_ALL")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return True
        else:
            raise ReflectionException(response.reflection_response.errormessage)

    def getProperty(self, robj, property_name):
        """
        Reads a property from an object, and returns the value.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.getProperty(robj._ref, property_name))

        if response is None:
            raise ReflectionException("expected a response to GET_PROPERTY")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return ReflectedType.fromArgument(response.reflection_response.result, reflector=self)
        else:
            raise ReflectionException(response.reflection_response.errormessage)

    def invoke(self, robj, method, *args):
        """
        Invokes a method on an object, and returns the return value.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.invoke(robj._ref, method).setArguments(args))

        if response is None:
            raise ReflectionException("expected a response to INVOKE")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return ReflectedType.fromArgument(response.reflection_response.result, reflector=self)
        else:
            raise ReflectionException(response.reflection_response.errormessage)

    def resolve(self, class_name):
        """
        Resolves a Java class, given its fully qualified name, and returns a
        ReflectedObject that can be used to instantiate it with #construct.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.resolve(class_name))

        if response is None:
            raise ReflectionException("expected a response to RESOLVE")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return ReflectedType.fromArgument(response.reflection_response.result, reflector=self)
        else:
            raise ReflectionException(response.reflection_response.errormessage)

    def sendAndReceive(self, message_or_factory):
        """
        Provides a wrapper around the Session's sendAndReceive method.
        """

        return self.__session.sendAndReceive(message_or_factory)

    def setProperty(self, robj, property_name, value):
        """
        Sets a property on an object to a given value.
        """

        response = self.sendAndReceive(ReflectionRequestFactory.setProperty(robj._ref, property_name, value))

        if response is None:
            raise ReflectionException("expected a response to SET_PROPERTY")
        elif response.reflection_response.status == Message.ReflectionResponse.SUCCESS:
            return response
        else:
            raise ReflectionException(response.reflection_response.errormessage)
