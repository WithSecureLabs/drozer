from mwr.droidhg.modules import common, Module

class Permissions(Module, common.PackageManager):
    
    name = "Get a list of all permissions used by packages on the device"
    description = "Get a list of all permissions used by packages on the device"
    examples = '''
    mercury> run information.permissions
    android.permission.ACCESS_ALL_DOWNLOADS
    android.permission.ACCESS_ASSISTED_GPS
    android.permission.ACCESS_AUDIO
    android.permission.ACCESS_BLUETOOTH_SHARE
    android.permission.ACCESS_CACHE_FILESYSTEM
    android.permission.ACCESS_CELL_ID
    android.permission.ACCESS_CHECKIN_PROPERTIES
    android.permission.ACCESS_COARSE_LOCATION
    ...
    '''
    author = "Tyrone (@mwrlabs)"
    date = "2012-12-20"
    license = "MWR Code License"
    path = ["information"]

    def execute(self, arguments):
        
        permissionList = []
        
        # Iterate through each package and get unique permissions
        for package in self.packageManager().getPackages(common.PackageManager.GET_PERMISSIONS):
                if package.requestedPermissions != None:
                    for permission in package.requestedPermissions:
                        if permission not in permissionList:
                            permissionList.append(str(permission))
        
        # Print sorted
        for permission in sorted(permissionList):
            self.stdout.write(permission + "\n")
