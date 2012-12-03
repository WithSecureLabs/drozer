from logging import getLogger
from twisted.internet.protocol import Protocol

class HTTP(Protocol):
    """
    Basic implementation of an HTTP server.
    """
    
    __logger = getLogger(__name__)
    
    name = 'HTTP'
    
    def connectionMade(self):
        """
        Called when a connection is made to the HTTP Server. We write back a
        placeholder message, for testing.
        """
        
        self.transport.write("I should be an HTTP Server!\n")
        