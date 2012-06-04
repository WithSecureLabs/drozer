from merc.lib.modules import Module
from merc.lib.reflect import Reflect

class Reflection(Module):
    """Description: Get all secret codes from the Manifest
Credit: Mike Auty - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["test"]

    def execute(self, session, _args):

        r = Reflect(session)
        print r.resolve('java.lang.reflect.Method')
