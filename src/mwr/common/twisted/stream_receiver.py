from StringIO import StringIO
from twisted.internet.protocol import Protocol

class StreamReceiver(Protocol):
    """
    A Twisted Protocol that receives data from the runtime, and recombines it
    into a data stream.

    Whenever the stream is updated, the streamReceived() method is called on
    the implementation, which can choose to consume some of the data.
    """
    
    stream = None
    
    def __init__(self):
        pass
    
    def connectionMade(self):
        """
        Called when a connection is received to the StreamReceiver. This
        initialises the buffer we will use.
        """

        self.stream = StringIO()
    
    def dataReceived(self, data):
        """
        Called whenever more data is received from the client. The data is
        added to the stream, and streamReceived() called on the implementation.

        If the implementation has consumed the entire stream, we truncate
        it to preserve memory.
        """

        self.__enqueue(data)
        
        self.streamReceived()

        if self.stream.tell() == self.stream.len:
            self.stream.truncate(0)

    def __enqueue(self, data):
        """
        Append some more data to the end of the stream.
        """

        position = self.stream.tell()

        self.stream.seek(self.stream.len)
        self.stream.write(data)
        self.stream.seek(position)
        