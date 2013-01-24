from mwr.droidhg import android
from mwr.droidhg.modules import common, Module

class AttackSurface(Module, common.Filters, common.PackageManager):

    name = "Get attack surface of package"
    description = "Examine the attack surface of an installed package."
    examples = """Finding the attack surface of the built-in browser

    mercury> run app.package.attacksurface com.android.browser

    6 activities exported
    4 broadcast receivers exported
    1 content providers exported
    0 services exported"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("package", help="the identifier of the package to inspect")

    def execute(self, arguments):
        if arguments.package != None:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_ACTIVITIES | common.PackageManager.GET_RECEIVERS | common.PackageManager.GET_PROVIDERS | common.PackageManager.GET_SERVICES)
            application = package.applicationInfo

            activities = self.match_filter(package.activities, 'exported', True)
            receivers = self.match_filter(package.receivers, 'exported', True)
            providers = self.match_filter(package.providers, 'exported', True)
            services = self.match_filter(package.services, 'exported', True)
            
            self.stdout.write("Attack Surface:\n")
            self.stdout.write("  %d activities exported\n" % len(activities))
            self.stdout.write("  %d broadcast receivers exported\n" % len(receivers))
            self.stdout.write("  %d content providers exported\n" % len(providers))
            self.stdout.write("  %d services exported\n" % len(services))

            if (application.flags & application.FLAG_DEBUGGABLE) != 0:
                self.stdout.write("    is debuggable\n")

            if package.sharedUserId != None:
                self.stdout.write("    Shared UID (%s)\n" % package.sharedUserId)
        else:
            self.stdout.write("Package Not Found\n")

class Info(Module, common.Filters, common.PackageManager):

    name = "Get information about installed packages"
    description = "List all installed packages on the device with optional filters. Specify optional keywords to search for in the package information, or granted permissions."
    examples = """Finding all packages with the keyword "browser" in their name:

    mercury> run app.package.info -f browser

    Package: com.android.browser
      Process name: com.android.browser
      Version: 4.1.1
      Data Directory: /data/data/com.android.browser
      APK path: /system/app/Browser.apk
      UID: 10014
      GID: [3003, 1015, 1028]
      Shared libraries: null
      Permissions:
      - android.permission.ACCESS_COARSE_LOCATION
      - android.permission.ACCESS_DOWNLOAD_MANAGER
      - android.permission.ACCESS_FINE_LOCATION
      ...

Finding all packages with the "INSTALL_PACKAGES" permission:

    mercury> run app.package.info -p INSTALL_PACKAGES

    Package: com.android.packageinstaller
      Process Name: com.android.packageinstaller
      Version: 4.1.1-403059
      Data Directory: /data/data/com.android.packageinstaller
      APK Path: /system/app/PackageInstaller.apk
      UID: 10003
      GID: [1028]
      Shared Libraries: null
      Shared User ID: null
      Permissions:
      - android.permission.INSTALL_PACKAGES
      - android.permission.DELETE_PACKAGES
      - android.permission.CLEAR_APP_CACHE
      - android.permission.READ_PHONE_STATE
      - android.permission.CLEAR_APP_USER_DATA
      - android.permission.READ_EXTERNAL_STORAGE"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", default=None, help="the identifier of the package to inspect")
        parser.add_argument("-f", "--filter", default=None, help="keyword filter conditions")
        parser.add_argument("-p", "--permission", default=None, help="permission filter conditions")

    def execute(self, arguments):
        if arguments.package == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS | common.PackageManager.GET_CONFIGURATIONS | common.PackageManager.GET_GIDS | common.PackageManager.GET_SHARED_LIBRARY_FILES):
                self.__get_package(arguments, package)
        else:
            package = self.packageManager().getPackageInfo(arguments.package, common.PackageManager.GET_PERMISSIONS | common.PackageManager.GET_CONFIGURATIONS | common.PackageManager.GET_GIDS | common.PackageManager.GET_SHARED_LIBRARY_FILES)

            self.__get_package(arguments, package)
            
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "permission":
            return android.permissions

    def __get_package(self, arguments, package):
        application = package.applicationInfo

        if (arguments.filter == None or package.packageName.upper().find(arguments.filter.upper()) >= 0) and (arguments.permission == None or package.requestedPermissions != None and True in map(lambda p: p.upper().find(arguments.permission.upper()) >= 0, package.requestedPermissions)):
            self.stdout.write("Package: %s\n" % application.packageName)
            self.stdout.write("  Process Name: %s\n" % application.processName)
            self.stdout.write("  Version: %s\n" % package.versionName)
            self.stdout.write("  Data Directory: %s\n" % application.dataDir)
            self.stdout.write("  APK Path: %s\n" % application.publicSourceDir)
            self.stdout.write("  UID: %s\n" % application.uid)
            if package.gids != None:
                self.stdout.write("  GID: %s\n" % package.gids)
            else:
                self.stdout.write("  GID: None")
            self.stdout.write("  Shared Libraries: %s\n" % application.sharedLibraryFiles)
            self.stdout.write("  Shared User ID: %s\n" % package.sharedUserId)
            self.stdout.write("  Permissions:\n")
            if package.requestedPermissions != None:
                for permission in package.requestedPermissions:
                    self.stdout.write("  - %s\n" % permission)
            else:
                self.stdout.write("  - None\n")
            self.stdout.write("\n")

class LaunchIntent(Module, common.PackageManager):

    name = "Get launch intent of package"
    description = "Get the launch intent of an installed package."
    examples = """Finding the launch intent of the Android browser package:

    mercury> run app.package.launchintent com.android.browser

    Intent { act=android.intent.action.MAIN flg=0x10000000
             cmp=com.android.browser/.BrowserActivity }"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("package", help="the identifier of the package to inspect")

    def execute(self, arguments):
        intent = self.packageManager().getLaunchIntentForPackage(arguments.package)

        if intent != None:
            self.stdout.write("%s\n\n" % str(intent.toString()))
        else:
            self.stdout.write("No Launch Intent found.\n\n")

class List(Module, common.PackageManager):

    name = "List Packages"
    description = "List all installed packages on the device. Specify optional keywords to search for in the package name."
    examples = """Finding all packages with the keyword "browser" in their name:

    mercury> run app.package.list -f browser

    com.android.browser"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("-f", "--filter", default=None, help="keyword filter conditions")

    def execute(self, arguments):
        for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS | common.PackageManager.GET_CONFIGURATIONS | common.PackageManager.GET_GIDS | common.PackageManager.GET_SHARED_LIBRARY_FILES):
            self.__get_package(arguments, package)

    def __get_package(self, arguments, package):
        application = package.applicationInfo

        if arguments.filter == None or package.packageName.upper().find(arguments.filter.upper()) >= 0:
            self.stdout.write("%s\n" % application.packageName)

class Manifest(Module, common.Assets, common.ClassLoader):

    name = "Get AndroidManifest.xml of package"
    description = "Retrieves AndroidManifest.xml from an installed package."
    examples = """Getting the manifest for Mercury

    mercury> run app.package.manifest com.mwr.droidhg.agent

    <manifest versionCode="2" versionName="1.1" package="com.mwr.mercury">
      <uses-sdk minSdkVersion="8" targetSdkVersion="4">
      </uses-sdk>
      <uses-permission name="android.permission.INTERNET">
      </uses-permission>

      ...
    </manifest>"""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("package", help="the identifier of the package")

    def execute(self, arguments):
        if arguments.package == None or arguments.package == "":
            self.stderr.write("No package provided.\n")
        else:
            self.stdout.write(self.getAndroidManifest(arguments.package) + "\n")

class SharedUID(Module, common.PackageManager):

    name = "Look for packages with shared UIDs"
    description = "Finds packages that have shared UIDs and gives their accumulated permissions."
    examples = """Finding packages that share the UID 10011

    mercury> run app.package.shareduid -u 10011

    UID: 10011 (com.motorola.blur.uid.provider_authenticator:10011)
    Package Name: com.motorola.blur.provider.photobucket
    Package Name: com.motorola.blur.provider.picasa
    Package Name: com.motorola.blur.provider.yahoo
    Package Name: com.motorola.blur.provider.twitter
    Package Name: com.motorola.blur.provider.fixedemail
    Package Name: com.motorola.blur.provider.motorola.app
    Package Name: com.motorola.blur.provider.orkut
    Package Name: com.motorola.blur.provider.email
    Package Name: com.motorola.blur.provider.facebook
    Package Name: com.motorola.blur.provider.lastfm
    Package Name: com.motorola.blur.provider.linkedin
    Package Name: com.motorola.blur.provider.youtube
    Package Name: com.motorola.blur.provider.skyrock
    Package Name: com.motorola.blur.provider.activesync
    Package Name: com.motorola.blur.provider.flickr
    Accumulated permissions: com.motorola.blur.setupprovider.Permissions.ACCESS_ACCOUNTS; ..."""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["app", "package"]

    def add_arguments(self, parser):
        parser.add_argument("-u", "--uid", default=None, help="specify uid")

    def execute(self, arguments):
        uids = set([])

        if arguments.uid == None:
            for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                uids.add(int(package.applicationInfo.uid))
        else:
            uids.add(int(arguments.uid))

        for uid in uids:
            self.stdout.write("UID: %d (%s)\n"%(uid, self.packageManager().getNameForUid(uid)))

            packages = self.packageManager().getPackagesForUid(uid)

            if packages != None:
                permissions = set([])

                for packageName in packages:
                    package = self.packageManager().getPackageInfo(packageName, common.PackageManager.GET_PERMISSIONS)

                    self.stdout.write("  Package: %s\n"%packageName)

                    if package.requestedPermissions != None:
                        for permission in package.requestedPermissions:
                            permissions.add(permission)

                self.stdout.write("  Permissions: %s\n"%", ".join(map(lambda p: str(p), permissions)))
                self.stdout.write("\n")
            else:
                self.stdout.write("No such UID.\n")
