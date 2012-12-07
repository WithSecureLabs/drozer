import ConfigParser
import os

class Configuration(object):
    """
    Configuration provides a wrapper around a user's Mercury configuration, stored
    in their home directory as .mercury_config.
    """
    
    __config = None
    
    @classmethod
    def delete(cls, section, key):
        """
        Removes a key from the configuration, and persists the change to disk.
        """
        
        cls.__ensure_config()
        
        cls.__config.remove_option(section, key)
        cls.__config.write(open(cls.path(), 'w'))
    
    @classmethod
    def get(cls, section, key):
        """
        Returns a single configuration value.
        """
        
        cls.__ensure_config()
        
        try:
            if cls.__config.has_section(section):
                return cls.__config.get(section, key)
            else:
                return None
        except ConfigParser.NoOptionError:
            return None
    
    @classmethod
    def get_all_keys(cls, section):
        """
        Returns all keys from a section of the configuration file.
        """
        
        cls.__ensure_config()
        
        if cls.__config.has_section(section):
            return cls.__config.options(section)
        else:
            return []
        
    @classmethod
    def get_all_values(cls, section):
        """
        Returns all values from a section of the configuration file.
        """
        
        cls.__ensure_config()
        
        if cls.__config.has_section(section):
            return map(lambda k: cls.__config.get(section, k), cls.__config.options(section))
        else:
            return []
            
    @classmethod
    def path(cls):
        """
        Returns the path to the configuration file.
        """
        
        return os.path.sep.join([os.path.expanduser("~"), ".mercury_config"])
    
    @classmethod
    def set(cls, section, key, value):
        """
        Sets a key in the configuration (creating it if it does not exist), and persists
        the change to disk.
        """
        
        cls.__ensure_config()
        
        cls.__config.set(section, key, value)
        cls.__config.write(open(cls.path(), 'w'))
        
    @classmethod
    def __ensure_config(cls):
        """
        Loads the configuration from file, if it has not already been loaded.
        """
        
        if cls.__config == None:
            cls.__config = ConfigParser.SafeConfigParser()
            
            if os.path.exists(cls.path()):
                cls.__config.read(cls.path())
                