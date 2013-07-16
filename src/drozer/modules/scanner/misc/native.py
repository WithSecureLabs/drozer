from drozer.modules import common, Module

class Native(Module, common.ClassLoader, common.Filters, common.PackageManager):

    name = "Find native components included in packages"
    description = "Lists packages which use native code.\nNOTE: This only checks for libraries that are bundled inside the package APK. System packages often do not contain the libraries they use inside their APK and so this module will miss them."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["scanner", "misc"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", help="specify a package to search")
        parser.add_argument("-f", "--filter", action="store", dest="filter", default=None, help="filter term")
        parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be verbose")

    def execute(self, arguments):
        Native = self.loadClass("common/Native.apk", "Native")

        if arguments.package != None:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_PROVIDERS)
            
            self.__find_libraries(package, True, Native)
        else:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                if arguments.filter == None or package.packageName.upper().find(arguments.filter.upper()) >= 0:
                    self.__find_libraries(package, arguments.verbose, Native)
    
    def __find_libraries(self, package, verbose, Native):
        libraries = Native.list(package.applicationInfo)

        if len(libraries) > 0:
            self.stdout.write("Package: %s\n" % package.packageName)
            self.stdout.write("  Native Libraries:\n")

            for library in libraries:
                self.stdout.write("   - %s\n"%library)
            self.stdout.write("\n")
        elif verbose:
            self.stdout.write("Package: %s\n" % package.packageName)
            self.stdout.write("  No Native Libraries.\n")
            self.stdout.write("\n")
            
