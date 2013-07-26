try:
    from twisted.internet import reactor
except ImportError:
    pass

from pydiesel.api import handlers
from pydiesel.api.builders import SystemResponseFactory
from pydiesel.api.protobuf_pb2 import Message

from drozer.device import Devices
from drozer.session import Sessions

class SystemRequestHandler(handlers.SystemRequestHandler):
    """
    SystemRequestHandler is given all SYSTEM_REQUEST messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.

    The Handler returns a reply that is wishes to send.
    """
    
    def __init__(self, connection, logger):
        handlers.SystemRequestHandler.__init__(self)
        
        self.connection = connection
        self.__logger = logger
    
    def bindDevice(self, message):
        """
        Invoked when a Device wishes to bind to the Server.

        The Device is added to the collection of available Devices, and a
        request to refresh the list of active sessions is queued for later.
        """

        if message.system_request.HasField('device'):
            device = Devices.addFromProtobuf(message.system_request.device)
            
            if device in Devices:
                self.connection.device = device
                device.connection = self.connection

                def enumerateSessions():
                    """
                    We pass this function to the reactor to call later and grab
                    a list of active Sessions from the Agent.

                    We define this here to capture the outer scope temporarily.
                    """

                    device.enumerateSessions()

                reactor.callLater(1.0, enumerateSessions)
                
                self.__logger.info("accepted connection from " + device.device_id)
                return SystemResponseFactory.bound(device)\
                    .inReplyTo(message)\
                    .build()
            else:
                return SystemResponseFactory\
                    .error(Message.SystemResponse.BOUND, "error binding")\
                    .inReplyTo(message)\
                    .build()
        else:
            return SystemResponseFactory\
                .error(Message.SystemResponse.BOUND, "no device specified")\
                .inReplyTo(message)\
                .build()
    
    def listDevices(self, message):
        """
        Invoked when a Console wishes to see a list of all Devices bound to the
        Server.
        """

        return SystemResponseFactory\
            .listDevices(Devices)\
            .inReplyTo(message)\
            .build()

    def listSessions(self, message):
        """
        Invoked when a Console wishes to see a list of all active Sessions on
        the Server.
        """

        return SystemResponseFactory\
            .listSessions(Sessions)\
            .inReplyTo(message)\
            .build()
    
    def startSession(self, message):
        """
        Invoked when a Console wishes to establish a Session with a bound
        Device.
        """

        if message.system_request.HasField('device'):
            device = Devices.getFromProtobuf(message.system_request.device)

            if device is not None:
                return device.startSession(self.connection, message)
            else:
                return SystemResponseFactory\
                    .error(Message.SystemResponse.SESSION_ID, "unknown device")\
                    .inReplyTo(message)\
                    .build()
        else:
            return SystemResponseFactory\
                .error(Message.SystemResponse.SESSION_ID, "no device")\
                .inReplyTo(message)\
                .build()
    
    def stopSession(self, message):
        """
        Invoked when a Console wishes to terminate an established Session.
        """

        session = Sessions.get(message.system_request.session_id)

        if session is not None:
            return session.device.stopSession(self.connection, session, message)
        else:
            return SystemResponseFactory\
            .error(Message.SystemResponse.SESSION_ID, "unknown session")\
            .inReplyTo(message)\
            .build()
    
    def unbindDevice(self, message):
        """
        Invoked when a Device wishes to unbind from the Server.

        All handles on the device a freed. We allow Sessions to live for now,
        but they will get DeviceGoneAway when they try to make another
        request.
        """

        if message.system_request.HasField('device'):
            device = Devices.removeFromProtobuf(message.system_request.device)
            
            self.connection.device = None
            device.connection = None
            
            if(device not in Devices):
                return SystemResponseFactory\
                    .unbound(device)\
                    .inReplyTo(message)\
                    .build()
            else:
                return SystemResponseFactory\
                    .error(Message.SystemResponse.UNBOUND, "error unbinding")\
                    .inReplyTo(message)\
                    .build()
        else:
            raise Exception("UNBIND_DEVICE request does not specify a device")
        
