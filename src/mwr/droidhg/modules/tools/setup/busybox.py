from mwr.droidhg.modules import common, Module

class BusyBox(Module, common.BusyBox, common.FileSystem, common.Shell):

    name = "Install Busybox."
    description = """Installs Busybox on the Agent.

Busybox provides a number of *nix utilities that are missing from Android. Some modules require Busybox to be installed.

Typically, you require root access to the device to install Busybox. Mercury can install it from its restrictive context. You can then use $BB in the when executing shell commands from Mercury to use it."""
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["tools", "setup"]

    def execute(self, arguments):
        if self.isBusyBoxInstalled():
            self.stdout.write("BusyBox is already installed.\n")
        else:
            if self.installBusyBox():
                self.stdout.write("BusyBox installed.\n")
            else:
                self.stdout.write("BusyBox installation failed.\n")
