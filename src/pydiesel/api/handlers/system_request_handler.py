from pydiesel.api.exceptions import InvalidMessageException, UnexpectedMessageException
from pydiesel.api.protobuf_pb2 import Message

class SystemRequestHandler(object):
    """
    SystemRequestHandler is given all SYSTEM_REQUEST messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.

    The Handler returns a reply that is wishes to send.
    """
    
    def handle(self, message):
        """
        handle() is passed messages for the SystemRequestHandler to interpret.
        """

        if message.type != Message.SYSTEM_REQUEST:
            raise InvalidMessageException("is not a SYSTEM_REQUEST")
        if not message.HasField('system_request'):
            raise InvalidMessageException("does not contain a SYSTEM_REQUEST")
            
        # TODO: validate the content of the message
        if message.system_request.type == Message.SystemRequest.BIND_DEVICE:
            return self.bindDevice(message)
        elif message.system_request.type == Message.SystemRequest.LIST_DEVICES:
            return self.listDevices(message)
        elif message.system_request.type == Message.SystemRequest.LIST_SESSIONS:
            return self.listSessions(message)
        elif message.system_request.type == Message.SystemRequest.PING:
            pass
        elif message.system_request.type == Message.SystemRequest.START_SESSION:
            return self.startSession(message)
        elif message.system_request.type == Message.SystemRequest.STOP_SESSION:
            return self.stopSession(message)
        elif message.system_request.type == Message.SystemRequest.UNBIND_DEVICE:
            return self.unbindDevice(message)
        else:
            raise UnexpectedMessageException(message.system_request.type)
            