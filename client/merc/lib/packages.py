#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import shlex
from basecmd import BaseCmd
from basecmd import BaseArgumentParser

class Packages(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#packages> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_info(self, args):
        """
List all installed packages on the device with optional filters. It is possible to search for keywords in package information and permissions using the filters.
usage: info [--filter <filter>] [--permissions <filter>] [--output <filename>]

--------------------------------
Example - finding which packages contain the keyword "browser" in their information
--------------------------------
*mercury#packages> info -f browser

Package name: com.android.browser
Process name: com.android.browser
Version: 2.3.6
Data directory: /data/data/com.android.browser
APK path: /system/app/Browser.apk
UID: 10014
GID: 3003; 1015; 
Shared libraries: /system/framework/com.motorola.android.frameworks.jar; /system/framework/com.motorola.android.storage.jar; 
Permissions: android.permission.ACCESS_COARSE_LOCATION; android.permission.ACCESS_DOWNLOAD_MANAGER; android.permission.ACCESS_FINE_LOCATION; android.permission.ACCESS_NETWORK_STATE; android.permission.ACCESS_WIFI_STATE; android.permission.VIBRATE; com.android.launcher.permission.INSTALL_SHORTCUT; android.permission.INTERNET; android.permission.SET_WALLPAPER; android.permission.WAKE_LOCK; android.permission.WRITE_EXTERNAL_STORAGE; android.permission.WRITE_SETTINGS; com.android.browser.permission.READ_HISTORY_BOOKMARKS; com.android.browser.permission.WRITE_HISTORY_BOOKMARKS; android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS; android.permission.SET_PREFERRED_APPLICATIONS; android.permission.WRITE_SECURE_SETTINGS;

--------------------------------
Example - finding which packages have the "INSTALL_PACKAGES" permission
--------------------------------
*mercury#packages> info -p INSTALL_PACKAGES

Package name: com.android.packageinstaller
Process name: com.android.packageinstaller
Version: 2.3.6
Data directory: /data/data/com.android.packageinstaller
APK path: /system/app/PackageInstaller.apk
UID: 10047
GID: 
Permissions: android.permission.INSTALL_PACKAGES; android.permission.DELETE_PACKAGES; android.permission.CLEAR_APP_CACHE; android.permission.READ_PHONE_STATE; android.permission.CLEAR_APP_USER_DATA; 

Package name: com.android.vending
Process name: com.android.vending
Version: 3.3.12
Data directory: /data/data/com.android.vending
APK path: /system/app/Phonesky.apk
UID: 10070
GID: 3003; 1015; 
Permissions: com.android.vending.billing.IN_APP_NOTIFY.permission.C2D_MESSAGE; com.google.android.c2dm.permission.RECEIVE; com.android.vending.BILLING; android.permission.GET_TASKS; android.permission.INTERNET; android.permission.GET_ACCOUNTS; android.permission.MANAGE_ACCOUNTS; android.permission.AUTHENTICATE_ACCOUNTS; android.permission.USE_CREDENTIALS; android.permission.WRITE_EXTERNAL_STORAGE; android.permission.READ_EXTERNAL_STORAGE; android.permission.CLEAR_APP_CACHE; android.permission.CHANGE_COMPONENT_ENABLED_STATE; android.permission.ACCESS_NETWORK_STATE; android.permission.READ_PHONE_STATE; android.permission.CHANGE_NETWORK_STATE; com.google.android.providers.gsf.permission.READ_GSERVICES; com.google.android.providers.gsf.permission.WRITE_GSERVICES; android.permission.ACCESS_DOWNLOAD_MANAGER; android.permission.ACCESS_DOWNLOAD_MANAGER_ADVANCED; android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS; android.permission.INSTALL_PACKAGES; android.permission.DELETE_PACKAGES; android.permission.NFC; com.android.vending.INTENT_VENDING_ONLY; android.permission.RECEIVE_BOOT_COMPLETED; android.permission.RECEIVE_SMS; com.android.launcher.permission.INSTALL_SHORTCUT; android.permission.STATUS_BAR; 

...
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        parser.add_argument('--permissions', '-p', metavar = '<filter>')


        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("packages", "info", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_shareduid(self, args):
        """
Get which packages share a UID
usage: shareduid [--uid <uid>] [--output <filename>]

--------------------------------
Example - finding all the packages that have the shared-UID of 10011
--------------------------------
*mercury#packages> shareduid -u 10011

UID: 10011 (com.motorola.blur.uid.provider_authenticator:10011)
Package name: com.motorola.blur.provider.photobucket
Package name: com.motorola.blur.provider.picasa
Package name: com.motorola.blur.provider.yahoo
Package name: com.motorola.blur.provider.twitter
Package name: com.motorola.blur.provider.fixedemail
Package name: com.motorola.blur.provider.motorola.app
Package name: com.motorola.blur.provider.orkut
Package name: com.motorola.blur.provider.email
Package name: com.motorola.blur.provider.facebook
Package name: com.motorola.blur.provider.lastfm
Package name: com.motorola.blur.provider.linkedin
Package name: com.motorola.blur.provider.youtube
Package name: com.motorola.blur.provider.skyrock
Package name: com.motorola.blur.provider.activesync
Package name: com.motorola.blur.provider.flickr
Accumulated permissions: com.motorola.blur.setupprovider.Permissions.ACCESS_ACCOUNTS; com.motorola.blur.permission.ACCESS_POLICY_MANAGER; com.motorola.blur.permission.ACCESS_POLICY_MANAGER_ADVANCED; android.permission.AUTHENTICATE_ACCOUNTS; android.permission.GET_ACCOUNTS; android.permission.MANAGE_ACCOUNTS; android.permission.READ_CONTACTS; com.motorola.blur.friendfeed.permission.READ; android.permission.ACCESS_NETWORK_STATE; android.permission.WRITE_SYNC_SETTINGS; com.motorola.blur.service.blur.Permissions.INTERACT_BLUR_SERVICE; com.motorola.blur.service.email.Permissions.INTERACT; android.permission.WRITE_EXTERNAL_STORAGE; android.permission.INTERNET; android.permission.BIND_DEVICE_ADMIN;
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'shareduid', add_help = False)
        parser.add_argument('--uid', '-u', metavar = '<uid>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("packages", "shareduid", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_attacksurface(self, args):
        """
Examine the attack surface of the given package
usage: attacksurface packageName [--output <filename>]

--------------------------------
Example - finding the attack surface of the built-in browser
--------------------------------
*mercury#packages> attacksurface com.android.browser

5 activities exported
3 broadcast receivers exported
1 content providers exported
0 services exported
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'attacksurface', add_help = False)
        parser.add_argument('packageName')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print self.session.executeCommand("packages", "attacksurface", {'packageName':splitargs.packageName}).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass
