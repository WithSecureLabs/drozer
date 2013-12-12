from drozer.modules import common, Module

class BusyBox(Module, common.BusyBox, common.Shell):

    name = "Install Busybox."
    description = """Installs Busybox on the Agent.

Busybox provides a number of *nix utilities that are missing from Android. Some modules require Busybox to be installed.

Typically, you require root access to the device to install Busybox. drozer can install it from its restrictive context. You can then use 'busybox' in the when executing shell commands from drozer to use it."""
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-12-12"
    license = "BSD (3 clause)"
    path = ["tools", "setup"]

    def execute(self, arguments):
        if self.isBusyBoxInstalled():
            self.stdout.write("BusyBox is already installed.\n")
        else:
            # ARCH check
            if "ARM" not in str(self.klass('java.lang.System').getProperty("os.arch")).upper():
                response = raw_input("[-] Unsupported CPU architecture - ARM only. Continue anyway (y/n)? ")
                if "Y" not in response.upper():
                    return

            if self.installBusyBox():
                self.stdout.write("BusyBox installed.\n")
            else:
                self.stdout.write("BusyBox installation failed.\n")
