from logging import getLogger

from twisted.internet.protocol import Protocol

shells = {}

class ShellCollector(Protocol):
    
    name = "shellsender"
    
    shell = None
    
    def connectionMade(self):
        self.transport.write("drozer Shell Server\n-------------------\n")
        self.transport.write("There are %d shells waiting...\n\n" % len(shells))
        
        for shell in shells:
            self.transport.write("  %s\n" % shell)
        
        self.transport.write("\n")
    
    def dataReceived(self, data):
        if self.shell == None:
            if data.strip() in shells:
                self.shell = shells[data.strip()]
                self.shell.collector = self
            
            if self.shell == None:
                self.transport.write("Shell: ")
            else:
                self.transport.write("Selecting Shell: %s\n" % data)
        else:
            self.shell.transport.write(data)
    
class ShellServer(Protocol):
    
    collector = None
    name = "shell"
    
    __logger = getLogger(__name__)
    
    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        
        del(shells["%s:%d" % (str(peer.host), peer.port)])
        
    def connectionMade(self):
        peer = self.transport.getPeer()
        
        shells["%s:%d" % (str(peer.host), peer.port)] = self
        
        self.__logger.info("accepted shell from %s:%d" % (str(peer.host), peer.port))
    
    def dataReceived(self, data):
        if self.collector != None:
            self.collector.transport.write(data)
        
