from mwr.droidhg.modules import common, Module

class SecretCodes(Module, common.ClassLoader, common.PackageManager):
    
    name = "Secret Codes"
    description = "Finds Secret Codes from all installed packages."
    examples = ""
    author = "Mike (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["scanner", "misc"]

    def add_arguments(self, parser):
        parser.add_argument("-v", "--verbose", action="store_true", default=False, help="be verbose")

    def execute(self, arguments):
        SecretCodes = self.loadClass("scanner/misc/SecretCodes.apk", "SecretCodes")

        packages = self.packageManager().installedPackages(0)

        for i in range(packages.size()):
            package = packages.get(i).packageName
            codes = SecretCodes.find(self.getContext(), package)

            if len(codes) > 0 or arguments.verbose == True:
                self.stdout.write("Package: %s\n"%package)

                for code in codes:
                    self.stdout.write("  %s\n"%code)

                self.stdout.write("\n")
                