#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

from shell import Shell
from tools import Tools
from basecmd import BaseCmd
from service import Service
from modules import Modules
from activity import Activity
from provider import Provider
from packages import Packages
from broadcast import Broadcast
from debuggable import Debuggable

class Menu(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury> "

    def do_back(self, _args):
        """
Return to home screen
        """
        return -1

    def do_activity(self, _args):
        """
Interact with exported activities on the device
        """
        subconsole = Activity(self.session)
        subconsole.cmdloop()

    def do_provider(self, _args):
        """
Interact with exported providers on the device
        """
        subconsole = Provider(self.session)
        subconsole.cmdloop()

    def do_service(self, _args):
        """
Interact with exported services on the device
        """
        subconsole = Service(self.session)
        subconsole.cmdloop()

    def do_broadcast(self, _args):
        """
Interact with broadcast receivers on the device
        """
        subconsole = Broadcast(self.session)
        subconsole.cmdloop()

    def do_modules(self, _args):
        """
Interact with custom Mercury modules
        """
        subconsole = Modules(self.session)
        subconsole.cmdloop()

    def do_shell(self, _args):
        """
Issue Linux commands using provided shells within the context of Mercury
        """
        subconsole = Shell(self.session)
        subconsole.cmdloop()

    def do_debuggable(self, _args):
        """
Interact with debuggable applications
        """
        subconsole = Debuggable(self.session)
        subconsole.cmdloop()

    def do_tools(self, _args):
        """
Make use of general purpose tools that are useful
        """
        subconsole = Tools(self.session)
        subconsole.cmdloop()

    def do_packages(self, _args):
        """
Get information about packages installed on the device
        """
        subconsole = Packages(self.session)
        subconsole.cmdloop()
