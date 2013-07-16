from pydiesel.api.exceptions import InvalidMessageException, UnexpectedMessageException
from pydiesel.api.protobuf_pb2 import Message

class SystemResponseHandler(object):
    """
    SystemResponseHandler is given all SYSTEM_RESPONSE messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.

    The Handler returns a reply that is wishes to send.
    """
    
    def handle(self, message):
        """
        handle() is passed messages for the SystemResponseHandler to interpret.
        """

        if message.type != Message.SYSTEM_RESPONSE:
            raise InvalidMessageException("is not a SYSTEM_RESPONSE")
        if not message.HasField('system_response'):
            raise InvalidMessageException("does not contain a SYSTEM_RESPONSE")
            
        # TODO: validate the content of the message
        if message.system_response.type == Message.SystemResponse.BOUND:
            self.bound(message)
        elif message.system_response.type == Message.SystemResponse.DEVICE_LIST:
            self.device_list(message)
        elif message.system_response.type == Message.SystemResponse.PONG:
            self.pong(message)
        elif message.system_response.type == Message.SystemResponse.SESSION_ID:
            self.session_id(message)
        elif message.system_response.type == Message.SystemResponse.SESSION_LIST:
            self.session_list(message)
        elif message.system_response.type == Message.SystemResponse.UNBOUND:
            self.unbound(message)
        else:
            raise UnexpectedMessageException(message.system_response.type)
            