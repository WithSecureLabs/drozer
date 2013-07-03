from base64 import b64encode
from socket import socket
import ssl

from drozer.server.receivers.http import HTTPRequest, HTTPResponse
from drozer.ssl.provider import Provider

def delete(arguments, resource):
    pass
    #factory = UploaderFactory(arguments, "DELETE", resource, "", None)
    #if arguments.ssl != None:
    #    reactor.connectSSL(arguments.server[0], arguments.server[1], factory, ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
    #else:
    #    reactor.connectTCP(arguments.server[0], arguments.server[1], factory)
    #reactor.run()

def upload(arguments, resource, data, magic=None):
    #factory = UploaderFactory(arguments, "POST", resource, data, magic)
    sock = socket()
    
    if arguments.ssl:
        provider = Provider()
        
        sock = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs=provider.ca_certificate_path())

    sock.settimeout(90.0)
    sock.connect(arguments.server)
    
    #if arguments.ssl:
        #trust_callback(provider, sock.getpeercert(True), sock.getpeername())
    
    request = HTTPRequest(verb="POST", resource=resource, body=data)
    if arguments.credentials != None:
        request.headers["Authorization"] = "Basic %s" % b64encode(":".join(arguments.credentials))
    request.headers["Content-Length"] = len(data)
    if magic != None:
        request.headers["X-Drozer-Magic"] = magic
        
    request_data = str(request)
    sent = 0
    
    while sent < len(request_data):
        sent += sock.send(request_data[sent:])
    
    response = HTTPResponse.readFrom(sock)

    return response.status == 201
