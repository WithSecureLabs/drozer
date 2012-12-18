import argparse
import sys

class Base(object):

    def __init__(self):
        self._parser = argparse.ArgumentParser(description="\n".join(self.__doc__.strip().split("\n")[1:]), usage=self.__doc__.strip().split("\n")[0])
        self._parser.add_argument("command", default=None,
            help="the command to execute, try `commands` to see all available")
        
        self._parser.error = self.__parse_error

    def run(self, argv=None):
        """
        Run is the main entry point of the console, called by the runtime. It
        parses the command-line arguments, and invokes an appropriate handler.
        """

        if argv == None:
            argv = []

        arguments = self._parser.parse_args(argv)

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
        
    def __parse_error(self, message):
        self.__showUsage(message)
        
        sys.exit(-1)
            
    def __showUsage(self, message):
        """
        Print usage information.
        """

        if message != None:
            print "error:", message
        print self._parser.format_help()
        
        
class UsageError(Exception):
    """
    UsageError exception is thrown if an invalid set of parameters is passed
    to a console method, through __invokeCommand().
    """

    pass