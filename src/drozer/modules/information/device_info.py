from drozer.modules import common, Module

class DeviceInfo(Module, common.Shell):
    
    name = "Get verbose device information"
    description = "Gets device information"
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["information"]

    def execute(self, arguments):
        self.stdout.write("-----------------------------------------\n")
        self.stdout.write("/proc/version\n")
        self.stdout.write("-----------------------------------------\n")
        self.stdout.write(self.readFile("/proc/version") + "\n\n")

        self.stdout.write("-----------------------------------------\n")
        self.stdout.write("/system/build.prop\n")
        self.stdout.write("-----------------------------------------\n")
        self.stdout.write(self.readFile("/system/build.prop") + "\n\n")

        self.stdout.write("-----------------------------------------\n")
        self.stdout.write("getprop\n")
        self.stdout.write("-----------------------------------------\n\n")
        self.stdout.write(self.shellExec("getprop") + "\n")
        
