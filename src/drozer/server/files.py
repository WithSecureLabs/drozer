from drozer.server.receivers.http import HTTPResponse

class FileProvider(object):
    
    def __init__(self, store={}):
        self.__store = store
    
    def create(self, resource, body):
        self.__store[resource] = InMemoryResource(resource, body)
        
        return self.__store[resource].getBody() == body
        
    def delete(self, resource):
        del self.__store[resource]
        
    def get(self, resource):
        if resource in self.__store:
            return self.__store[resource]
        else:
            return ErrorResource(resource, 404, "The resource %s could not be found on this server.")
        
        
class Resource(object):
    
    def __init__(self, resource, reserved=False):
        self.resource = resource
        self.reserved = reserved

    def getBody(self):
        return None
    
    def getResponse(self):
        return None


class ErrorResource(Resource):
    
    def __init__(self, resource, code, description):
        Resource.__init__(self, resource, False)
        
        self.code = code
        self.description = description
    
    def getBody(self):
        return "<h1>%d %s</h1><p>%s</p><hr/><p>drozer Server</p>" % (self.code, HTTPResponse(status=self.code).status_text(), self.description % self.resource)
    
    def getResponse(self):
        return HTTPResponse(status=self.code, body=self.getBody())
        
        
class FileResource(Resource):
    
    def __init__(self, resource, path, reserved=False):
        Resource.__init__(self, resource, reserved)
        
        self.path = path
    
    def getBody(self):
        return open(self.path).read()
            
    def getResponse(self):
        return HTTPResponse(status=200, body=self.getBody())
    
class InMemoryResource(Resource):
    
    def __init__(self, resource, body):
        Resource.__init__(self, resource, False)
        
        self.body = body
    
    def getBody(self):
        return self.body
            
    def getResponse(self):
        return HTTPResponse(status=200, body=self.getBody())
    