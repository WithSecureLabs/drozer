from logging import getLogger
from os import path
import sys

try:
    from twisted.internet import reactor, ssl, task
    from twisted.internet.protocol import Protocol, ServerFactory
except ImportError:
    print "drozer Server requires Twisted to run."
    print "Run 'pip install twisted' to fetch this dependency."
    sys.exit(-1)

from drozer.configuration import Configuration
from drozer.server.heartbeat import heartbeat
from drozer.server.protocols.byte_stream import ByteStream
from drozer.server.protocols.shell import ShellCollector, ShellServer
from drozer.server.files import FileProvider, FileResource, StatusResource
from drozer.server.protocols.http import HTTP
from drozer.server.protocols.drozerp import Drozer
from drozer.ssl.provider import Provider

def serve(arguments):
    task.LoopingCall(heartbeat).start(arguments.ping_interval)
        
    if arguments.ssl != None:
        print "Starting drozer Server, listening on 0.0.0.0:%d (with SSL)" % arguments.port

        if arguments.ssl == []:
            print "Using default SSL key material..."
            
            arguments.ssl = Provider().get_keypair("drozer-server")
        
        reactor.listenSSL(arguments.port,
                          SwitcherFactoryServer(dict(arguments.credentials)),
                          ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
    else:
        print "Starting drozer Server, listening on 0.0.0.0:%d" % arguments.port
        
        reactor.listenTCP(arguments.port,
                          SwitcherFactoryServer(dict(arguments.credentials)))
    
    reactor.run()
        
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
    __file_provider = FileProvider({ "/": FileResource("/", path.join(__web_root, "index.html"), magic="I", reserved=False, type="text/html"),
                                     "/default-agent\\.apk": FileResource("/default-agent.apk", Configuration.library("standard-agent.apk"), reserved=True, type="application/vnd.android.package-archive"),
                                     "/agent\\.jar": FileResource("/agent.jar", Configuration.library("agent.jar"), reserved=False, type="application/vnd.android.package-archive"),
                                     "/drozer\\.png": FileResource("/drozer.png", path.join(__web_root, "drozer.png"), reserved=False, type="image/png"),
                                     "/favicon\\.png": FileResource("/favicon.png", path.join(__web_root, "favicon.png"), reserved=False, type="image/png"),
                                     "/index\\.html": FileResource("/index.html", path.join(__web_root, "index.html"), reserved=False, type="text/html"),
                                     "/jquery\\.js": FileResource("/jquery.js", path.join(__web_root, "jquery.js"), reserved=False, type="text/javascript"),
                                     "/labs\\.png": FileResource("/labs.png", path.join(__web_root, "labs.png"), reserved=False, type="image/png") })
    __file_provider.add("/status\\?.*", StatusResource("/status", __file_provider))
    __logger = getLogger(__name__)
    
    def __init__(self):
        pass
    
    def __chooseProtocol(self, data):
        """
        Selects which protocol to be used, by inspecting the data.
        """

        if data.startswith("DELETE") or data.startswith("GET") or data.startswith("HEAD") or data.startswith("POST"):
            return HTTP(self.factory.credentials, self.__file_provider)
        elif data.startswith("COLLECT"):
            return ShellCollector()
        elif data.startswith("S"):
            return ShellServer()
        elif self.__file_provider.has_magic_for(data.strip()):
            return ByteStream(self.__file_provider)
        else:
            return Drozer()
    
    def connectionMade(self):
        """
        When a connection is first established, no protocol is selected.
        """

        self.__logger.debug("accepted incoming connection from " + str(self.transport.getPeer()))
        
        self.protocol = None
    
    def dataReceived(self, data):
        """
        When data is received, we try to select a protocol. Future messages are
        routed to the appropriate handler.
        """

        if self.protocol == None:
            protocol = self.__chooseProtocol(data)
            
            if protocol is not None:
                self.__logger.debug("switching protocol to " + protocol.name + " for " + str(self.transport.getPeer()))
                
                self.protocol = protocol
                
                self.protocol.makeConnection(self.transport)
                self.protocol.dataReceived(data)
            else:
                self.__logger.error("unrecognised protocol from " + str(self.transport.getPeer()))
                
                self.transport.loseConnection()
        else:
            self.protocol.dataReceived(data)
            
class SwitcherFactoryServer(ServerFactory):
    """
    Implements a Twisted ServerFactory, which implements the ProtocolSwitcher
    protocol to support running multiple protocols on a port.
    """

    protocol = ProtocolSwitcher

    def __init__(self, credentials):
        self.credentials = credentials
