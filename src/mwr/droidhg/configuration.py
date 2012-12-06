import ConfigParser
import os

class Configuration(object):
    
    __config = None
    
    @classmethod
    def get(cls, section, key):
        cls.__ensure_config()
        
        return cls.__config.get(section, key)
    
    @classmethod
    def get_all_values(cls, section):
        cls.__ensure_config()
        
        if cls.__config.has_section(section):
            return map(lambda k: cls.__config.get(section, k), cls.__config.options(section))
        else:
            return []
            
    @classmethod
    def path(cls):
        return os.path.sep.join([os.path.expanduser("~"), ".mercury_config"])
        
    @classmethod
    def __ensure_config(cls):
        if cls.__config == None:
            cls.__config = ConfigParser.SafeConfigParser()
            
            if os.path.exists(cls.path()):
                cls.__config.read(cls.path())
                