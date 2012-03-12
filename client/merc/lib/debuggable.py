#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd

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
List debuggable apps on the device with optional filter
usage: info [--filter <filter>]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("debuggable", "info", {'filter':splitargs.filter} if splitargs.filter else None).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass
