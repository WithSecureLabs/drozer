from drozer.server.receivers.http import HTTPResponse

class FileProvider(object):
    
    def __init__(self, store={}):
        self.__store = store
    
    def create(self, resource, body, magic=None):
        self.__store[resource] = InMemoryResource(resource, body, magic=magic)
        
        return self.__store[resource].getBody() == body
        
    def delete(self, resource):
        del self.__store[resource]
        
    def get(self, resource):
        if resource in self.__store:
            return self.__store[resource]
        else:
            return ErrorResource(resource, 404, "The resource %s could not be found on this server.")
    
    def get_by_magic(self, magic):
        resources = filter(lambda r: self.__store[r].magic == magic, self.__store)
        
        if len(resources) == 1:
            return self.__store[resources[0]]
        else:
            return None
    
    def has_magic_for(self, magic):
        resources = filter(lambda r: self.__store[r].magic == magic, self.__store)
        
        if len(resources) == 1:
            return True
        else:
            return False
        
        
class Resource(object):
    
    def __init__(self, resource, magic=None, reserved=False):
        self.resource = resource
        self.reserved = reserved
        self.magic = magic

    def getBody(self):
        return None
    
    def getResponse(self):
        return None


class CreatedResource(Resource):
    
    def __init__(self, resource):
        Resource.__init__(self, resource, False)
        
        self.code = 201
        self.description = "Location: %s"
        self.resource = resource
    
    def getBody(self):
        return "<h1>%d %s</h1><p>%s</p><hr/><p>drozer Server</p>" % (self.code, HTTPResponse(status=self.code).status_text(), self.description % self.resource)
    
    def getResponse(self):
        return HTTPResponse(status=self.code, headers={ "Location": self.resource }, body=self.getBody())
        
    
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
    
    def __init__(self, resource, path, magic=None, reserved=False, type="text/plain"):
        Resource.__init__(self, resource, magic=magic, reserved=reserved)
        
        self.path = path
        self.type = type
    
    def getBody(self):
        return open(self.path).read()
            
    def getResponse(self):
        response = HTTPResponse(status=200, body=self.getBody())
        response.headers["Content-Type"] = self.type
        
        return response
    
class InMemoryResource(Resource):
    
    def __init__(self, resource, body, magic=None):
        Resource.__init__(self, resource, magic=magic, reserved=False)
        
        self.body = body
    
    def getBody(self):
        return self.body
            
    def getResponse(self):
        return HTTPResponse(status=200, body=self.getBody())
    