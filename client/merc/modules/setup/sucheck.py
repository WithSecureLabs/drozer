import os

from merc.lib.modules import Module

class sucheck(Module):
    """Description: Test if SU binary works on device
Credit: Tyrone Erasmus - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["setup"]

    def execute(self, session, _arg):
 
        session.executeCommand("shell", "executeMercuryShell", {'args':'su'})
        print "\n--------------<mercury_shell>--------------"
        print session.executeCommand("shell", "readMercuryShell", None).getPaddedErrorOrData()
        print "--------------</mercury_shell>-------------\n"
        print "If this was successful there will be a root shell waiting for you in shell->persistent\n"
