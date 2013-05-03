from struct import pack, unpack

from pydiesel.api.protobuf_pb2 import Message

class Frame:
    """
    Models a drozer message as it is sent on-the-wire, with a 16-byte header
    comprising the version number and payload length.

    This model is able to read these frames from input streams and sockets, as
    well as build a representation that can be send on-the-wire.
    """
    
    def __init__(self, version, length, payload):
        self.version = version
        self.length = length
        self.payload = payload
        
    @classmethod
    def fromMessage(cls, message):
        """
        Builds a new Frame given a serialized Message object.
        """

        return Frame(2, len(message), message)
    
    def isValid(self):
        """
        Determines whether a Frame is valid. Since we have no checksum, we can
        only check the length.
        """

        return self.length == len(self.payload)
    
    def message(self):
        """
        Extracts the Message from a Frame by parsing the payload into a Message
        object. 
        """

        message = Message()
        message.ParseFromString(self.payload)
        
        return message
    
    def messageType(self):
        """
        Determine the type of the Message encapsulated in this Frame.
        """

        if self.message().type == Message.REFLECTION_REQUEST:
            return "REFLECTION_REQUEST"
        elif self.message().type == Message.REFLECTION_RESPONSE:
            return "REFLECTION_RESPONSE"
        elif self.message().type == Message.SYSTEM_REQUEST:
            return "SYSTEM_REQUEST"
        elif self.message().type == Message.SYSTEM_RESPONSE:
            return "SYSTEM_RESPONSE"
        else:
            return "UNKNOWN"
        
    @classmethod
    def readFrom(cls, stream):
        """
        Read a Frame from a Stream (such as a StringIO), if an entire Frame is
        available, and consumes the read bytes from the stream.

        If no more data is available, the stream is left intact and None
        returned.
        """

        position = stream.tell()
        
        header = stream.read(8)
        
        if len(header) == 8:
            version, length = unpack(">II", header)
            payload = stream.read(length)
            
            if len(payload) == length:
                return Frame(version, length, payload)
            else:
                stream.seek(position)
        else:
            stream.seek(position)

    @classmethod
    def readFromSocket(cls, socket):
        """
        Read a Frame from a network Socket.

        This blocks until a header is available, then continues to block until
        the entire payload has been read.
        """

        header = socket.recv(8)

        if len(header) == 8:
            version, length = unpack(">II", header)
            payload = ""

            while len(payload) != length:
                # TODO: add a timeout in here!
                payload += socket.recv(length - len(payload))

                if len(payload) == length:
                    return Frame(version, length, payload)
        
        return None
            
    def __repr__(self):
        return "<pydiesel.api.Frame version={} length={} {} {} />".format(
            self.version, self.length, self.isValid() and 'VALID' or 'INVALID',
            self.messageType())
        
    def __str__(self):
        return pack(">II", self.version, self.length) + self.payload
        