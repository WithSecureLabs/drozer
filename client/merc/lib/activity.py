#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd
from common import intentDictionary

class Activity(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#activity> "

    def do_back(self, _args):
        """Return to main menu\n"""
        return -1

    def do_start(self, args):
        """
Start an activity with an intent
usage: start [--action <action>] [--category <category> [<category> ...]]
             [--component package class] [--data <data>]
             [--flags <0x...>] [--mimetype <mime_type>]
             [--extraboolean key=value [key=value ...]]
             [--extrabyte key=value [key=value ...]]
             [--extradouble key=value [key=value ...]]
             [--extrafloat key=value [key=value ...]]
             [--extrainteger key=value [key=value ...]]
             [--extralong key=value [key=value ...]]
             [--extraserializable key=value [key=value ...]]
             [--extrashort key=value [key=value ...]]
             [--extrastring key=value [key=value ...]]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'start', add_help = False)
        parser.add_argument('--action', '-a', metavar = '<action>')
        parser.add_argument('--category', '-c', nargs = '+', metavar = '<category>')
        parser.add_argument('--component', '-co', nargs = 2, metavar = ('package', 'class'))
        parser.add_argument('--data', '-d', metavar = '<data>')
        parser.add_argument('--flags', '-f', metavar = '<0x...>')
        parser.add_argument('--mimetype', '-dt', metavar = '<mime_type>')
        parser.add_argument('--extraboolean', '-eb', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrabyte', '-eby', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extradouble', '-ed', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrafloat', '-ef', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrainteger', '-ei', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extralong', '-el', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extraserializable', '-ese', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrashort', '-esh', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrastring', '-es', nargs = '+', metavar = 'key=value')


        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            if (splitargs.component):
                request['component'] = splitargs.component[0] + "=" + splitargs.component[1]

            if (splitargs.flags):
                request['flags'] = str(int(splitargs.flags, 0))

            print self.session.executeCommand("activity", "start", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass


    def complete_start(self, _text, line, _begidx, _endidx):

        # Split arguments using shlex
        splitargs = shlex.split(line)

        # Autocompletion of different intents
        if splitargs[-1]:
            return [
                intent for intent in sorted(intentDictionary.itervalues())
                if intent.startswith(splitargs[-1])
            ]
        else:
            return sorted(intentDictionary.itervalues())





    def do_match(self, args):
        """
Find which apps can handle the given intent
usage: match [--action <action>] [--category <category> [<category> ...]]
             [--component package class] [--data <data>]
             [--flags <0x...>] [--mimetype <mime_type>]
             [--extraboolean key=value [key=value ...]]
             [--extrabyte key=value [key=value ...]]
             [--extradouble key=value [key=value ...]]
             [--extrafloat key=value [key=value ...]]
             [--extrainteger key=value [key=value ...]]
             [--extralong key=value [key=value ...]]
             [--extraserializable key=value [key=value ...]]
             [--extrashort key=value [key=value ...]]
             [--extrastring key=value [key=value ...]]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'start', add_help = False)
        parser.add_argument('--action', '-a', metavar = '<action>')
        parser.add_argument('--category', '-c', nargs = '+', metavar = '<category>')
        parser.add_argument('--component', '-co', nargs = 2, metavar = ('package', 'class'))
        parser.add_argument('--data', '-d', metavar = '<data>')
        parser.add_argument('--flags', '-f', metavar = '<0x...>')
        parser.add_argument('--mimetype', '-dt', metavar = '<mime_type>')
        parser.add_argument('--extraboolean', '-eb', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrabyte', '-eby', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extradouble', '-ed', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrafloat', '-ef', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrainteger', '-ei', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extralong', '-el', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extraserializable', '-ese', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrashort', '-esh', nargs = '+', metavar = 'key=value')
        parser.add_argument('--extrastring', '-es', nargs = '+', metavar = 'key=value')


        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            if (splitargs.component):
                request['component'] = splitargs.component[0] + "=" + splitargs.component[1]

            if (splitargs.flags):
                request['flags'] = str(int(splitargs.flags, 0))

            print self.session.executeCommand("activity", "match", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass


    def complete_match(self, _text, line, _begidx, _endidx):

        # Split arguments using shlex
        splitargs = shlex.split(line)

        # Autocompletion of different intents
        if splitargs[-1]:
            return [
                intent for intent in sorted(intentDictionary.itervalues())
                if intent.startswith(splitargs[-1])
            ]
        else:
            return sorted(intentDictionary.itervalues())


    def do_info(self, args):
        """
Get information about exported activities
usage: info [--filter <filter>]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("activity", "info", {'filter':splitargs.filter} if splitargs.filter else None).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_launchintent(self, args):
        """
Get the launch intent of the given package
usage: launchintent packageName
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'launchintent', add_help = False)
        parser.add_argument('packageName')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("activity", "launchintent", {'packageName':splitargs.packageName}).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

