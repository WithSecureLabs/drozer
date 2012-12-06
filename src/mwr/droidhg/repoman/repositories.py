from mwr.droidhg.configuration import Configuration

class Repository(object):
    
    @classmethod
    def all(cls):
        return Configuration.get_all_values('repositories')
        
    @classmethod
    def droidhg_modules_path(cls):
        return ":".join(cls.all())
        