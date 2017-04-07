from logging import getLogger
from time import time

from pydiesel.api import Frame
from pydiesel.api.protobuf_pb2 import Message

from drozer.api.handlers import *
from drozer.server.receivers.frame import FrameReceiver

class Drozer(FrameReceiver):
    """
    Implementation of the drozer Protocol, as a FrameReceiver.
    """
    
    __logger = getLogger(__name__ + '.drozer')
    
    name = 'drozer'
    
    device = None
    request_forwarder = None
    request_handler = None
    response_forwarder = None
    response_handler = None
    
    def __init__(self, *args, **kwargs):
        FrameReceiver.__init__(self, *args, **kwargs)
    
    def connectionMade(self):
        """
        Called whena a connection is made to the drozer Server. It initialises
        the FrameReceiver, and then sets up the various message handlers and
        forwarders that we require.
        """

        FrameReceiver.connectionMade(self)

        self.request_forwarder = ReflectionRequestForwarder(self, self.__logger)
        self.request_handler = SystemRequestHandler(self, self.__logger)
        self.response_forwarder = ReflectionResponseForwarder(self, self.__logger)
        self.response_handler = SystemResponseHandler(self, self.__logger)
        
        self.device = None
    
    def close(self):
        """
        Closes the connection.
        """

        self.transport.loseConnection()
    
    def frameReceived(self, frame):
        """
        Called whenever a frame has been received.

        This extracts the message, and routes it appropriately to a callback
        function, or a request handler.

        If something sends a response, this is forwarded back to the client.
        """

        message = frame.message()
        response = None

        if self.device and self.device.hasCallback(message.id):
            response = self.device.callCallback(message.id, message)
        elif message.type == Message.REFLECTION_REQUEST:
            self.request_forwarder.handle(message)
        elif message.type == Message.REFLECTION_RESPONSE:
            self.response_forwarder.handle(message)
        elif message.type == Message.SYSTEM_REQUEST:
            response = self.request_handler.handle(message)
        elif message.type == Message.SYSTEM_RESPONSE:
            response = self.response_handler.handle(message)
        else:
            self.__logger.error("got unexpected message type " + message.type)
        
        if response is not None:
            self.write(response)
        
        if self.device is not None:
            self.device.last_message_at = time()
    
    def write(self, message):
        """
        Writes a message to a client, encapsulating it in a Frame first.
        """

        self.__write(Frame.fromMessage(message))
        
    def __write(self, frame):
        """
        Writes a message to a client.
        """
        
        self.transport.write(str(frame))
        
