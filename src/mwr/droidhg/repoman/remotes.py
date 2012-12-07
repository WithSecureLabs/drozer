import httplib
import StringIO
import urllib2

from mwr.droidhg.configuration import Configuration

class Remote(object):
    """
    Remote is a wrapper around a set of Mercury remote repositories, and provides
    methods for managing them.
    
    A Remote can be instantiated to provide API access to the repository, to
    get information about available modules and download their source.
    """
    
    def __init__(self, url):
        self.url = url
        
    @classmethod
    def all(cls):
        """
        Returns all known Mercury remotes. 
        """
        
        return Configuration.get_all_values('remotes')
        
    @classmethod
    def create(cls, url):
        """
        Create a new Mercury remote, with the specified URL.
        
        If the URL already exists, no remote will be created.
        """
        
        if cls.get(url) == None:
            Configuration.set('remotes', url, url)
    
    @classmethod
    def delete(cls, url):
        """
        Removes a Mercury remote, with the specified URL.
        """
        
        if cls.get(url) != None:
            Configuration.delete('remotes', url)
        else:
            raise UnknownRemote(url)
    
    @classmethod
    def get(cls, url):
        """
        Get an instance of Remote, initialised with the remote settings.
        """
        
        url = Configuration.get('remotes', url)
        
        if url != None:
            return cls(url)
        else:
            return None
    
    def download(self, module):
        """
        Download a module from the remote, if it exists.
        """
        
        try:
            return self.getPath(module)
        except urllib2.HTTPError:
            # such as not found: there is no module to download
            return None
        except urllib2.URLError:
            # such as connection refused: the server simply isn't there
            return None
    
    def getPath(self, path):
        """
        Fetch a file from the remote.
        """
        
        r = urllib2.urlopen(self.url + path)
        socket = FakeSocket(r.read())
        r.close()
        
        response = httplib.HTTPResponse(socket)
        response.begin()
        data = response.read()
        response.close()
        
        return data
            
        
class FakeSocket(StringIO.StringIO):
    
    def makefile(self, *args, **kwargs):
        return self
    
class UnknownRemote(Exception):
    
    def __init__(self, url):
        Exception.__init__(self)
        
        self.url = url
    
    def __str__(self):
        return "The remote %s is not registered." % self.url
    