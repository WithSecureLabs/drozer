#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex, sys, urllib2
from xml.dom.minidom import parseString
from merc.lib.basecmd import BaseCmd
from merc.lib.common import Session, mercury_version
from merc.lib.menu import Menu

class Mercury(BaseCmd):

    def __init__(self):
        BaseCmd.__init__(self, None)
        self.prompt = "mercury> "
        self.intro = """
               ..                    ..:.
              ..I..                  .I..
               ..I.    . . .... .  ..I=
                 .I...I?IIIIIIIII~..II
                 .?I?IIIIIIIIIIIIIIII..
              .,IIIIIIIIIIIIIIIIIIIIIII+.
           ...IIIIIIIIIIIIIIIIIIIIIIIIIII:.
           .IIIIIIIIIIIIIIIIIIIIIIIIIIIIIII..
         ..IIIIII,..,IIIIIIIIIIIII,..,IIIIII.
         .?IIIIIII..IIIIIIIIIIIIIII..IIIIIIII.
         ,IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
        .IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.
        .IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII:
        .IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

        The heavy metal that poisoned the droid
        """

    def do_exit(self, _args):
        """
Exits from Mercury
        """
        return -1

    def do_version(self, _args):
        """
Version and author information
        """
        print "\nMercury Client v" + mercury_version
        print "MWR InfoSecurity @ http://labs.mwrinfosecurity.com\n"

    def do_connect(self, args):
        """
Connect to a Mercury instance
usage: connect [--port <port>] ip
Use adb forward tcp:31415 tcp:31415 when using an emulator or usb-connected device
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'connect', add_help = False)
        parser.add_argument('ip')
        parser.add_argument('--port', '-p', metavar = '<port>')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Get session ip
            sessionip = splitargs.ip

            # Get session port
            if (splitargs.port):
                sessionport = int(splitargs.port)
            else:
                sessionport = 31415

            # Create new session object - display success/failure with session id
            newsession = Session(splitargs.ip, sessionport, "bind")

            # Check if connection can be established
            if newsession.executeCommand("core", "ping", None).data == "pong":

                # Start new session
                subconsole = Menu(newsession)
                subconsole.cmdloop()

            else:
                print "\n**Network Error** Could not connect to " + sessionip + ":" + str(sessionport) + "\n"

        # FIXME: Choose specific exceptions to catch
        except:
            print sys.exc_info()[0]
            
            
    def do_update(self, args):
        """
Check if there is an updated release available from http://labs.mwrinfosecurity.com
        """
        
        try:
            # Fetch the manifest file from the Labs site
            response = urllib2.urlopen("http://labs.mwrinfosecurity.com/tools/2012/03/16/mercury/downloads/manifest.xml")
            xmlStr = response.read()
            
            # Parse XML and get <version> contents
            doc = parseString(xmlStr)
            version = doc.getElementsByTagName("version")[0]
            
            # Get <number> text
            data = version.getElementsByTagName("number")[0].childNodes[0]
            if (data.nodeType == data.TEXT_NODE):
                update_version_number = data.nodeValue
            else:
                raise Exception("XML not in expected format")
            
            # Get <uri> text
            data = version.getElementsByTagName("uri")[0].childNodes[0]
            if (data.nodeType == data.TEXT_NODE):
                update_version_uri = data.nodeValue
            else:
                raise Exception("XML not in expected format")
            
            # Get <date> text
            data = version.getElementsByTagName("date")[0].childNodes[0]
            if (data.nodeType == data.TEXT_NODE):
                update_version_date = data.nodeValue
            else:
                raise Exception("XML not in expected format")
            
            # Get <size> text
            data = version.getElementsByTagName("size")[0].childNodes[0]
            if (data.nodeType == data.TEXT_NODE):
                update_version_size = data.nodeValue
            else:
                raise Exception("XML not in expected format")
            
            # Get <checksum> text
            data = version.getElementsByTagName("checksum")[0].childNodes[0]
            if (data.nodeType == data.TEXT_NODE):
                update_version_checksum = data.nodeValue
            else:
                raise Exception("XML not in expected format")
            
            # Check if current version is the latest
            if mercury_version == update_version_number:
                display =  "You are currently running the latest release."
            else:
                display = "There is an update available with the following information:\n"
                display += "Version: " + update_version_number + "\n"
                display += "Download: " + update_version_uri + "\n"
                display += "Date: " + update_version_date + "\n"
                display += "Size (bytes): " + update_version_size + "\n"
                display += "MD5: " + update_version_checksum
        
        except:
            display = "Failed to retrieve update information. Please visit http://labs.mwrinfosecurity.com to find information about the latest release."

        print "\n" + display + "\n"


if __name__ == '__main__':

    console = Mercury()
    console.cmdloop()
