


class Platform(object):
    """
    Methods for identifying platform information
    """

    def getArchitecture(self):
        """
        Get device architecture
        """

        return self.klass('java.lang.System').getProperty("os.arch").upper()

    def isPIE(self):
        """
        Is PIE enforced on the device
        """

        if self.klass("android.os.Build$VERSION").SDK_INT >= 21:
            return True
        else:
            return False

    def getBuildVersion(self):
        """
        Get Android Device Version
        """

        return self.klass("android.os.Build$VERSION").SDK_INT