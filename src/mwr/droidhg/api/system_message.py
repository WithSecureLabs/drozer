try:
    from twisted.internet import reactor
except ImportError:
    pass

from mwr.cinnibar.api.builders import SystemResponseFactory

from mwr.droidhg import Devices, Sessions
from mwr.droidhg.api.protobuf_pb2 import Message

class SystemRequestHandler:
    """
    SystemRequestHandler is given all SYSTEM_REQUEST messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.

    The Handler returns a reply that is wishes to send.
    """
    
    def __init__(self, connection):
        self.connection = connection
    
    def handle(self, message):
        """
        handle() is passed messages for the SystemRequestHandler to interpret.
        """

        if message.type != Message.SYSTEM_REQUEST:
            raise Exception("is not a SYSTEM_REQUEST")
        if not message.HasField('system_request'):
            raise Exception("does not contain a SYSTEM_REQUEST")
        
        if message.system_request.type == Message.SystemRequest.PING:
            pass
        elif message.system_request.type == Message.SystemRequest.BIND_DEVICE:
            return self.__bindDevice(message)
        elif message.system_request.type == Message.SystemRequest.UNBIND_DEVICE:
            return self.__unbindDevice(message)
        elif message.system_request.type == Message.SystemRequest.LIST_DEVICES:
            return self.__listDevices(message)
        elif message.system_request.type == Message.SystemRequest.START_SESSION:
            return self.__startSession(message)
        elif message.system_request.type == Message.SystemRequest.STOP_SESSION:
            return self.__stopSession(message)
        elif message.system_request.type == Message.SystemRequest.LIST_SESSIONS:
            return self.__listSessions(message)
        else:
            raise Exception("unhandled SYSTEM_REQUEST type: " +
                message.system_request.type)
    
    def __bindDevice(self, message):
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
    
    def __listDevices(self, message):
        """
        Invoked when a Console wishes to see a list of all Devices bound to the
        Server.
        """

        return SystemResponseFactory\
            .listDevices(Devices)\
            .inReplyTo(message)\
            .build()

    def __listSessions(self, message):
        """
        Invoked when a Console wishes to see a list of all active Sessions on
        the Server.
        """

        return SystemResponseFactory\
            .listSessions(Sessions)\
            .inReplyTo(message)\
            .build()
    
    def __startSession(self, message):
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
    
    def __stopSession(self, message):
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
    
    def __unbindDevice(self, message):
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
            

class SystemResponseHandler:
    """
    SystemResponseHandler is given all SYSTEM_RESPONSE messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.
    """

    def __init__(self, connection):
        self.connection = connection
    
    def handle(self, message):
        """
        handle() is passed messages for the SystemResponseHandler to interpret.
        """

        if message.type != Message.SYSTEM_RESPONSE:
            raise Exception("is not a SYSTEM_RESPONSE")
        if not message.HasField('system_response'):
            raise Exception("does not contain a SYSTEM_RESPONSE")
        
        if message.system_response.type == Message.SystemResponse.PONG:
            self.__pong(message)
        elif message.system_response.type == Message.SystemResponse.BOUND:
            raise Exception("unexpected SYSTEM_RESPONSE type: BOUND")
        elif message.system_response.type == Message.SystemResponse.UNBOUND:
            raise Exception("unexpected SYSTEM_RESPONSE type: UNBOUND")
        elif message.system_response.type == Message.SystemResponse.DEVICE_LIST:
            raise Exception("unexpected SYSTEM_RESPONSE type: DEVICE_LIST")
        elif message.system_response.type == Message.SystemResponse.SESSION_ID:
            raise Exception("unexpected SYSTEM_RESPONSE type: SESSION_ID")
        elif message.system_response.type == Message.SystemResponse.SESSION_LIST:
            self.__sessionList(message)
        else:
            raise Exception("unhandled SYSTEM_RESPONSE type: " +
                str(message.system_response.type))

    def __sessionList(self, message):
        """
        An Agent may send an updated Session list at any time. This information
        is passed to the Device, so it can update the Sessions collection.
        """

        if self.connection.device is not None:
            self.connection.device.sessionList(message)

    def __pong(self, message):
        """
        An Agent will acknowledge all PING requests with a PONG. We keep track
        of these as they are received, to perform liveness checking and drop
        the connection to dead Agents.
        """

        if self.connection.device is not None:
            self.connection.device.pong(message.id)
