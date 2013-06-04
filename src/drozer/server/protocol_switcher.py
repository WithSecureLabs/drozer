from logging import getLogger
from os import path
from twisted.internet.protocol import Protocol

from drozer.server.protocols.byte_stream import ByteStream
from drozer.server.files import FileProvider, FileResource
from drozer.server.protocols.http import HTTP
from drozer.server.protocols.drozerp import Drozer

class ProtocolSwitcher(Protocol):
    """
    ProtocolSwitcher is a virtual protocol that can differentiate between different
    protocols being spoken to the drozer Server.

    If the incoming message starts with GET or POST, the server will route the
    connection to an HTTP server, otherwise it is connected to the drozer
    Server.
    """
    
    protocol = None
    
    __web_root = path.join(path.dirname(__file__), "web_root")
    __file_provider = FileProvider({ "/": FileResource("/", path.join(__web_root, "index.html"), magic="I", reserved=True, type="text/html"),
                                     "/index.html": FileResource("/index.html", path.join(__web_root, "index.html"), reserved=True, type="text/html"),
                                     "/agent-std.apk": FileResource("/agent-std.apk", path.join(__web_root, "agent-std.apk"), magic="A", type="application/vnd.android.package-archive") })
    __logger = getLogger(__name__)
    
    def __init__(self):
        pass
    
    def __chooseProtocol(self, data):
        """
        Selects which protocol to be used, by inspecting the data.
        """

        if data.startswith("DELETE") or data.startswith("GET") or data.startswith("POST"):
            return HTTP(self.credentials, self.__file_provider)
        elif self.__file_provider.has_magic_for(data.strip()):
            return ByteStream(self.__file_provider)
        else:
            return Drozer()
    
    def connectionMade(self):
        """
        When a connection is first established, no protocol is selected.
        """

        self.__logger.info("accepted incoming connection from " + str(self.transport.getPeer()))
        
        self.protocol = None
    
    def dataReceived(self, data):
        """
        When data is received, we try to select a protocol. Future messages are
        routed to the appropriate handler.
        """

        if self.protocol == None:
            protocol = self.__chooseProtocol(data)
            
            if protocol is not None:
                self.__logger.info("switching protocol to " + protocol.name + " for " + str(self.transport.getPeer()))
                
                self.protocol = protocol
                
                self.protocol.makeConnection(self.transport)
                self.protocol.dataReceived(data)
            else:
                self.__logger.error("unrecognised protocol from " + str(self.transport.getPeer()))
                
                self.transport.loseConnection()
        else:
            self.protocol.dataReceived(data)
            