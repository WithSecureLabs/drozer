import argparse
import textwrap
import sys

from mwr.common import console

class Base(object):
    """
    cli.Base provides a simple command-line environment, where numerous different
    commands can be invoked.
    """

    def __init__(self):
        doc_text = textwrap.dedent(self.__doc__).strip().split("\n")
        
        self._parser = argparse.ArgumentParser(description="\n".join(doc_text[1:]), usage=doc_text[0])
        self._parser.add_argument("command", default=None,
            help="the command to execute")
        
        self._parser.epilog = "available commands:\n%s" % self.__get_commands_help()
        self._parser.error = self.__parse_error
        self._parser.formatter_class = argparse.RawDescriptionHelpFormatter

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

        print "usage:", self.__doc__.strip()
        print
        print "available commands:"
        print self.__get_commands_help()

    def __commands(self):
        """
        Get a list of supported commands to console, by searching for any
        method beginning with do_.
        """

        return filter(lambda f: f.startswith("do_") and\
            getattr(self, f).__doc__ is not None, dir(self))
    
    def __get_commands_help(self):
        """
        Produce a piece of text, containing the available commands, and their short
        description.
        """
        
        commands = {}
        
        for command in self.__commands():
            commands[command.replace("do_", "")] = getattr(self, command).__doc__.strip()
            
        return console.format_dict(commands, left_margin=2)

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