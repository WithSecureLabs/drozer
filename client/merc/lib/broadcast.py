#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd
from common import intentDictionary

class Broadcast(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#broadcast> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_info(self, args):
        """
Get information about exported broadcast receivers
usage: info [--filter <filter>]

Note: it is possible to use -f instead of --filter as shorthand

--------------------------------
Example - finding which broadcast receivers have the word "bluetooth" in them
--------------------------------
*mercury#broadcast> info -f bluetooth

Package name: com.android.bluetooth
Receiver: com.android.bluetooth.opp.BluetoothOppReceiver

Package name: com.android.bluetooth
Receiver: com.android.bluetooth.pbap.BluetoothPbapReceiver

Package name: com.android.settings
Receiver: com.android.settings.bluetooth.DockEventReceiver

Package name: com.android.settings
Receiver: com.android.settings.bluetooth.BluetoothPairingRequest

Package name: com.android.settings
Receiver: com.android.settings.bluetooth.BluetoothPermissionRequest
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("broadcast", "info", {'filter':splitargs.filter} if splitargs.filter else None).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_send(self, args):
        """
Send a broadcast with the formulated intent.
usage: send [--action <action>] [--category <category> [<category> ...]]
            [--component package class] [--data <data>]
            [--flags <0x...>] [--mimetype <mimetype>]
            [--extraboolean key=value [key=value ...]]
            [--extrabyte key=value [key=value ...]]
            [--extradouble key=value [key=value ...]]
            [--extrafloat key=value [key=value ...]]
            [--extrainteger key=value [key=value ...]]
            [--extralong key=value [key=value ...]]
            [--extraserializable key=value [key=value ...]]
            [--extrashort key=value [key=value ...]]
            [--extrastring key=value [key=value ...]]
            
--------------------------------
Example - sending a BOOT_COMPLETED broadcast that we do not have the permissions for
--------------------------------
*mercury#broadcast> send --action android.intent.action.BOOT_COMPLETED

Permission Denial: not allowed to send broadcast android.intent.action.BOOT_COMPLETED from pid=1828, uid=10116
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'send', add_help = False)
        parser.add_argument('--action', '-a', metavar = '<action>')
        parser.add_argument('--category', '-c', nargs = '+', metavar = '<category>')
        parser.add_argument('--component', '-co', nargs = 2, metavar = ('package', 'class'))
        parser.add_argument('--data', '-d', metavar = '<data>')
        parser.add_argument('--flags', '-f', metavar = '<0x...>')
        parser.add_argument('--mimetype', '-dt', metavar = '<mimetype>')
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

            print self.session.executeCommand("broadcast", "send", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def complete_send(self, _text, line, _begidx, _endidx):

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
