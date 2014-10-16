import socket
import ssl

from pydiesel.api import Frame
from pydiesel.api.transport.exceptions import ConnectionError
from pydiesel.api.transport.transport import Transport

from drozer.ssl.provider import Provider # TODO: eugh

class SocketTransport(Transport):
    
    def __init__(self, arguments, trust_callback=None):
        Transport.__init__(self)
        self.__socket = socket.socket()
        
        if arguments.ssl:
            provider = Provider()
            self.__socket = ssl.wrap_socket(self.__socket, cert_reqs=ssl.CERT_REQUIRED, ca_certs=provider.ca_certificate_path())

        self.setTimeout(90.0)
        self.__socket.connect(self.__getEndpoint(arguments))
        
        if arguments.ssl:
            trust_callback(provider, self.__socket.getpeercert(True), self.__socket.getpeername())
            
    def close(self):
        """
        Close the connection to the Server.
        """

        self.__socket.close()
        
    def receive(self):
        """
        Receive a Message from the Server.

        If not frame is available, None is returned.
        """

        try:
            frame = Frame.readFromSocket(self.__socket)
    
            if frame is not None:
                return frame.message()
            else:
                return None
        except socket.timeout as e:
            raise ConnectionError(e)
        except ssl.SSLError as e:
            raise ConnectionError(e)

    def send(self, message):
        """
        Send a Message to the Server.

        The Message is automatically assigned an identifier, and this is
        returned.
        """

        try:
            message_id = self.nextId()
    
            frame = Frame.fromMessage(message.setId(message_id).build())
    
            self.__socket.sendall(str(frame))
    
            return message_id
        except socket.timeout as e:
            raise ConnectionError(e)
        except ssl.SSLError as e:
            raise ConnectionError(e)

    def sendAndReceive(self, message):
        """
        Send a Message to the Server, and wait for the response to be received.
        """

        message_id = self.send(message)

        while(True):
            response = self.receive()

            if response == None:
                raise ConnectionError(RuntimeError('Received an empty response from the Agent.'))
            elif response.id == message_id:
                return response
            
    def setTimeout(self, timeout):
        """
        Change the read timeout on the socket.
        """
        
        self.__socket.settimeout(timeout)

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
            endpoint = ":".join([self.DefaultHost, str(self.DefaultPort)])

        if ":" in endpoint:
            host, port = endpoint.split(":")
        else:
            host = endpoint
            port = self.DefaultPort
        
        return (host, int(port))
            
