import os
import shutil

from mwr.droidhg.configuration import Configuration

class Repository(object):
    """
    Repository is a wrapper around a set of Mercury repositories, and provides
    methods for managing them.
    """
    
    @classmethod
    def all(cls):
        """
        Returns all known Mercury repositories. 
        """
        
        return Configuration.get_all_values('repositories')
        
    @classmethod
    def create(cls, path):
        """
        Create a new Mercury repository at the specified path.
        
        If the path already exists, no repository will be created.
        """
        
        if not os.path.exists(path):
            os.makedirs(path)
            
            open(os.path.join(path, "__init__.py"), 'w').close()
            open(os.path.join(path, ".mercury_repository"), 'w').close()
        
            Configuration.set('repositories', path, path)
        else:
            raise NotEmptyException(path)
    
    @classmethod
    def delete(cls, path):
        """
        Removes a Mercury repository at a specified path.
        
        If the path is not a Mercury repository, it will not be removed.
        """
        
        if cls.is_repo(path):
            shutil.rmtree(path)
            
            Configuration.delete('repositories', path)
        else:
            raise UnknownRepository(path)
        
    @classmethod
    def droidhg_modules_path(cls):
        """
        Returns the DROIDHG_MODULE_PATH, that was previously stored in an environment
        variable.
        """
        
        return ":".join(cls.all())
    
    @classmethod
    def is_repo(cls, path):
        """
        Tests if a path represents a Mercury repository.
        """
        
        return path in cls.all() and \
            os.path.exists(path) and \
            os.path.exists(os.path.join(path, "__init__.py"))  and \
            os.path.exists(os.path.join(path, ".mercury_repository")) 
        

class NotEmptyException(Exception):
    
    def __init__(self, path):
        Exception.__init__(self)
        
        self.path = path
    
    def __str__(self):
        return "The path %s is not empty." % self.path
    
    
class UnknownRepository(Exception):
    
    def __init__(self, path):
        Exception.__init__(self)
        
        self.path = path
    
    def __str__(self):
        return "Unknown Repository: %s" % self.path
    