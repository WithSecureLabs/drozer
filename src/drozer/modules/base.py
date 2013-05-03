import argparse

from pydiesel.reflection.types import ReflectedType

from mwr.common import argparse_completer, console
from mwr.common.text import wrap

from drozer.modules.loader import ModuleLoader

class Module(object):
    """
    Module is the base class for all drozer Modules.

    It provides base services, including initializing your module and access to
    the reflector.
    """

    name = "drozer Module"
    description = ""
    examples = ""
    author = "Unspecified"
    date = "1970-01-01"
    license = "Unspecified"
    path = []
    permissions = []
    
    push_completer = None
    pop_completer = None

    __klasses = {}
    __loader = ModuleLoader()

    def __init__(self, session):
        self.__reflector = session.get_reflector()
        self.stdout = session.stdout
        self.stderr = session.stderr
        self.variables = session.variables

    def add_arguments(self, parser):
        """
        Stub Method: override this in a module to add command-line options to the
        internal ArgumentParser instance.
        """

        pass

    @classmethod
    def all(cls, permissions=None):
        """
        Loads all modules from the specified module repositories, and returns a
        collection of module identifiers.
        """

        return cls.__loader.all(cls, permissions)

    def arg(self, native, obj_type=None):
        """
        Utility method to build a ReflectedType from a native value.

        This should be used to force an object to assume a particular data type
        in Java.
        """

        return ReflectedType.fromNative(native, reflector=self.__reflector, obj_type=obj_type)
    
    @classmethod
    def cache_klass(cls, klass, ref):
        """
        Store a reflected Class reference in the cache of classes.
        """
        
        Module.__klasses[klass] = ref
    
    @classmethod
    def cached_klass(cls, klass):
        """
        True, if there is a reflected Class reference stored in the cache of classes.
        """
        
        return klass in Module.__klasses

    def clearObjectStore(self):
        """
        Removes all stored objects from the remote ObjectStore.

        This invalidates all cached object references.
        """

        Module.__klasses = {}

        self.__reflector.deleteAll()

    def complete(self, text, line, begidx, endidx):
        """
        Intercept all readline completion requests for argument strings, and delegate
        them to the ArgumentParserCompleter to get suitable suggestions.
        """
        
        return argparse_completer\
            .ArgumentParserCompleter(self.__prepare_parser(), self)\
            .get_suggestions(text, line, begidx, endidx)

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
    
    @classmethod
    def get_cached_klass(cls, klass):
        """
        Retrieve a reflected class reference from the cache of classes.
        """
        
        return Module.__klasses[klass]
    
    def get_completion_suggestions(self, action, text, **kwargs):
        """
        Stub Method: invoked during completion of module arguments, to allow the module
        to provide suggestions.
        """
        
        pass

    def getContext(self):
        """
        Gets the context of the running Agent application.
        """

        return self.klass('com.mwr.droidhg.Agent').getContext()

    def klass(self, class_name):
        """
        Resolves a class name, and returns an object reference for the class.
        """

        if not Module.cached_klass(class_name):
            Module.cache_klass(class_name, self.__reflector.resolve(class_name))
        
        return Module.get_cached_klass(class_name)

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

    def null_complete(self, text, state):
        return None
    
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

        parser = self.__prepare_parser()

        parser.description = self.__description()
        parser.usage = self.__usage(parser)

        if "-h" in args or "--help" in args:
            return parser.print_help()
        else:
            arguments = parser.parse_args(args)
            
            if hasattr(self, 'execute'):
                result = self.execute(arguments)
            else:
                self.stderr.write("drozer doesn't know how to do that.\n")
                self.stderr.write("The %s module does not define an execute() method.\n\n" % self.fqmn())
                
                result = None
                
            self.clearObjectStore()

            return result

    def __description(self):
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
    
    def __prepare_parser(self):
        """
        Build an argparse.ArgumentParser for this Module.
        """
        
        parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.RawTextHelpFormatter)

        parser.error = self.__parse_error

        parser.add_argument("-h", "--help", action="store_true", dest="help", default=False)

        self.add_arguments(parser)
        
        return parser
    
    def __usage(self, parser):
        """
        Get usage information about the Module.
        """

        return "run {} {}\n\n".format(self.__class__.fqmn(), " ".join(parser.format_usage().split(" ")[2:]))
        