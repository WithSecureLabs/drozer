from pydiesel.api.protobuf_pb2 import Message

class SystemRequestFactory:
    """
    The SystemRequestFactory provides a DSL for building SystemRequest
    messages.
    """
    
    def __init__(self, request_type):
        self.builder = Message(type=Message.SYSTEM_REQUEST)
        self.builder.system_request.type = request_type
    
    def addDevice(self, device):
        """
        Set the Device specified in the message.
        """

        self.builder.system_request.device.id = device.device_id
        self.builder.system_request.device.manufacturer = device.manufacturer
        self.builder.system_request.device.model = device.model
        self.builder.system_request.device.software = device.software
        
        return self
    
    def addDeviceId(self, device_id):
        """
        Set the Device identifier specified in the message.

        This sets all other device fields (manufacturer, model and software
        to "N/A").
        """

        self.builder.system_request.device.id = device_id
        self.builder.system_request.device.manufacturer = "N/A"
        self.builder.system_request.device.model = "N/A"
        self.builder.system_request.device.software = "N/A"
        
        return self
    
    def build(self):
        """
        Serialize the built Message to a String, using the Protocol Buffer
        format.
        """

        return self.builder.SerializeToString()

    def getId(self):
        """
        Get the Identifier assigned to the message.
        """

        return self.builder.id

    @classmethod
    def listDevices(cls):
        """
        Helper method to build a request that the server list all known
        devices.
        """

        builder = SystemRequestFactory(Message.SystemRequest.LIST_DEVICES)

        return builder

    @classmethod
    def listSessions(cls):
        """
        Helper method to build a request that the server list all established
        sessions.
        """

        builder = SystemRequestFactory(Message.SystemRequest.LIST_SESSIONS)

        return builder
        
    @classmethod
    def ping(cls):
        """
        Helper method to build a ping request.
        """

        builder = SystemRequestFactory(Message.SystemRequest.PING)
        
        return builder
    
    def setId(self, message_id):
        """
        Set the identifier of the message.
        """

        self.builder.id = message_id
        
        return self

    def setPassword(self, password):
        """
        Set the password required to establish a session.
        """
        
        if password != None:
            self.builder.system_request.password = password
        
        return self
        
    def setSessionId(self, session):
        """
        Set session identifier, to route a message correctly on the Agent.
        """

        self.builder.system_request.session_id = session

        return self

    @classmethod
    def startSession(cls, device_id):
        """
        Helper method to build a request to start a session with a device.
        """

        builder = SystemRequestFactory(Message.SystemRequest.START_SESSION)

        builder.addDeviceId(device_id)

        return builder

    @classmethod
    def stopSession(cls, session):
        """
        Helper method to build a request to stop an established session.
        """

        builder = SystemRequestFactory(Message.SystemRequest.STOP_SESSION)

        builder.setSessionId(session.session_id)

        return builder

    @classmethod
    def stopSessionId(cls, session_id):
        """
        Helper method to build a request to stop an established session, by
        identifier only.
        """

        builder = SystemRequestFactory(Message.SystemRequest.STOP_SESSION)

        builder.setSessionId(session_id)

        return builder
        