from pydiesel.api.builders import SystemRequestFactory

from drozer.session import Sessions

class Device:
    """
    Device encapsulates the parameters of a device that is bound to the Server
    when running in Infrastructure Mode.

    All devices are persisted in the Devices collection, which is a singleton
    instance of DeviceCollection.
    """
    
    def __init__(self, device_id, manufacturer, model, software):
        self.device_id = device_id
        self.manufacturer = manufacturer
        self.model = model
        self.software = software
        
        self.callbacks = {}
        self.connection = None
        self.last_message_at = None
        self.last_ping = 0
        self.last_pong = None

    def callCallback(self, callback_id, message):
        """
        Invoke a callback defined on the Device, if it exists.
        """

        if self.hasCallback(callback_id):
            callback = self.callbacks[callback_id]
            self.callbacks[callback_id] = None

            return callback(message)
        else:
            return None
    
    def enumerateSessions(self):
        """
        Send a request to the Agent, asking it to enumerate all sessions.

        The response will be intercepted by a message handler, and the Sessions
        collection updated at some point in the future.
        """
        self.write(SystemRequestFactory.listSessions().setId(999).build())

    @classmethod
    def fromProtobuf(cls, protobuf):
        """
        Build a new Device from a Protocol Buffer representation.
        """

        return Device(protobuf.id,
            protobuf.manufacturer,
            protobuf.model,
            protobuf.software)
    
    def hasCallback(self, callback_id):
        """
        Determine whether the Device has a callback with a given identifier.
        """

        return callback_id in self.callbacks and \
            self.callbacks[callback_id] is not None

    def onMessage(self, message_id, func):
        """
        Define a callback to be executed on receipt of a response to a given
        message identifier.
        """

        self.callbacks[message_id] = func

    def ping(self):
        """
        Send a ping request to the Agent.

        The response will be intercepted by a message handler, and the
        last_pong identifier updated at some point in the future.
        """

        self.last_ping += 1
        
        self.write(SystemRequestFactory.ping().setId(self.last_ping).build())

    def pong(self, pong_id):
        """
        Called by the runtime on receipt of a pong response.

        The last_pong identifier is updated to reflect the latest value.
        """

        self.last_pong = pong_id

    def sessionList(self, message):
        """
        Called by the runtime on receipt of a listing of active sessions from
        the Agent.

        The Sessions collection is updated with the most recent information.
        """

        for session in message.system_response.sessions:
            Sessions.add_session(session.session_id, self, None)

    def startSession(self, console, message):
        """
        Instantiates a new Session with the Agent, by sending a START_SESSION
        request.

        At some point in the future, the Agent will acknowledge the Session and
        the __startedSession() callback will be invoked to pass the session
        identifier back to the console.
        """

        self.onMessage(message.id, self.__startedSession(console))

        self.write(SystemRequestFactory
            .startSession(self.device_id)
            .setPassword(message.system_request.password)
            .setId(message.id)
            .build())

    def __startedSession(self, console):
        """
        Called by the runtime after a Session has been established with an
        Agent.

        This updates the Sessions collection, and forwards the message back to
        the Console.
        """

        def callback(message):
            """
            Callback to be invoked when a response to the START_SESSION request
            is received.
            """

            Sessions.add_session(message.system_response.session_id,
                self, console)

            console.write(message.SerializeToString())
        
        return callback

    def stopSession(self, console, session, message):
        """
        Terminates an active Session with the Agent, by sending a STOP_SESSION
        request.

        At some point in the future, the Agent will acknowledge the Session has
        terminated, and the __stoppedSession() callback will be invoked to
        pass update the internal state.
        """

        self.onMessage(message.id, self.__stoppedSession(console, session))

        self.write(SystemRequestFactory
            .stopSession(session)
            .setId(message.id)
            .build())

    def __stoppedSession(self, console, session):
        """
        Called by the runtime after a Session has been stopped.

        This updates the Sessions collection, and forwards the messages back to
        the Console.
        """

        def callback(message):
            """
            Callback to be invoked when a response to the START_SESSION request
            is received.
            """
            
            Sessions.remove(session)

            console.write(message.SerializeToString())
        
        return callback
    
    def write(self, message):
        """
        Sends a message to the Device, if the connection is still open.

        If the connection has closed, raises a DeviceGoneAway exception.
        """

        if self.connection != None:
            self.connection.write(message)
        else:
            raise DeviceGoneAway(self.device_id)
    
    def __eq__(self, other):
        return self.device_id == other.device_id
    
    def __hash__(self):
        return hash(self.device_id)
    
    def __ne__(self, other):
        return self.device_id != other.device_id

class DeviceCollection(set):
    """
    DeviceCollection provides a thin wrapper on top of a set to provide a DSL
    for interacting with the devices.
    """

    def addFromProtobuf(self, protobuf):
        """
        Build a Device from a Protocol Buffer representation, and add it to the
        collection.

        If the device already exists (determined by identifier), we ensure to
        return the existing device.
        """

        device = Device.fromProtobuf(protobuf)
        
        self.add(device)
        
        return self.__getMy(device)

    def getFromProtobuf(self, protobuf):
        """
        Gets a Device from the collection, given a Protocol Buffer
        representation.
        """

        return self.__getMy(Device.fromProtobuf(protobuf))
    
    def removeFromProtobuf(self, protobuf):
        """
        Removes a Device from the collection, if it exists, given a Protocol
        Buffer representation.
        """

        device = self.__getMy(Device.fromProtobuf(protobuf))
        
        self.remove(device)
        
        return device
    
    def __getMy(self, target):
        """
        Gets a Device from the collection, given another representation of a
        Device.
        """

        for device in Devices:
            if device == target:
                return device

        return None

class DeviceGoneAway(Exception):
    """
    Indicates that the device has closed its connection to the server.
    """

    def __init__(self, device_id):
        Exception.__init__(self)
        
        self.device_id = device_id

    def __str__(self):
        return "No connection to {}.".format(self.device_id)

Devices = DeviceCollection()
