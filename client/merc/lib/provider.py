#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex
from basecmd import BaseCmd

class Provider(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#provider> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_columns(self, args):
        """
Get the columns of the specified content uri
usage: columns uri

--------------------------------
Example - finding the columns on content://settings/secure
--------------------------------
*mercury#provider> columns content://settings/secure

_id | name | value
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'columns', add_help = False)
        parser.add_argument('uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = {}

            if (splitargs.uri):
                request['uri'] = splitargs.uri

            print self.session.executeCommand("provider", "columns", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_query(self, args):
        """
Query the specified content provider
usage: query [--projection <column> [<column> ...]] [--selection <rows>]
             [--selectionArgs <arg> [<arg> ...]] [--sortOrder <order>]
             [--showColumns <true/false>]
             Uri
             
The general structure of a content URI is:
content://authority/table

--------------------------------
Example - querying the settings content provider
--------------------------------
*mercury#provider> query content://settings/secure

_id | name | value
.....

5 | assisted_gps_enabled | 1

9 | wifi_networks_available_notification_on | 1

10 | sys_storage_full_threshold_bytes | 2097152

11 | sys_storage_threshold_percentage | 10

12 | preferred_network_mode | 3

13 | cdma_cell_broadcast_sms | 1

14 | preferred_cdma_subscription | 1

15 | mock_location | 0

17 | backup_transport | com.google.android.backup/.BackupTransportService

18 | throttle_polling_sec | 600

...
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'query', add_help = False)
        parser.add_argument('--projection', '-p', nargs = '+', metavar = '<column>')
        parser.add_argument('--selection', '-s', metavar = '<rows>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('--sortOrder', '-so', metavar = '<order>')
        parser.add_argument('--showColumns', '-nc', metavar = '<true/false>')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("provider", "query", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass
        
    def do_read(self, args):
        """
Read from the specified content uri using openInputStream
usage: read Uri

--------------------------------
Example - attempting a directory traversal on a content provider that supports file reading
--------------------------------
*mercury#provider> read content://settings/secure/../../../../../../../../../../../system/etc/hosts

No files supported by provider at content://settings/secure/../../../../../../../../../../../system/etc/hosts
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'read', add_help = False)
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)
            
            print self.session.executeCommand("provider", "read", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass


    def do_insert(self, args):
        """
Insert into the specified content uri
usage: insert [--string column=data [column=data ...]]
              [--boolean column=data [column=data ...]]
              [--integer column=data [column=data ...]]
              [--double column=data [column=data ...]]
              [--float column=data [column=data ...]]
              [--long column=data [column=data ...]]
              [--short column=data [column=data ...]]
              Uri
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'insert', add_help = False)
        parser.add_argument('--string', '-s', nargs = '+', metavar = 'column=data')
        parser.add_argument('--boolean', '-b', nargs = '+', metavar = 'column=data')
        parser.add_argument('--integer', '-i', nargs = '+', metavar = 'column=data')
        parser.add_argument('--double', '-d', nargs = '+', metavar = 'column=data')
        parser.add_argument('--float', '-f', nargs = '+', metavar = 'column=data')
        parser.add_argument('--long', '-l', nargs = '+', metavar = 'column=data')
        parser.add_argument('--short', '-sh', nargs = '+', metavar = 'column=data')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("provider", "insert", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_delete(self, args):
        """
Delete from the specified content uri
usage: delete [--where <where>] [--selectionArgs <arg> [<arg> ...]] Uri
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'delete', add_help = False)
        parser.add_argument('--where', '-w', metavar = '<where>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("provider", "delete", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_update(self, args):
        """
Update the specified content uri
usage: update [--string column=data [column=data ...]]
              [--boolean column=data [column=data ...]]
              [--integer column=data [column=data ...]]
              [--double column=data [column=data ...]]
              [--float column=data [column=data ...]]
              [--long column=data [column=data ...]]
              [--short column=data [column=data ...]] [--where <where>]
              [--selectionArgs args]
              Uri
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'update', add_help = False)
        parser.add_argument('--string', '-s', nargs = '+', metavar = 'column=data')
        parser.add_argument('--boolean', '-b', nargs = '+', metavar = 'column=data')
        parser.add_argument('--integer', '-i', nargs = '+', metavar = 'column=data')
        parser.add_argument('--double', '-d', nargs = '+', metavar = 'column=data')
        parser.add_argument('--float', '-f', nargs = '+', metavar = 'column=data')
        parser.add_argument('--long', '-l', nargs = '+', metavar = 'column=data')
        parser.add_argument('--short', '-sh', nargs = '+', metavar = 'column=data')
        parser.add_argument('--where', '-w', metavar = '<where>')
        parser.add_argument('--selectionArgs', '-sa', nargs = '+', metavar = '<arg>')
        parser.add_argument('Uri')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("provider", "update", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass


    def do_info(self, args):
        """
Get information about exported content providers with optional filters. . It is possible to search for keywords in content provider information and permissions using the filters.
usage: info [--filter <filter>] [--permissions <filter>]

--------------------------------
Example - finding all content provider with the keyword "settings" in them
--------------------------------
*mercury#provider> info -f settings

Package name: com.google.android.gsf
Authority: com.google.settings
Required Permission - Read: null
Required Permission - Write: com.google.android.providers.settings.permission.WRITE_GSETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.android.providers.settings
Authority: settings
Required Permission - Read: null
Required Permission - Write: android.permission.WRITE_SETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

--------------------------------
Example - finding all content providers that do not require any permissions to read from them or write to them
--------------------------------
*mercury#provider> info -p null

Package name: com.google.android.gsf
Authority: com.google.settings
Required Permission - Read: null
Required Permission - Write: com.google.android.providers.settings.permission.WRITE_GSETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.android.providers.settings
Authority: settings
Required Permission - Read: null
Required Permission - Write: android.permission.WRITE_SETTINGS
Grant Uri Permissions: false
Multiprocess allowed: false

Package name: com.google.android.apps.uploader
Authority: com.google.android.apps.uploader
Required Permission - Read: null
Required Permission - Write: null
Grant Uri Permissions: false
Multiprocess allowed: false

...
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')
        parser.add_argument('--permissions', '-p', metavar = '<filter>')


        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to executeCommand
            request = vars(splitargs)

            print self.session.executeCommand("provider", "info", request).getPaddedErrorOrData()

        # FIXME: Choose specific exceptions to catch
        except:
            pass


    def do_finduri(self, args):
        """
Find content uri strings that are referenced in a package
usage: finduri packageName

--------------------------------
Example - finding all content URI's referenced in the browser package
--------------------------------
*mercury#provider> finduri com.android.browser

/system/app/Browser.apk:
Contains no classes.dex

/system/app/Browser.odex:
content://com.google.android.partnersetup.rlzappprovider/
content://com.google.settings/partner

        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'finduri', add_help = False)
        parser.add_argument('packageName')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            path = self.session.executeCommand("packages", "path", {'packageName':splitargs.packageName}).data

            print ""

            # Delete classes.dex that might be there from previously
            self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})

            # Iterate through paths returned
            for line in path.split():

                if (".apk" in line):
                    print line + ":"
                    if self.session.executeCommand("core", "unzip", {'filename':'classes.dex', 'path':line, 'destination':'/data/data/com.mwr.mercury/'}).isError():

                        print "Contains no classes.dex\n"

                    else:

                        strings = self.session.executeCommand("provider", "finduri", {'path':'/data/data/com.mwr.mercury/classes.dex'}).data

                        for string in strings.split():
                            if (("CONTENT://" in string.upper()) and ("CONTENT://" != string.upper())):
                                print string[string.upper().find("CONTENT"):]

                        # Delete classes.dex
                        self.session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})

                        print ""


                if (".odex" in line):
                    print line + ":"
                    strings = self.session.executeCommand("core", "strings", {'path':line}).data

                    for string in strings.split():
                        if (("CONTENT://" in string.upper()) and ("CONTENT://" != string.upper())):
                            print string[string.upper().find("CONTENT"):]

                    print ""


        # FIXME: Choose specific exceptions to catch
        except:
            pass
