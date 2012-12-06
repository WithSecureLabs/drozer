import argparse

from mwr.droidhg.repoman.repositories import Repository

class Manager(object):
    """
    mercury module [command]
    
    Run the Mercury Module and Repository Manager.

    The Repository Manager handles Mercury modules and module repositories.
    """

    def __init__(self):
        self.__parser = argparse.ArgumentParser(description=self.__doc__.strip())
        self.__parser.add_argument("command", default=None,
            help="the command to execute, try `commands` to see all available")
        self.__server = None

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
    
    def do_list(self, arguments):
        """list all installed modules, and their path"""
        
    def do_remote(self, arguments):
        """manage the source repositories, from which you install modules"""
        
    def do_repository(self, arguments):
        """manage module repositories, on your local system"""
        
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
        
        print "Remote repositories:"
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
