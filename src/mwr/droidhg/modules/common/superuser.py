import os
from mwr.common import fs

class SuperUser(object):
    """
    Mercury Client Library: provides utility methods for aiding with superuser
    binary detection and installation of "minimal su" on the Agent.
    """

    def __agentPathMinimalSu(self):
        """
        Get the path to which su is uploaded on the Agent.
        """

        return "/data/data/com.mwr.droidhg.agent/su"

    def _localPathMinimalSu(self):
        """
        Get the path to the su binary on the local system.
        """

        return os.path.join(os.path.dirname(__file__) , "..", "tools", "setup", "minimal-su", "libs", "armeabi", "su")

    def __agentPathScript(self):
        """
        Get the path to which the install script is uploaded on the Agent.
        """

        return "/data/data/com.mwr.droidhg.agent/install-minimal-su.sh"

    def _localPathScript(self):
        """
        Get the path to the install script on the local system.
        """

        return os.path.join(os.path.dirname(__file__) , "..", "tools", "setup", "minimal-su", "install-su.sh")

    def isAnySuInstalled(self):
        """
        Test whether any su binary is installed on the Agent.
        """
        
        return (self.exists("/system/bin/su") or self.exists("/system/xbin/su"))
            
    def isMinimalSuInstalled(self):
        """
        
        Test whether the 'minimal su' binary is installed on the Agent.
        """
        
        return (self.md5sum("/system/bin/su") == fs.md5sum(self._localPathMinimalSu()))

    def uploadMinimalSu(self):
        """
        Upload minimal su to the Agent.
        """

        # Remove existing uploads of su
        self.shellExec("rm /data/data/com.mwr.droidhg.agent/su")

        bytes_copied = self.uploadFile(self._localPathMinimalSu(), self.__agentPathMinimalSu())

        if bytes_copied == os.path.getsize(self._localPathMinimalSu()):
            return True
        else:
            return False

    def uploadMinimalSuInstallScript(self):
        """
        Upload minimal su install script to the Agent.
        """

        # Remove existing uploads of su install script
        self.shellExec("rm /data/data/com.mwr.droidhg.agent/install-su.sh")

        bytes_copied = self.uploadFile(self._localPathScript(), self.__agentPathScript())

        if bytes_copied == os.path.getsize(self._localPathScript()):
            self.shellExec("chmod 770 " + self.__agentPathScript())
            return True
        else:
            return False

