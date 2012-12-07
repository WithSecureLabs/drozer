from mwr.droidhg.configuration import Configuration

class Remote(object):
    """
    Remote is a wrapper around a set of Mercury remote repositories, and provides
    methods for managing them.
    
    A Remote can be instantiated to provide API access to the repository, to
    get information about available modules and download their source.
    """
    
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
            
            
class UnknownRemote(Exception):
    
    def __init__(self, url):
        Exception.__init__(self)
        
        self.url = url
    
    def __str__(self):
        return "The remote %s is not registered." % self.url
    