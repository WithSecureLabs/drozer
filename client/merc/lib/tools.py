#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import argparse, shlex, os
from basecmd import BaseCmd
from common import intentDictionary

class Tools(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#tools> "

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_download(self, args):
        """
Download a file from the device
usage: download filepath downloadfolder
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'download', add_help = False)
        parser.add_argument('path')
        parser.add_argument('downloadfolder')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            response = self.session.downloadFile(splitargs.path, splitargs.downloadfolder)

            if response.isError():
                print "\n" + response.error + "\n"
            else:
                print "\nFile downloaded successfully\nMD5 = " + response.data + "\n"

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def complete_download(self, _text, line, _begidx, _endidx):
        # Split args with shlex
        splitargs = shlex.split(line)

        # Check if the 3rd option is being delt with
        if (len(splitargs) == 3):
            enteredpath = splitargs[-1]

            # Get the folder and path to be completed
            folder = enteredpath[:enteredpath.rfind('/') + 1] if (enteredpath != '/') else "/"
            halfcomplete = enteredpath[enteredpath.rfind('/') + 1:]

            return [
                    (path + "/") for path in os.listdir(folder)
                    if (path.startswith(halfcomplete) and path != halfcomplete and os.path.isdir(folder + path))
                ]



    def do_upload(self, args):
        """
Upload a file to the device
usage: upload [--uploadFolder <uploadFolder>] localPath
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'upload', add_help = False)
        parser.add_argument('localPath')
        parser.add_argument('--uploadFolder', '-u', metavar = '<uploadFolder>')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Check for specified upload dir. Defaults to Mercury data dir
            if splitargs.uploadFolder:
                uploadDir = splitargs.uploadFolder
            else:
                uploadDir = "/data/data/com.mwr.mercury/"

            response = self.session.uploadFile(splitargs.localPath, uploadDir)

            if (response.isError()):
                print response.getPaddedError()
            else:
                print "\nFile uploaded successfully to " + uploadDir + "\nMD5: " + response.data + "\n"

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def complete_upload(self, _text, line, _begidx, _endidx):
        # Split args with shlex
        splitargs = shlex.split(line)

        # Check if the 2nd option is being delt with
        if (len(splitargs) == 2):
            enteredpath = splitargs[1]

            # Get the folder and path to be completed
            folder = enteredpath[:enteredpath.rfind('/') + 1] if (enteredpath != '/') else "/"
            halfcomplete = enteredpath[enteredpath.rfind('/') + 1:]

            return [
                    ((path + "/") if os.path.isdir(folder + path) else (path)) for path in os.listdir(folder)
                    if (path.startswith(halfcomplete) and path != halfcomplete)
                ]



    def do_fileinfo(self, args):
        """
Get size and MD5 of specified file on the device
usage: fileinfo path
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'fileinfo', add_help = False)
        parser.add_argument('path')

        try:
            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            fileSize = self.session.executeCommand("core", "fileSize", {"path":splitargs.path})

            if (fileSize.isError()):
                print fileSize.getPaddedError()
            else:
                print "\nSize (bytes) = " + fileSize.data
                print "MD5 = " + self.session.executeCommand("core", "fileMD5", {"path":splitargs.path}).data + "\n"

        # FIXME: Choose specific exceptions to catch
        except:
            pass

    def do_intents(self, args):
        """
List all actions/categories/extras with optional search filter
usage: intents [--filter <filter>]
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'intents', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            print ""

            for value in sorted(intentDictionary.itervalues()):
                if splitargs.filter == None or value.upper().find(splitargs.filter.upper()) > -1:
                    print value

            print ""

        # FIXME: Choose specific exceptions to catch
        except:
            pass
