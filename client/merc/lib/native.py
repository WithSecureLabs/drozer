#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd

class Native(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#native> "

    def do_back(self, _args):
        """
Return to menu
        """
        return -1

    def do_info(self, args):
        """
Show information about apps on the device containing native code with optional filter
usage: info [--filter <filter>]

Note: it is possible to use -f instead of --filter as shorthand
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            response = self.session.executeCommand("native", "info", {'filter':splitargs.filter} if splitargs.filter else None).getPaddedErrorOrData()

            if response.strip() == "":
                print "\nNo applications found containing native code\n"
            else:
                print response

        # FIXME: Choose specific exceptions to catch
        except:
            pass
