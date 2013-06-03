from logging import getLogger
from twisted.internet.protocol import Protocol

from drozer.server.receivers.http import HttpReceiver, HTTPResponse

class HTTP(HttpReceiver):
    """
    Basic implementation of an HTTP server.
    """
    
    __logger = getLogger(__name__)
    
    name = 'HTTP'
    
    def __init__(self, file_provider):
        self.__file_provider = file_provider
    
    def connectionMade(self):
        """
        Called when a connection is made to the HTTP Server. We write back a
        placeholder message, for testing.
        """
        
        HttpReceiver.connectionMade(self)
        
    def requestReceived(self, request):
        """
        Called when a complete HTTP request has been made to the HTTP server.
        """
        
        self.transport.write(str(HTTPResponse(body=request.resource)))
        self.transport.loseConnection()
        