import os

from merc.lib.modules import Module

class Busybox(Module):
    """Description: Upload busybox to the device
Credit: Tyrone Erasmus - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["setup"]

    def execute(self, session, _arg):

        # busybox binary placed in tools directory
        localBB = os.path.join(os.path.dirname(__file__) , "..", "..", "..", "tools", "busybox")

        print "\n[*] Uploading busybox"
        upload = session.uploadFile(localBB, "/data/data/com.mwr.mercury")

        if upload.isError():
            print "[-] Failed: " + upload.error + "\n"
        else:
            print "[+] Succeeded"
            print "[*] chmod 770 busybox\n"
            session.executeCommand("shell", "executeSingleCommand", {'args':'chmod 770 /data/data/com.mwr.mercury/busybox'})

