from base64 import b64decode
from logging import getLogger

from drozer.server.files import CreatedResource, ErrorResource
from drozer.server.receivers.http import HttpReceiver

class HTTP(HttpReceiver):
    """
    Basic implementation of an HTTP server.
    """
    
    __logger = getLogger(__name__)
    
    name = 'HTTP'
    
    def __init__(self, credentials, file_provider):
        self.__credentials = credentials
        self.__file_provider = file_provider
    
    def authenticated(self, authorization):
        """
        Checks the Authorization header, send to provide credentials
        to the server.
        """
        
        method, credentials = authorization.split(" ")
        username, password = b64decode(credentials).split(":")
        
        return method == "Basic" and username in self.__credentials and self.__credentials[username] == password
    
    def connectionMade(self):
        """
        Called when a connection is made to the HTTP Server. We write back a
        placeholder message, for testing.
        """
        
        HttpReceiver.connectionMade(self)
        
    def requestReceived(self, request):
        """
        Called when a complete HTTP request has been made to the HTTP server.
        """
        
        resource = None
        
        if request.verb == "DELETE":
            self.__logger.info("DELETE %s" % request.resource)
            
            resource = self.__file_provider.get(request.resource)
            
            if resource != None and resource.reserved:
                resource = ErrorResource(request.resource, 403, "You are not authorized to delete the resource %s.")
            else:
                self.__file_provider.delete(request.resource)
                
                resource = ErrorResource(request.resource, 200, "Deleted: %s")
        elif request.verb == "GET" or request.verb == "HEAD":
            self.__logger.info("%s %s" % (request.verb, request.resource))
            
            resource = self.__file_provider.get(request.resource)
        elif request.verb == "POST":
            self.__logger.info("POST %s (%d bytes)" % (request.resource, len(request.body)))
            
            if len(self.__credentials) > 0 and (not "Authorization" in request.headers or not self.authenticated(request.headers["Authorization"])):
                resource = ErrorResource(request.resource, 401, "You must authenticate to write the resource %s.")
                
                response = resource.getResponse(request)
                response.headers["WWW-Authenticate"] = "Basic realm=\"drozer\""
                self.transport.write(str(response))
                self.transport.loseConnection()
                return
            else:
                resource = self.__file_provider.get(request.resource)
                
                if resource != None and resource.reserved:
                    resource = ErrorResource(request.resource, 403, "You are not authorized to write the resource %s.")
                else:
                    if "Content-Type" in request.headers:
                        mimetype = request.headers["Content-Type"]
                    else:
                        mimetype = None
                    if "X-Drozer-Magic" in request.headers:
                        magic = request.headers["X-Drozer-Magic"]
                    else:
                        magic = None
                    if "X-Drozer-Vary-UA" in request.headers and request.headers["X-Drozer-Vary-UA"].startswith("true"):
                        multipart = request.headers["X-Drozer-Vary-UA"].split(";")[1].strip()
                    else:
                        multipart = None

                    custom_headers = {}
                    for key, value in request.headers.items():
                        if key.startswith("X-Drozer-Set-Header-"):
                            custom_headers[key.split("X-Drozer-Set-Header-")[1]] = value

                    print request.headers
                    
                    if magic != None and self.__file_provider.has_magic_for(magic) and self.__file_provider.get_by_magic(magic).resource != request.resource:
                        resource = ErrorResource(request.resource, 409, "Could not create %s. The specified magic has already been assigned to another resource.")
                    elif self.__file_provider.create(request.resource, request.body, magic=magic, mimetype=mimetype, multipart=multipart, custom_headers=custom_headers):
                        resource = CreatedResource(request.resource)
                    else:
                        resource = ErrorResource(request.resource, 500, "The server encountered an error whilst creating the resource %s.")

        httpResponse = resource.getResponse(request)
        if httpResponse != None and request.verb == "GET":
            resource.download(request.resource)
        if httpResponse != None and request.verb == "HEAD":
            httpResponse.body = None
 
        self.transport.write(str(httpResponse))
        self.transport.loseConnection()
        
