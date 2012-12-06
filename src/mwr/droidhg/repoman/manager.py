import argparse

from mwr.common import console
from mwr.common.text import wrap
from mwr.droidhg.repoman.installer import ModuleInstaller
from mwr.droidhg.repoman.repositories import Repository, NotEmptyException, UnknownRepository

class ModuleManager(object):
    """
    mercury module [command]
    
    Run the Mercury Module and Repository Manager.

    The Repository Manager handles Mercury modules and module repositories.
    """

    def __init__(self):
        self.__parser = argparse.ArgumentParser(description=self.__doc__.strip())
        self.__parser.add_argument("command", default=None,
            help="the command to execute, try `commands` to see all available")
        self.__parser.add_argument("options", nargs='*')

    def run(self, argv=None):
        """
        Run is the main entry point of the console, called by the runtime. It
        parses the command-line arguments, and invokes an appropriate handler.
        """

        if argv == None:
            argv = []

        arguments = self.__parser.parse_args(argv)

        try:
            self.__invokeCommand(arguments)
        except UsageError as e:
            self.__showUsage(e.message)

    def do_commands(self, arguments):
        """shows a list of all console commands"""

        print "Usage:", self.__doc__.strip()
        print
        print "Commands:"
        for command in self.__commands():
            print "  {:<15}  {}".format(command.replace("do_", ""),
                getattr(self, command).__doc__.strip())
        print
        
    def do_install(self, arguments):
        """install a new module"""
        
        repository = self.__choose_repo()
        
        if repository != None:
            installer = ModuleInstaller(repository)
            modules = installer.install(arguments.options)
                        
            print
            print "Successfully installed %d modules." % len(modules['success'])
            print "Failed to install %d:" % len(modules['fail'])
            for module in modules['fail']:
                print "  %s" % module
            print
            
    def do_list(self, arguments):
        """list all installed modules, and their path"""
        
        self.__list_modules()
        
    def do_remote(self, arguments):
        """manage the source repositories, from which you install modules"""
        
    def do_repository(self, arguments):
        """manage module repositories, on your local system"""
        
        RepositoryManager().run(arguments.options)
    
    def __choose_repo(self):
        """
        Return the path of a repository, either the only repo or presenting the user
        with a choice.
        """
        
        repositories = Repository.all()
        
        if len(repositories) == 1:
            return repositories[0]
        elif len(repositories) == 0:
            print "You do not have a Mercury module repository. Please create one, then try again."
            
            return None
        else:
            print "You have %d Mercury module repositories. Which would you like to install into?\n" % len(repositories)
            for i in range(len(repositories)):
                print "  %5d  %s" % (i+1, repositories[i])
            print
            
            while(True):
                print "repo>",
                try:
                    idx = int(raw_input().strip())
                
                    if idx >= 1 and idx <= len(repositories):
                        print
                        
                        return repositories[idx-1]
                    else:
                        raise ValueError(idx)
                except ValueError:
                    print "Not a valid selection. Please enter a number between 1 and %d." % len(repositories)

    def __commands(self):
        """
        Get a list of supported commands to console, by searching for any
        method beginning with do_.
        """

        return filter(lambda f: f.startswith("do_") and\
            getattr(self, f).__doc__ is not None, dir(self))

    def __invokeCommand(self, arguments):
        """
        Execute a console command, given the command-line arguments.
        """

        try:
            command = arguments.command

            if "do_" + command in dir(self):
                getattr(self, "do_" + command)(arguments)
            else:
                raise UsageError("unknown command: " + command)
        except IndexError:
            raise UsageError("incorrect usage")
    
    def __list_modules(self):
        """
        Get a list of all loaded modules.
        """
        
        from mwr.droidhg.modules.base import Module
        
        width = { 'gutter': 2, 'total': console.getSize()[0] }
        width['label'] = width['total'] / 3
        width['desc'] = width['total'] - (width['gutter'] + width['label'])

        for module in Module.all():
            name = wrap(Module.get(module).name, width['desc']).split("\n")

            if len(module) > width['label']:
                print ("%%-%ds" % width['label']) % module 
                print ("%%-%ds  %%-%ds" % (width['label'], width['desc'])) % ("", name.pop(0))
            else:
                print ("%%-%ds  %%-%ds" % (width['label'], width['desc'])) % (module, name.pop(0))

            for line in name:
                print ("%%-%ds  %%-%ds" % (width['label'], width['desc'])) % ("", line)
        
    def __showUsage(self, message):
        """
        Print usage information.
        """

        print "console:", message
        print
        print self.__parser.format_help()

class RepositoryManager(object):
    """
    mercury module repository [command]
    
    Run the repository part of the Mercury Module and Repository Manager.

    The Repository Manager handles Mercury modules and module repositories.
    """

    def __init__(self):
        self.__parser = argparse.ArgumentParser(description=self.__doc__.strip())
        self.__parser.add_argument("command", default=None,
            help="the command to execute, try `commands` to see all available")
        self.__parser.add_argument("options", nargs='*')

    def run(self, argv=None):
        """
        Run is the main entry point of the console, called by the runtime. It
        parses the command-line arguments, and invokes an appropriate handler.
        """

        if argv == None:
            argv = []
        if argv == []:
            argv.append("list")

        arguments = self.__parser.parse_args(argv)

        try:
            self.__invokeCommand(arguments)
        except UsageError as e:
            self.__showUsage(e.message)

    def do_commands(self, arguments):
        """shows a list of all console commands"""

        print "Usage:", self.__doc__.strip()
        print
        print "Commands:"
        for command in self.__commands():
            print "  {:<15}  {}".format(command.replace("do_", ""),
                getattr(self, command).__doc__.strip())
        print
        
    def do_create(self, arguments):
        """create a new Mercury module repository"""
        
        if len(arguments.options) == 1:
            path = arguments.options[0]
            
            try:
                Repository.create(path)
                
                print "Initialised repository at %s.\n" % path
            except NotEmptyException:
                print "The target (%s) already exists.\n" % path
        else:
            print "usage: mercury module repository create /path/to/repository\n"
    
    def do_delete(self, arguments):
        """remove a Mercury module repository"""
        
        if len(arguments.options) == 1:
            path = arguments.options[0]
            
            try:
                Repository.delete(path)
                
                print "Removed repository at %s.\n" % path
            except UnknownRepository:
                print "The target (%s) is not a Mercury module repository.\n" % path
        else:
            print "usage: mercury module repository delete /path/to/repository\n"
                
    def do_disable(self, arguments):
        """hide a Module repository, without deleting its contents"""
        
        if len(arguments.options) == 1:
            path = arguments.options[0]
            
            try:
                Repository.disable(path)
                
                print "Hidden repository at %s.\n" % path
            except UnknownRepository:
                print "The target (%s) is not a Mercury module repository.\n" % path
        else:
            print "usage: mercury module repository disable /path/to/repository\n"
    
    def do_enable(self, arguments):
        """enable a previously disabled Module repository"""
        
        if len(arguments.options) == 1:
            path = arguments.options[0]
            
            try:
                Repository.enable(path)
                
                print "Enabled repository at %s.\n" % path
            except UnknownRepository:
                print "The target (%s) is not a Mercury module repository.\n" % path
        else:
            print "usage: mercury module repository enable /path/to/repository\n"
        
    def do_list(self, arguments):
        """list all repositories, both local and remote"""
        
        self.__list_repositories()

    def __commands(self):
        """
        Get a list of supported commands to console, by searching for any
        method beginning with do_.
        """

        return filter(lambda f: f.startswith("do_") and\
            getattr(self, f).__doc__ is not None, dir(self))

    def __invokeCommand(self, arguments):
        """
        Execute a console command, given the command-line arguments.
        """

        try:
            command = arguments.command

            if "do_" + command in dir(self):
                getattr(self, "do_" + command)(arguments)
            else:
                raise UsageError("unknown command: " + command)
        except IndexError:
            raise UsageError("incorrect usage")
        
    def __list_repositories(self):
        """
        Print a list of Mercury repositories (a) on the local system, and
        (b) registered as remotes.
        """
        
        print "Local repositories:"
        for repo in Repository.all():
            print "  %s" % repo
        print

    def __showUsage(self, message):
        """
        Print usage information.
        """

        print "console:", message
        print
        print self.__parser.format_help()

class UsageError(Exception):
    """
    UsageError exception is thrown if an invalid set of parameters is passed
    to a console method, through __invokeCommand().
    """

    pass
