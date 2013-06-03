from twisted.internet.protocol import ServerFactory

from drozer.server.protocol_switcher import ProtocolSwitcher

class DrozerServer(ServerFactory):
    """
    Implements a Twisted ServerFactory, which implements the ProtocolSwitcher
    protocol to support running multiple protocols on a port.
    """

    protocol = ProtocolSwitcher

    def __init__(self, enable_http):
        self.protocol.enable_http = enable_http
