#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd

class Packages(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#packages> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_info(self, args):
        """
List all installed packages on the device with optional filter
usage: info [--filter <filter>] [--permissions <filter>]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        parser.add_argument('--permissions', '-p', metavar = '<filter>')


        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("packages", "info", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_shareduid(self, args):
        """
Get packages with the same uid with optional filter
usage: shareduid [--uid <uid>]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'shareduid', add_help = False)
        parser.add_argument('--uid', '-u', metavar = '<uid>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("packages", "shareduid", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_attacksurface(self, args):
        """
Examine the attack surface of the given package
usage: attacksurface packageName
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'attacksurface', add_help = False)
        parser.add_argument('packageName')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("packages", "attacksurface", {'packageName':splitargs.packageName}).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass
