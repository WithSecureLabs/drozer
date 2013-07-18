from drozer.modules import collection, loader

Formats = ["R", "U", "X"]

class Builder(object):
    
    def __init__(self):
        self.__modules = collection.ModuleCollection(loader.ModuleLoader())
    
    def build(self, key, arguments):
        return self.module(key).execute(arguments)
        
    def module(self, key):
        return self.__modules.get(key)(None, self.__modules)
    
    def modules(self):
        return self.__modules.all(module_type="payload")
