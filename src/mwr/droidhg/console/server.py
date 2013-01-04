import socket
import ssl
import sys

from mwr.droidhg.api.builders import SystemRequestFactory
from mwr.droidhg.api.frame import Frame
from mwr.droidhg.ssl.provider import Provider

class Server:
    """
    The Server model represents a connection between a Console and a Mercury
    Server (or embedded Agent Server).

    The model is responsible for establishing the connection, and sending and
    receiving Frames on the wire.
    """

    DefaultHost = "127.0.0.1"
    DefaultPort = 31415
    
    def __init__(self, arguments, trust_callback):
        self.__id = 1
        self.__socket = socket.socket()
        
        if arguments.ssl:
            provider = Provider()
            
            self.__socket = ssl.wrap_socket(self.__socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=provider.ca_certificate_path())

        try:
            self.__socket.settimeout(90.0)
            self.__socket.connect(self.__getEndpoint(arguments))
        except socket.error as e:
            print "error connecting to server:", e.strerror.lower()

            sys.exit(-1)
        except socket.timeout as e:
            print "error connecting to server:", e.strerror.lower()

            sys.exit(-1)
        
        if arguments.ssl:
            trust_callback(provider, self.__socket.getpeercert(True), self.__socket.getpeername())

    def close(self):
        """
        Close the connection to the Server.
        """

        self.__socket.close()

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

    def receive(self):
        """
        Receive a Message from the Server.

        If not frame is available, None is returned.
        """

        frame = Frame.readFromSocket(self.__socket)

        if frame is not None:
            return frame.message()
        else:
            return None

    def send(self, message):
        """
        Send a Message to the Server.

        The Message is automatically assigned an identifier, and this is
        returned.
        """

        message_id = self.__nextId()

        frame = Frame.fromMessage(message.setId(message_id).build())

        self.__socket.sendall(str(frame))

        return message_id

    def sendAndReceive(self, message):
        """
        Send a Message to the Server, and wait for the response to be received.
        """

        message_id = self.send(message)

        while(True):
            response = self.receive()

            if response == None:
                raise RuntimeError('Received an empty response from the Agent. This normally means the remote service has crashed.')
            elif response.id == message_id:
                return response

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

    def __getEndpoint(self, arguments):
        """
        Decode the Server endpoint parameters, from an ArgumentParser arguments
        object with a server member.

        This extracts the hostname and port, assigning a default if they are
        not provided.
        """

        if arguments.server != None:
            endpoint = arguments.server
        else:
            endpoint = ":".join([Server.DefaultHost, str(Server.DefaultPort)])

        if ":" in endpoint:
            host, port = endpoint.split(":")
        else:
            host = endpoint
            port = Server.DefaultPort
        
        return (host, int(port))

    def __nextId(self):
        """
        Calculates the next Message identifier for this connection.
        """

        self.__id += 1

        return self.__id
