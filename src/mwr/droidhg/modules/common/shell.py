class Shell(object):
    """
    Mercury Client Library: provides a wrapper around the Android Shell, allowing
    commands to be executed.
    """

    def shellExec(self, command):
        """
        Execute a single Shell command on the Agent.
        """

        ShellWrapper = self.loadClass("common/ShellWrapper.apk", "ShellWrapper")

        return ShellWrapper.execute(command)
