from mwr.droidhg.modules import common, Module

class Native(Module, common.ClassLoader, common.Filters, common.PackageManager):

    name = "Find native components included in packages"
    description = "Lists packages which use native code."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["scanner", "misc"]

    def add_arguments(self, parser):
        parser.add_argument("-f", "--filter", action="store", dest="filter", default=None, help="filter term")
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be verbose")

    def execute(self, arguments):
        Native = self.loadClass("scanner/misc/Native.apk", "Native")

        for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
            if arguments.filter == None or package.packageName.upper().find(arguments.filter.upper()) >= 0:
                libraries = Native.libraries(package.applicationInfo)

                if len(libraries) > 0:
                    self.stdout.write("Package: %s\n" % package.packageName)
                    self.stdout.write("  Native Libraries:\n")

                    for library in libraries:
                        self.stdout.write("   - %s\n"%library)
                    self.stdout.write("\n")
                elif arguments.verbose:
                    self.stdout.write("Package: %s\n" % package.packageName)
                    self.stdout.write("  No Native Libraries.\n")
                    self.stdout.write("\n")
                