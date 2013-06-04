from twisted.internet.protocol import Protocol

class ByteStream(Protocol):
    
    name = "bytestream"
    
    def __init__(self, file_provider):
        self.__file_provider = file_provider
    
    def dataReceived(self, data):
        self.transport.write(self.__file_provider.get_by_magic(data.strip()).getBody())
        self.transport.loseConnection()
        