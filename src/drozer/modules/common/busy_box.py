import os

from drozer.modules.common import file_system, shell

class BusyBox(shell.Shell):
    """
    Utility methods for installing and using Busybox on the Agent.
    """

    def busyboxPath(self):
        """
        Get the path to which Busybox is installed on the Agent.
        """

        return self.workingDir() + "/bin/busybox"

    def _localPath(self, pie):
        """
        Get the path to the Busybox binary on the local system.
        """
        if pie == True:
            return os.path.join(os.path.dirname(__file__) , "..", "tools", "setup", "pie", "busybox")
        else:
            return os.path.join(os.path.dirname(__file__) , "..", "tools", "setup", "nopie","busybox")


    def busyBoxExec(self, command):
        """
        Execute a command using Busybox.
        """

        return self.shellExec("%s %s" % (self.busyboxPath(), command))

    def isBusyBoxInstalled(self):
        """
        Test whether Busybox is installed on the Agent.
        """

        return self.exists(self.busyboxPath())

    def installBusyBox(self,pie):
        """
        Install Busybox on the Agent.
        """

        if self.ensureDirectory(self.busyboxPath()[0:self.busyboxPath().rindex("/")]):
            bytes_copied = self.uploadFile(self._localPath(pie), self.busyboxPath())
    
            if bytes_copied != os.path.getsize(self._localPath(pie)):
                return False
            else:
                self.shellExec("chmod 775 " + self.busyboxPath())
                
                return True
        else:
            return False
