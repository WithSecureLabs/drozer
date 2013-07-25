from pydiesel.api import handlers, UnexpectedMessageException

class SystemResponseHandler(handlers.SystemResponseHandler):
    """
    SystemResponseHandler is given all SYSTEM_RESPONSE messages received by a
    Server. It decodes the message, and invokes an appropriate method to act
    on it.
    """

    def __init__(self, connection, logger):
        handlers.SystemResponseHandler.__init__(self)
        
        self.connection = connection
        self.__logger = logger

    def bound(self, message):
        """
        We do not expect to receive a BOUND message.
        """
        
        raise UnexpectedMessageException(message.system_response.type)
    
    def device_list(self, message):
        """
        We do not expect to receive a DEVICE_LIST response message.
        """
        
        raise UnexpectedMessageException(message.system_response.type)

    def pong(self, message):
        """
        An Agent will acknowledge all PING requests with a PONG. We keep track
        of these as they are received, to perform liveness checking and drop
        the connection to dead Agents.
        """

        if self.connection.device is not None:
            self.connection.device.pong(message.id)
            
    def session_id(self, message):
        """
        We do not expect to receive a SESSION_ID message.
        """
        
        raise UnexpectedMessageException(message.system_response.type)
            
    def session_list(self, message):
        """
        An Agent may send an updated Session list at any time. This information
        is passed to the Device, so it can update the Sessions collection.
        """

        if self.connection.device is not None:
            self.connection.device.sessionList(message)
    
    def unbound(self, message):
        """
        We do not expect to receive an UNBOUND message.
        """
        
        raise UnexpectedMessageException(message.system_response.type)
        