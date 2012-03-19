from merc.lib.modules import Module

class sbitbinaries(Module):
    """Description: Find all the suid/sgid binaries in the /system folder - uses method from http://hexesec.wordpress.com/2009/10/14/exploiting-suid-binaries/
Credit: Tyrone Erasmus - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]

    def execute(self, session, _arg):

        # Check if busybox exists
        if session.executeCommand("core", "fileSize", {'path':'/data/data/com.mwr.mercury/busybox'}).isError():
            print "\nRun setup.busybox first and then retry\n"
            return

        binaries = ""
        for binary in iter(session.executeCommand("shell", "executeSingleCommand", {'args':'/data/data/com.mwr.mercury/busybox find /system -type f \( -perm -04000 -o -perm -02000 \) \-exec ls {} \;'}).data.splitlines()):
            if not binary.startswith('find: '):
                binaries += binary + "\n"
                
        print "\n" + binaries.strip() + "\n"