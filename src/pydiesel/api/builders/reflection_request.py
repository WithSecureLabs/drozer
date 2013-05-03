from pydiesel.api.protobuf_pb2 import Message

class ReflectionRequestFactory:
    """
    The ReflectionRequestFactory provides a DSL for building ReflectionRequest
    messages.
    """
    
    def __init__(self, request_type):
        self.builder = Message(type=Message.REFLECTION_REQUEST)
        self.builder.reflection_request.type = request_type
    
    def build(self):
        """
        Serialize the built Message to a String, using the Protocol Buffer
        format.
        """

        return self.builder.SerializeToString()
    
    @classmethod
    def construct(cls, ref):
        """
        Helper method to build a CONSTRUCT request, to build a new object
        instance.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.CONSTRUCT)

        builder.builder.reflection_request.construct.object.reference = ref
        
        return builder

    @classmethod
    def delete(cls, ref):
        """
        Helper method to build a DELETE request, to remove a cached object from
        the ObjectStore.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.DELETE)

        builder.builder.reflection_request.delete.object.reference = ref
        
        return builder

    @classmethod
    def deleteAll(cls):
        """
        Helper method to build a DELETE_ALL request, to clear the ObjectStore.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.DELETE_ALL)
        
        return builder

    def getId(self):
        """
        Get the Identifier assigned to the message.
        """

        return self.builder.id
    
    @classmethod
    def getProperty(cls, ref, property_name):
        """
        Helper method to build a GET_PROPERTY request, to get the value of an
        object's field.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.GET_PROPERTY)

        builder.builder.reflection_request.get_property.object.reference = ref
        builder.builder.reflection_request.get_property.property = property_name
        
        return builder
    
    @classmethod
    def invoke(cls, ref, method_name):
        """
        Helper method to build an INVOKE request, to call a method on an object.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.INVOKE)

        builder.builder.reflection_request.invoke.object.reference = ref
        builder.builder.reflection_request.invoke.method = method_name
        
        return builder

    @classmethod
    def resolve(cls, class_name):
        """
        Helper method to build a RESOLVE request, to get a reference to a class
        given its name.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.RESOLVE)

        builder.builder.reflection_request.resolve.classname = class_name
        
        return builder

    def setArguments(self, arguments):
        """
        Adds an array of Arguments to an INVOKE or a CONSTRUCT request.
        """

        if self.builder.reflection_request.type == Message.ReflectionRequest.INVOKE:
            request = self.builder.reflection_request.invoke
        elif self.builder.reflection_request.type == Message.ReflectionRequest.CONSTRUCT:
            request = self.builder.reflection_request.construct
        else:
            request = None

        if request is not None:
            for argument in arguments:
                request.argument.add().MergeFrom(argument._pb())

        return self
    
    def setId(self, message_id):
        """
        Set the identifier of the message.
        """

        self.builder.id = message_id
        
        return self

    @classmethod
    def setProperty(cls, ref, property_name, value):
        """
        Helper method to build a SET_PROPERTY request, to assign the value of
        an object's field.
        """

        builder = ReflectionRequestFactory(Message.ReflectionRequest.SET_PROPERTY)

        builder.builder.reflection_request.set_property.object.reference = ref
        builder.builder.reflection_request.set_property.property = property_name
        builder.builder.reflection_request.set_property.value.MergeFrom(value._pb())
        
        return builder

    def setSessionId(self, session_id):
        """
        Set session identifier, to route a message correctly on the Agent.
        """

        self.builder.reflection_request.session_id = session_id
        
        return self
        