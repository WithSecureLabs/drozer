import os
import sys

from drozer.modules.import_conflict_resolver import ImportConflictResolver
from drozer.repoman import Repository

class ModuleLoader(object):

    def __init__(self):
        self.__conflict_resolver = ImportConflictResolver
        self.__modules = {}
        self.__module_paths = os.path.join(os.path.dirname(__file__), "..", "modules")

    def all(self, base):
        """
        Loads all modules from the specified module repositories, and returns a
        collection of module identifiers.
        """

        if(len(self.__modules) == 0):
            self.__load(base)

        return sorted(self.__modules.keys())

    def get(self, base, key):
        """
        Gets a module implementation, given its identifier.
        """

        if(len(self.__modules) == 0):
            self.__load(base)
        
        return self.__modules[key]

    def reload(self):
        self.__modules = {}

    def __import_modules(self, modules):
        """
        Import all modules, given a collection of Python modules.
        """

        for i in modules.keys():
            if modules[i] is not None and modules[i] != "drozer.modules.base":
                try:
                    __import__(modules[i])
                    # Reload the module in case the source has changed. We don't
                    # need to be careful over i, because the import must have
                    # been successful to get here.
                    if modules[i] in sys.modules:
                        reload(sys.modules[modules[i]])
                except ImportError:
                    sys.stderr.write("Skipping source file at %s. Unable to load Python module.\n" % modules[i])
                    pass 
                except IndentationError:
                    sys.stderr.write("Skipping source file at %s. Indentation Error.\n" % modules[i])
                    pass

    def __load(self, base):
        """
        Load all modules from module repositories.
        """

        self.__modules = {}

        self.__import_modules(self.__locate())

        for klass in self.__subclasses_of(base):
            if klass != base:
                if not klass.fqmn() in self.__modules: 
                    self.__modules[klass.fqmn()] = klass
                else:
                    self.__modules[klass.fqmn()] = self.__conflict_resolver().resolve(self.__modules[klass.fqmn()], klass)

    def __locate(self):
        """
        Search the module paths for Python modules, which may contain drozer
        Modules, and build a collection of Python modules to load.
        """

        modules = {}
        
        for path in self.__paths():
            for dirpath, _dirnames, filenames in os.walk(path):
                for filename in filenames:
                    module_path = os.path.join(dirpath[len(path) + len(os.path.sep):], filename)
                    module_name, ext = os.path.splitext(module_path)

                    if ext in [".py", ".pyc", ".pyo"]:
                        namespace = ".".join(module_name.split(os.path.sep))
                        filepath = os.path.join(path, module_path)

                        module = filepath[len(path)+1:filepath.rindex(".")].replace(os.path.sep, ".")

                        if os.path.abspath(self.__module_paths) in path:
                            modules[namespace] = "drozer.modules." + module
                        else:
                            modules[namespace] = module

        return modules

    def __module_path(self):
        """
        Calculate the full set of module paths, by combining internal paths with
        those specified in the DROZER_MODULE_PATH environment variable.
        """

        return self.__module_paths + ":" + Repository.drozer_modules_path()
        
    def __paths(self):
        """
        Form a collection of file system paths to search for drozer Modules,
        by dissecting the search paths and collecting folders that exist.

        We also add these locations to the PYTHONPATH so we can load Python
        modules from them.
        """

        paths = []

        for p in self.__module_path().split(":"):
            path = os.path.abspath(p)

            if path not in sys.path:
                sys.path.append(path)

            if p != "" and os.path.exists(path) and os.path.isdir(path):
                paths.append(path)

        return paths

    def __subclasses_of(self, klass):
        """
        Method to recursively find subclasses of a given class, used to collate
        the list of drozer Modules after loading all Python modules from the
        specified paths.
        """
        
        for i in klass.__subclasses__():
            for c in self.__subclasses_of(i):
                yield c
                
        yield klass
