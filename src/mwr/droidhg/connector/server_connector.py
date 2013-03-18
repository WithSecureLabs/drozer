import socket
import sys

from mwr.cinnibar.api.builders import SystemRequestFactory
from mwr.cinnibar.api.transport import SocketTransport

class ServerConnector(SocketTransport):
    """
    The Server model represents a connection between a Console and a Mercury
    Server (or embedded Agent Server).

    The model is responsible for establishing the connection, and sending and
    receiving Frames on the wire.
    """

    DefaultHost = "127.0.0.1"
    DefaultPort = 31415
    
    def __init__(self, arguments, trust_callback=None):
        try:
            SocketTransport.__init__(self, arguments, trust_callback)
        except socket.error as e:
            print "error connecting to server:", e.strerror.lower()

            sys.exit(-1)
        except socket.timeout as e:
            print "error connecting to server:", e.strerror.lower()

            sys.exit(-1)

    def listDevices(self):
        """
        Get a list of Devices boud to the Server.
        """

        return self.sendAndReceive(SystemRequestFactory.listDevices())

    def listSessions(self):
        """
        Get a list of active sessions on the Server.
        """

        return self.sendAndReceive(SystemRequestFactory.listSessions())

    def startSession(self, device_id, password):
        """
        Start a new Session with a Device known to the Server.
        """

        return self.sendAndReceive(SystemRequestFactory.startSession(device_id).setPassword(password))

    def stopSession(self, session_id):
        """
        Stop an active Session, known to the Server.
        """

        return self.sendAndReceive(SystemRequestFactory.stopSessionId(session_id))
        