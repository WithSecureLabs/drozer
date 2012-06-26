#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex, sys
from basecmd import BaseCmd
from basecmd import BaseArgumentParser

class Shell(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#shell> "
        self.use_rawinput = True

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1


    def do_persistent(self, args):
        """
Execute Linux commands in a persistent shell within the context of Mercury. The use of the word "persistent" means that a connection is maintained to the same shell session. This means that the state of the shell persists. If root were to be obtained on this shell, it would persist across the life of the shell connection.
usage: persistent [--new]
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'persistent', add_help = False)
        parser.add_argument('--new', '-n', action = 'store_const', const = True)

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            if splitargs.new:
                _newShell = self.session.executeCommand("shell", "newMercuryShell", None)


            prompt = ""
            while (prompt.upper() != "BACK"):
                _write = self.session.executeCommand("shell", "executeMercuryShell", {'args':prompt})
                read = self.session.executeCommand("shell", "readMercuryShell", None)
                sys.stdout.write(read.getErrorOrData().replace(prompt, "", 1).strip() + " ")
                prompt = raw_input().replace("$BB", "/data/data/com.mwr.mercury/busybox")

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_oneoff(self, _args):
        """
Execute Linux commands one at a time (no persistent shell is maintained) within the context of Mercury. The state of the current working directory is maintained for convenience, but this does not actually persist in the shell session.

Put in simpler terms: a command is received -> new shell session is opened -> command is executed -> reply is received -> shell session is closed
        """

        cwd = "/data/data/com.mwr.mercury"

        try:

            prompt = "echo"
            while (prompt.upper() != "BACK"):
                # When executing commands, first place user back in the same directory then execute command with trailing pwd to get cwd
                command = "cd " + cwd + ";" + prompt + ";pwd"
                
                # Check that blank input was not entered
                if len(prompt) > 0:
                
                    result = self.session.executeCommand("shell", "executeSingleCommand", {'args':command}).getErrorOrData().split("\n")
    
                    # Parse out cwd
                    if ("**Network Error**" not in result[-1]):
                        cwd = result[-1]
    
                        # Print result
                        for i in result[:-1]:
                            print i
                    else:
                        print result[-1]

                prompt = raw_input("oneoffshell:" + cwd + "$ ").replace("$BB", "/data/data/com.mwr.mercury/busybox")

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass




