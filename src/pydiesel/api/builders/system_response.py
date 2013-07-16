from pydiesel.api.protobuf_pb2 import Message

class SystemResponseFactory:
    """
    The SystemResponseFactory provides a DSL for building SystemResponse
    messages.
    """
    
    def __init__(self, response_type):
        self.builder = Message(type=Message.SYSTEM_RESPONSE)
        self.builder.system_response.type = response_type
        self.builder.system_response.status = Message.SystemResponse.SUCCESS
    
    def addDevice(self, device):
        """
        Add a Device to the list of devices within the message.
        """

        d = self.builder.system_response.devices.add()
        d.id = device.device_id
        d.manufacturer = device.manufacturer
        d.model = device.model
        d.software = device.software
        
        return d

    def add_session(self, session):
        """
        Add a Session to the list of Sessions within the message.
        """

        s = self.builder.system_response.sessions.add()
        s.id = session.session_id
        s.device_id = session.device.device_id
    
    @classmethod
    def bound(cls, device):
        """
        Helper method to build a message to indicate a Device has successfully
        bound to the server.
        """

        builder = SystemResponseFactory(Message.SystemResponse.BOUND)
        
        builder.addDevice(device)
        
        return builder
    
    def build(self):
        """
        Serialize the built Message to a String, using the Protocol Buffer
        format.
        """

        return self.builder.SerializeToString()
    
    @classmethod
    def error(cls, error_type, message):
        """
        Helper method to build an error message, with a particular type and an
        error message.
        """

        builder = SystemResponseFactory(error_type)
        
        builder.isError()
        builder.setErrorMessage(message)
        
        return builder
    
    def inReplyTo(self, message):
        """
        Tag the response as a reply to another message, by setting the message
        identifiers to be equal.
        """

        self.builder.id = message.id
        
        return self
    
    def isError(self):
        """
        Indicate an error in the response status code.
        """

        self.builder.system_response.status = Message.SystemResponse.ERROR
    
    def isSuccess(self):
        """
        Indicate success in the response status code.
        """

        self.builder.system_response.status = Message.SystemResponse.SUCCESS
        
    @classmethod
    def listDevices(cls, devices):
        """
        Helper method to build a DEVICE_LIST response, with a list of devices
        built from a collection.
        """

        builder = SystemResponseFactory(Message.SystemResponse.DEVICE_LIST)
        
        for device in devices:
            builder.addDevice(device)
        
        return builder

    @classmethod
    def listSessions(cls, sessions):
        """
        Helper method to build a SESSION_LIST response, with a list of sessions
        build from a collection.
        """

        builder = SystemResponseFactory(Message.SystemResponse.SESSION_LIST)

        #for session in sessions:
        #    builder.add_session(session)

        return builder

    def setErrorMessage(self, message):
        """
        Set the error message associated with this response.
        """

        self.builder.system_response.error_message = message

        return self
    
    @classmethod
    def unbound(cls, device):
        """
        Helper method to build a message to indicate a device has successfully
        unbound from the Server.
        """

        builder = SystemResponseFactory(Message.SystemResponse.UNBOUND)
        
        builder.addDevice(device)
        
        return builder
