import argparse
import os
import sys
import time

from mwr.common import console
from mwr.common.text import wrap
from mwr.droidhg.reflection import ReflectedType
from mwr.droidhg.repoman import Repository

class ImportConflictResolver(object):
    """
    The ImportConflictResolver defines rules that can be applied to determine which
    module to keep in the event that two-or-more modules try to register the same
    name.
    """
    
    def resolve(self, existing, new):
        """
        resolve() accepts two modules, the existing module and the new module. It decides
        which to keep, and returns that module. 
        """
        
        if new.__name__ != existing.__name__ or new.__module__ != existing.__module__:
            # the klasses do not refer to the same type; we prefer standard  modules
            # over extensions and newer modules over old
            if new.__module__.startswith("mwr.droidhg.modules.") and not existing.__module__.startswith("mwr.droidhg.modules."):
                replace = True
            elif existing.__module__.startswith("mwr.droidhg.modules.") and not new.__module__.startswith("mwr.droidhg.modules."):
                replace = False
            elif time.strptime(existing.date, "%Y-%m-%d") < time.strptime(new.date, "%Y-%m-%d"):
                replace = True
            else:
                replace = False
            
            # at this point, we should have decided whether we want to replace the module
            # or not
            if replace:
                sys.stderr.write("Import Conflict: more than one definition for %s. Replacing %s with %s.\n" % (new.fqmn() , existing, new))
                
                return new
            else:
                sys.stderr.write("Import Conflict: more than one definition for %s. Keeping %s.\n" % (new.fqmn(), existing))
                
                return existing
        else:
            # both klasses refer to the same type, just have different class
            # handles for some reason: we probably loaded a .py and a .pyc
            return existing
        
        
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
            self.load(base)

        return sorted(self.__modules.keys())

    def get(self, base, key):
        """
        Gets a module implementation, given its identifier.
        """

        if(len(self.__modules) == 0):
            self.load(base)
        
        return self.__modules[key]

    def load(self, base):
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

    def __import_modules(self, modules):
        """
        Import all modules, given a collection of Python modules.
        """

        for i in modules.keys():
            if modules[i] is not None:
                try:
                    __import__(modules[i])
                    # Reload the module in case the source has changed. We don't
                    # need to be careful over i, because the import must have
                    # been successful to get here.
                    if modules[i] in sys.modules:
                        reload(sys.modules[modules[i]])
                except ImportError:
                    sys.stderr.write("Skipping source file at %s. Unable to load Python module.\n" % modules[i])

    def __locate(self):
        """
        Search the module paths for Python modules, which may contain Mercury
        modules, and build a collection of Python modules to load.
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
                            modules[namespace] = "mwr.droidhg.modules." + module
                        else:
                            modules[namespace] = module

        return modules

    def __module_path(self):
        """
        Calculate the full set of module paths, by combining internal paths with
        those specified in the DROIDHG_MODULE_PATH environment variable.
        """

        return self.__module_paths + ":" + Repository.droidhg_modules_path()
        
    def __paths(self):
        """
        Form a collection of file system paths to search for Mercury modules,
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
        the list of Mercury modules after loading all Python modules from the
        specified paths.
        """
        
        for i in klass.__subclasses__():
            for c in self.__subclasses_of(i):
                yield c
                
        yield klass


class Module(object):
    """
    Module is the base class for all Mercury modules.

    It provides base services, including initializing your module and access to
    the reflector.
    """

    name = "Un-named Module"
    description = ""
    examples = ""
    author = "Unspecified"
    date = "1970-01-01"
    license = "Unspecified"
    path = []

    __klasses = {}
    __loader = ModuleLoader()

    def __init__(self, reflector, stdout, stderr):
        self.__reflector = reflector
        self.stdout = stdout
        self.stderr = stderr

    def add_arguments(self, parser):
        """
        Stub Method: override this in a module to add commandline options to the
        internal ArgumentParser instance.
        """

        pass

    @classmethod
    def all(cls):
        """
        Loads all modules from the specified module repositories, and returns a
        collection of module identifiers.
        """

        return cls.__loader.all(cls)

    def arg(self, native, obj_type=None):
        """
        Utility method to build a ReflectedType from a native value.

        This should be used to force an object to assume a particular data type
        in Java.
        """

        return ReflectedType.fromNative(native, reflector=self.__reflector, obj_type=obj_type)

    def clearObjectStore(self):
        """
        Removes all stored objects from the remote ObjectStore.

        This invalidates all cached object references.
        """

        Module.__klasses = {}

        self.__reflector.deleteAll()

    def complete(self, text, line, begidx, endidx):
        """
        Stub Method: override this in a module to add command auto-completion
        to the module.
        """

        pass

    @classmethod
    def fqmn(cls):
        """
        Gets the fully-qualified module name, i.e., '.full.path.to.my.module'
        """

        return ".".join(cls.path + [cls.__name__.lower()])

    @classmethod
    def get(cls, key):
        """
        Gets a module implementation, given its identifier.
        """

        return cls.__loader.get(cls, key)

    def getContext(self):
        """
        Gets the context of the running Agent application.
        """

        return self.klass('com.mwr.droidhg.Agent').getContext()

    def klass(self, class_name):
        """
        Resolves a class name, and returns an object reference for the class.
        """

        if not class_name in Module.__klasses:
            Module.__klasses[class_name] = self.__reflector.resolve(class_name)
        
        return Module.__klasses[class_name]

    @classmethod
    def namespace(cls):
        """
        Get the namespace of the module, i.e., 'full.path.to.my' without '.module'
        """

        return ".".join(cls.path)

    def new(self, class_or_class_name, *args):
        """
        Instantiate a Java class, either by name or with a class reference.
        """

        if(isinstance(class_or_class_name, ReflectedType)):
            klass = class_or_class_name
        else:
            klass = self.klass(class_or_class_name)

        return self.__reflector.construct(klass, *map(lambda arg: self.arg(arg), args))

    def reflector(self):
        """
        Get the internal Reflector instance in use.
        """

        return self.__reflector
    
    @classmethod
    def reload(cls):
        """
        Reload all modules.
        """
        
        cls.__loader.load(cls)
        
    def run(self, args):
        """
        Entry point for running a module.

        This method prepare the ArgumentParser object, before invoking the
        custom execute() method, and cleaning up instantiated objects.
        """

        parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)

        parser.error = self.__parse_error

        parser.add_argument("-h", "--help", action="store_true", dest="help", default=False)

        self.add_arguments(parser)

        parser.description = self.__description(parser)
        parser.usage = self.__usage(parser)
        
        arguments = parser.parse_args(args)

        if(arguments.help):
            return parser.print_help()
        else:
            if hasattr(self, 'execute'):
                result = self.execute(arguments)
            else:
                self.stderr.write("Mercury doesn't know how to do that :(\n")
                self.stderr.write("The %s module does not define an execute() method.\n\n" % self.fqmn())
                
                result = None
                
            self.clearObjectStore()

            return result

    def __description(self, parser):
        """
        Get the description of the module, for inclusion in usage information.
        """

        description = self.__class__.description + "\n\n"
        description = description + "Examples:\n" + self.__class__.examples + "\n\n"
        description = description + "Last Modified: " + self.__class__.date + "\n"
        if isinstance(self.__class__.author, str):
            description = description + "Credit: " + self.__class__.author + "\n"
        else:
            description = description + "Credit: " + ", ".join(self.__class__.author) + "\n"
        description = description + "License: " + self.__class__.license + "\n\n"

        return wrap(description, width=console.get_size()[0])

    def __parse_error(self, message):
        """
        Error handler for the ArgumentParser instance, to override its default
        behaviour, and escalate the error to a point where we can handle it
        properly.
        """

        raise Exception(message)

    def __usage(self, parser):
        """
        Get usage information about the Module.
        """

        return "run {} {}\n\n".format(self.__class__.fqmn(), " ".join(parser.format_usage().split(" ")[2:]))
        