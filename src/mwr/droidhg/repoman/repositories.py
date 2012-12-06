import ConfigParser
import os

class Repository(object):
    
    __config = None
    
    @classmethod
    def all(cls):
        cls.__ensure_config()
        
        if cls.__config.has_section('repositories'):
            return map(lambda k: cls.__config.get('repositories', k), cls.__config.options('repositories'))
        else:
            return []
            
    @classmethod
    def config_path(cls):
        return os.path.sep.join([os.path.expanduser("~"), ".mercury_config"])
        
    @classmethod
    def droidhg_modules_path(cls):
        return ":".join(cls.all())
        
    @classmethod
    def __ensure_config(cls):
        if cls.__config == None:
            cls.__config = ConfigParser.SafeConfigParser()
            
            if os.path.exists(cls.config_path()):
                cls.__config.read(cls.config_path())
            
        return cls.__config
        