#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import sys
import cmd
import argparse
from common import FileWriter

class BaseCmd(cmd.Cmd):

    def __init__(self, session):
        cmd.Cmd.__init__(self)
        self.session = session
        self.ruler = "-"
        self.doc_header = "Commands - type help <command> for more info"

        self._hist = []      ## No history yet
        self._locals = {}      ## Initialize execution namespace for user
        self._globals = {}

    ## Command definitions to support Cmd object functionality ##
    def do_help(self, args):
        """
'help <command>' or '? <command>' gives help on <command>

For usage instructions on a command, type <command> -h or <command> --help
        """
        ## The only reason to define this method is for the help text in the doc string
        cmd.Cmd.do_help(self, args)

    ## Command definition to support quitting in any function ##
    def do_exit(self, _args):
        """
'exit quits mercury'
        """
        # Leave immediately, do not pass go, do not collect $200
        sys.exit(0)

    ## Override methods in Cmd object ##
    def preloop(self):
        """
Initialization before prompting user for commands.
Despite the claims in the Cmd documentaion, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   ## sets up command completion
        self._hist = []      ## No history yet
        self._locals = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """
Take care of any unfinished business.
Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   ## Clean up command completion

    def precmd(self, line):
        """
This method is called after the line has been input but before
it has been interpreted. If you want to modifdy the input line
before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """
If you want to stop the console, return something that evaluates to true.
If you want to do some post command processing, do it here.
        """
        # After the command is executed, redirect the output stream to the standard
        sys.stdout = sys.__stdout__
        return stop

    def emptyline(self):
        """
Do nothing on empty input line
        """
        pass

    def default(self, line):
        """
Called on an input line when the command prefix is not recognized.
        """
        print "Command not found\n"
        
        
class BaseArgumentParser(object):
    """
Class to replace "argparse.ArgumentParser" in order to enable user to save
an output of a command to a file
Added by Luander <luander.r@samsung.com>
    """
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser(**kwargs)
        self.outputToFileOption = False

    def add_argument(self, *args, **kwargs):
        """
add_argument(dest, ..., name=value, ...)
add_argument(option_string, option_string, ..., name=value, ...)
        """
        self.parser.add_argument(*args, **kwargs)
        
    def setOutputToFileOption(self):
        """
Enable the option to output the result of this command to a file
        """
        self.outputToFileOption = True

    def parse_args(self, args=None):
        """
Command line argument parsing methods
        """

        # Adds an argument to output to a file
        if self.outputToFileOption:
            self.parser.add_argument('--output', '-o', metavar = '<file>')
        
        # If an argument with a help indicator comes in then display usage
        if (("-h" in args) or ("--help" in args)):
            print ""
            self.parser.print_usage(None)
            print ""
            return None
        
        try:
            arguments = self.parser.parse_args(args)
            
            # If the (--output, -o) argument is set, then save the output to a specified file
            if arguments.output:
                sys.stdout = FileWriter(arguments.output)
                
        except:
            arguments = None

        return arguments
    

