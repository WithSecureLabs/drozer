import itertools

from mwr.common.list import flatten

from drozer.modules import base

class ModuleCollection(object):
    
    def __init__(self, loader):
        self.__base = base.Module
        self.__loader = loader
        
    def all(self, contains=None, permissions=None, prefix=None,exploit=None, module_type="drozer"):
        """
        Loads all modules from the specified module repositories, and returns a
        collection of module identifiers.
        """

        modules = self.__loader.all(self.__base)
        modules = [m for m in modules if self.get(m).module_type == module_type]

        if contains != None:
            modules = [m for m in modules if m.find(contains.lower()) >= 0]
        if permissions != None:
            modules = [m for m in modules if len(set(self.get(m).permissions).difference(permissions)) == 0]
        if prefix != None:
            modules = [m for m in modules if m.startswith(prefix)]
        if module_type =="payload" and exploit is not None:
            modules = [m for m in modules if m in self.get(exploit).payloads]
            
        return modules

    def contributors(self):
        """
        Returns a list of module contributors, ordered by the number of modules
        they have authored (in descending order).
        """
        
        contributors = [self.get(m).author for m in self.all()]
        contribution = [(c[0], len(list(c[1]))) for c in itertools.groupby(sorted(flatten(contributors)))]
        
        return [c[0] for c in sorted(contribution, key=lambda c: -c[1])]
        
    def get(self, key):
        """
        Gets a module implementation, given its identifier.
        """

        return self.__loader.get(self.__base, key)
    
    def reload(self):
        """
        Reload all modules.
        """
        
        self.__loader.reload()
        
