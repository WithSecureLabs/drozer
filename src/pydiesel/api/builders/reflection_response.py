from pydiesel.api.protobuf_pb2 import Message

class ReflectionResponseFactory:
    """
    The ReflectionResponseFactory provides a DSL for building ReflectionResponse
    messages.
    """
    
    def __init__(self):
        self.builder = Message(type=Message.REFLECTION_RESPONSE)
        self.builder.reflection_response.status = Message.ReflectionResponse.SUCCESS
    
    def build(self):
        """
        Serialize the built Message to a String, using the Protocol Buffer
        format.
        """

        return self.builder.SerializeToString()
    
    @classmethod
    def error(cls, message):
        """
        Helper method to build an error response.
        """

        builder = ReflectionResponseFactory()
        
        builder.isError()
        builder.setErrorMessage(message)
        
        return builder

    @classmethod
    def fatal(cls, message):
        """
        Helper method to build a fatal error response.
        """

        builder = ReflectionResponseFactory()
        
        builder.isFatal()
        builder.setErrorMessage(message)
        
        return builder
    
    def inReplyTo(self, message):
        """
        Tag the response as a reply to another message, by setting the message
        identifiers to be equal and setting the session to keep the flow
        intact.
        """

        self.builder.id = message.id
        self.builder.reflection_response.session_id = message.reflection_request.session_id
        
        return self
    
    def isError(self):
        """
        Indicate an error in the response status code.
        """

        self.builder.reflection_response.status = Message.ReflectionResponse.ERROR
    
    def isFatal(self):
        """
        Indicate a fatal error in the response status code.
        """

        self.builder.reflection_response.status = Message.ReflectionResponse.FATAL
    
    def isSuccess(self):
        """
        Indicate success in the response status code.
        """

        self.builder.reflection_response.status = Message.ReflectionResponse.SUCCESS

    def setErrorMessage(self, message):
        """
        Set the error message associated with this response.
        """

        self.builder.reflection_response.errormessage = message

        return self
        