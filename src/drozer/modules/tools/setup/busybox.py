from drozer.modules import common, Module

class BusyBox(Module, common.BusyBox, common.Shell):

    name = "Install Busybox."
    description = """Installs Busybox on the Agent.
    # 09/02/2016 - Updated binary for PIE Support

Busybox provides a number of *nix utilities that are missing from Android. Some modules require Busybox to be installed.

Typically, you require root access to the device to install Busybox. drozer can install it from its restrictive context. You can then use 'busybox' in the when executing shell commands from drozer to use it."""
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-12-12"
    license = "BSD (3 clause)"
    path = ["tools", "setup"]

    def execute(self, arguments):
        arch = str(self.klass('java.lang.System').getProperty("os.arch")).upper()
        
        # Check for unsupported architecture
        if "ARM" in arch:
            arch = "arm"
        elif "86" in arch:
            arch = "x86"
        else:
            self.stdout.write("Unsupported CPU architecture. Supported architectures are arm, arm64, x86 and x86_64.\n")

        # If the arch is supported, then check if busybox is installed
        if arch == "x86":
            if self.isBusyBoxInstalled():
                self.stdout.write("BusyBox is already installed.\n")
            else:
                if self.installBusyBox(arch="x86", pie=False):
                    self.stdout.write("BusyBox installed " + self.busyboxPath() + "\n")
                else:
                    self.stdout.write("BusyBox installation failed.\n")
        elif arch == "arm":
            if self.isBusyBoxInstalled():
                self.stdout.write("BusyBox is already installed.\n")
            else:
                if self.klass("android.os.Build$VERSION").SDK_INT >= 21:
                    if self.installBusyBox(arch="arm", pie=True):
                        self.stdout.write("BusyBox installed " + self.busyboxPath() + "\n")
                    else:
                        self.stdout.write("BusyBox installation failed.\n")
                else:
                    if self.installBusyBox(arch="arm",pie=False):
                        self.stdout.write("BusyBox installed. " + self.busyboxPath() + "\n")
                    else:   
                        self.stdout.write("BusyBox installation failed.\n")
        else:
            self.stdout.write("Unsupported CPU architecture. Supported architectures are arm, arm64, x86 and x86_64.\n")
