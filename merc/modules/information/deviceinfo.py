from merc.lib.modules import Module

class DeviceInfo(Module):
    """Description: Use different methods to get device information
Credit: Tyrone Erasmus - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]

    def execute(self, session, _arg):

        print "-----------------------------------------"
        print "/proc/version"
        print "-----------------------------------------"
        print session.executeCommand("shell", "executeSingleCommand", {'args':'cat /proc/version'}).getPaddedErrorOrData()

        print "-----------------------------------------"
        print "/system/build.prop"
        print "-----------------------------------------"
        print session.executeCommand("shell", "executeSingleCommand", {'args':'cat /system/build.prop'}).getPaddedErrorOrData()


        print "-----------------------------------------"
        print "getprop"
        print "-----------------------------------------"
        print session.executeCommand("shell", "executeSingleCommand", {'args':'getprop'}).getPaddedErrorOrData()
