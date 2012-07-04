#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex
from interface import BaseCmd, BaseArgumentParser

class Debuggable(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#debuggable> "

    def do_back(self, _args):
        """
Return to menu
        """
        return -1

    def do_info(self, args):
        """
Show information about debuggable apps on the device with optional filter
usage: info [--filter <filter>] [--output <filename>]

Note: it is possible to use -f instead of --filter as shorthand
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        
        parser.setOutputToFileOption()

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            response = self.session.executeCommand("debuggable", "info", {'filter':splitargs.filter} if splitargs.filter else None).getPaddedErrorOrData()

            if response.strip() == "":
                print "\nNo debuggable applications found\n"
            else:
                print response

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass
