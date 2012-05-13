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
Get information about exported content providers with optional filter
usage: info [--filter <filter>] [--permissions <filter>]
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
Find content uri strings in a package
usage: finduri packageName
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
                    if self.session.executeCommand("core", "unzip", {'path':line, 'destination':'/data/data/com.mwr.mercury/'}).isError():

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
