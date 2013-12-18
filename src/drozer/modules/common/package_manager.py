from pydiesel.reflection import ReflectionException

class PackageManager(object):
    """
    Utility methods for interacting with the Android Package Manager.
    """

    GET_ACTIVITIES = 0x00000001
    GET_CONFIGURATIONS = 0x00004000
    GET_DISABLED_COMPONENTS = 0x00000200
    GET_GIDS = 0x00000100
    GET_INSTRUMENTATION = 0x00000010
    GET_INTENT_FILTERS = 0x00000020
    GET_META_DATA = 0x00000080
    MATCH_DEFAULT_ONLY = 0x00010000
    GET_PERMISSIONS = 0x00001000
    GET_PROVIDERS = 0x00000008
    GET_RECEIVERS = 0x00000002
    GET_RESOLVED_FILTER = 0x00000040
    GET_SERVICES = 0x00000004
    GET_SHARED_LIBRARY_FILES = 0x00000400
    GET_SIGNATURES = 0x00000040
    GET_URI_PERMISSION_PATTERNS = 0x00000800

    __package_manager_proxy = None
    
    class NoSuchPackageException(ReflectionException):
        
        def __str__(self):
            return "could not find the package: %s" % self.message

    class PackageManagerProxy(object):
        """
        Wrapper for the native Java PackageManager object, which provides convenience
        methods for handling some of the return types.
        """

        def __init__(self, module):
            self.__module = module
            self.__package_manager = module.getContext().getPackageManager()

        def getLaunchIntentForPackage(self, package):
            """
            Gets the Launch Intent for the specified package.
            """

            return self.__package_manager.getLaunchIntentForPackage(package)

        def getNameForUid(self, uid):
            """
            Gets the name associated with the specified UID.
            """

            return self.__package_manager.getNameForUid(uid)

        def getPackageInfo(self, package, flags=0):
            """
            Get a package's PackageInfo object, optionally passing flags.
            """
            
            try:
                return self.__package_manager.getPackageInfo(package, flags)
            except ReflectionException as e:
                if e.message == package:
                    raise PackageManager.NoSuchPackageException(package)
                else:
                    raise

        def getPackages(self, flags=0):
            """
            Iterate through all installed packages.
            """

            packages = self.installedPackages(flags)

            for i in xrange(packages.size()):
                yield packages.get(i)

        def getApplicationLabel(self, package, flags=0):
            """
            Get the 'app_name' string for a package.
            """
            try:
                pkg = self.__package_manager.getApplicationInfo(package, flags)
                return self.__package_manager.getApplicationLabel(pkg)
            except ReflectionException as e:
                if e.message == package:
                    raise PackageManager.NoSuchPackageException(package)
                else:
                    raise

        def getPackagesForUid(self, uid):
            """
            Get all packages with a specified UID.
            """

            return self.__package_manager.getPackagesForUid(uid)

        def getSourcePaths(self, package):
            """
            Get all source directories associated with a package.
            """

            return self.getPackageInfo(package).applicationInfo.publicSourceDir.split()

        def installedPackages(self, flags=0):
            """
            Get all installed packages, as a Java List<>.
            """

            return self.__package_manager.getInstalledPackages(flags)

        def packageManager(self):
            """
            Get the internal reference to the PackageManager.
            """

            return self.__package_manager

        def queryContentProviders(self, process_name, uid, flags):
            """
            Get Content Provider information.
            """

            providers = self.__package_manager.queryContentProviders(process_name, uid, flags)

            for i in xrange(providers.size()):
                yield providers.get(i)

        def queryIntentActivities(self, intent, flags):
            """
            Get all Activities that can be launched with a specified Intent.
            """

            activities = self.__package_manager.queryIntentActivities(intent.buildIn(self.__module), flags)

            for i in xrange(activities.size()):
                yield activities.get(i)

    def packageManager(self):
        """
        Get the Android PackageManager.
        """

        if self.__package_manager_proxy == None:
            self.__package_manager_proxy = PackageManager.PackageManagerProxy(self)

        return self.__package_manager_proxy
        
