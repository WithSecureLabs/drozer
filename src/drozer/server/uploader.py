from base64 import b64encode

from twisted.internet import ssl, reactor
from twisted.internet.protocol import ClientFactory, Protocol

from drozer.server.receivers.http import HTTPRequest, HTTPResponse

def delete(arguments, resource):
    factory = UploaderFactory(arguments, "DELETE", resource, "", None)
    if arguments.ssl != None:
        reactor.connectSSL('localhost', arguments.port, factory, ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
    else:
        reactor.connectTCP('localhost', arguments.port, factory)
    reactor.run()

def upload(arguments, resource, data, magic=None):
    factory = UploaderFactory(arguments, "POST", resource, data, magic)
    if arguments.ssl != None:
        reactor.connectSSL('localhost', arguments.port, factory, ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
    else:
        reactor.connectTCP('localhost', arguments.port, factory)
    reactor.run()

class Uploader(Protocol):
    
    def connectionMade(self):
        request = HTTPRequest(verb=self.factory.verb, resource=self.factory.resource, body=self.factory.data)
        if self.factory.arguments.credentials != None:
            request.headers["Authorization"] = "Basic %s" % b64encode(":".join(self.factory.arguments.credentials))
        request.headers["Content-Length"] = len(self.factory.data)
        if self.factory.magic != None:
            request.headers["X-Drozer-Magic"] = self.factory.magic
        
        self.transport.write(str(request))

    def dataReceived(self, data):
        response = HTTPResponse.parse(data)
        
        if response.status == 201:
            print response.body
        else:
            print response.headers
            print response.body
            
        self.transport.loseConnection()
                
class UploaderFactory(ClientFactory):
    
    protocol = Uploader

    def __init__(self, arguments, verb, resource, data, magic=None):
        self.arguments = arguments
        self.data = data
        self.magic = magic
        self.resource = resource
        self.verb = verb
        
    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()
        