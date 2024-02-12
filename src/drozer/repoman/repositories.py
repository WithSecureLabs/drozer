import os
import shutil

from drozer.configuration import Configuration

class Repository(object):
    """
    Repository is a wrapper around a set of drozer Repositories, and provides
    methods for managing them.
    """
    
    @classmethod
    def all(cls):
        """
        Returns all known drozer Repositories. 
        """
        
        return Configuration.get_all_values('repositories')
        
    @classmethod
    def create(cls, path):
        """
        Create a new drozer Repository at the specified path.
        
        If the path already exists, no repository will be created.
        """
        
        if not os.path.exists(path):
            os.makedirs(path)
            
            open(os.path.join(path, "__init__.py"), 'w').close()
            open(os.path.join(path, ".drozer_repository"), 'w').close()
        
            cls.enable(path)
        else:
            raise NotEmptyException(path)
    
    @classmethod
    def delete(cls, path):
        """
        Removes a drozer Repository at a specified path.
        
        If the path is not a drozer Repository, it will not be removed.
        """
        
        if cls.is_repo(path):
            cls.disable(path)
            
            shutil.rmtree(path)
        else:
            raise UnknownRepository(path)
        
    @classmethod
    def disable(cls, path):
        """
        Remove a drozer Module Repository from the collection, but leave the file
        system intact.
        """
        
        if cls.is_repo(path):
            Configuration.delete('repositories', path)
        else:
            raise UnknownRepository(path)
        
    @classmethod
    def drozer_modules_path(cls):
        """
        Returns the DROZER_MODULE_PATH, that was previously stored in an environment
        variable.
        """
        
        return ":".join(cls.all())
    
    @classmethod
    def enable(cls, path):
        """
        Re-add a drozer Module Repository to the collection, that was created manually
        or has previously been removed with #disable().
        """
        
        if cls.looks_like_repo(path):
            Configuration.set('repositories', path, path)
        else:
            raise UnknownRepository(path)
    
    @classmethod
    def is_repo(cls, path):
        """
        Tests if a path represents a drozer Repository.
        """
        
        return path in cls.all() and cls.looks_like_repo(path)
    
    @classmethod
    def looks_like_repo(cls, path):
        """
        Tests if a path looks like a drozer Repository.
        """
        
        return os.path.exists(path) and \
            os.path.exists(os.path.join(path, "__init__.py"))  and \
            os.path.exists(os.path.join(path, ".drozer_repository")) 
        

class NotEmptyException(Exception):
    """
    Raised if a new repository path already exists on the filesystem.
    """
    
    def __init__(self, path):
        Exception.__init__(self)
        
        self.path = path
    
    def __str__(self):
        return "The path %s is not empty." % self.path
    
    
class UnknownRepository(Exception):
    """
    Raised if the specified repository is not in the configuration.
    """
    
    def __init__(self, path):
        Exception.__init__(self)
        
        self.path = path
    
    def __str__(self):
        return "Unknown Repository: %s" % self.path
    
