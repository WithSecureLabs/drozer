#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import os
import xml.dom.minidom
import socket
import re
import base64
import types
import md5

from xml.dom.minidom import parseString

# Mercury version
mercury_version = "1.0"

# Debugging mode
debug_mode = False

# Define a dictionary of all intents and their corresponding string values
intentDictionary = {"ACTION_AIRPLANE_MODE_CHANGED":"android.intent.action.AIRPLANE_MODE", "ACTION_ALL_APPS":"android.intent.action.ALL_APPS", "ACTION_ANSWER":"android.intent.action.ANSWER", "ACTION_ATTACH_DATA":"android.intent.action.ATTACH_DATA", "ACTION_BATTERY_CHANGED":"android.intent.action.BATTERY_CHANGED", "ACTION_BATTERY_LOW":"android.intent.action.BATTERY_LOW", "ACTION_BATTERY_OKAY":"android.intent.action.BATTERY_OKAY", "ACTION_BOOT_COMPLETED":"android.intent.action.BOOT_COMPLETED", "ACTION_BUG_REPORT":"android.intent.action.BUG_REPORT", "ACTION_CALL":"android.intent.action.CALL", "ACTION_CALL_BUTTON":"android.intent.action.CALL_BUTTON", "ACTION_CAMERA_BUTTON":"android.intent.action.CAMERA_BUTTON", "ACTION_CHOOSER":"android.intent.action.CHOOSER", "ACTION_CLOSE_SYSTEM_DIALOGS":"android.intent.action.CLOSE_SYSTEM_DIALOGS", "ACTION_CONFIGURATION_CHANGED":"android.intent.action.CONFIGURATION_CHANGED", "ACTION_CREATE_SHORTCUT":"android.intent.action.CREATE_SHORTCUT", "ACTION_DATE_CHANGED":"android.intent.action.DATE_CHANGED", "ACTION_DEFAULT":"android.intent.action.VIEW", "ACTION_DELETE":"android.intent.action.DELETE", "ACTION_DEVICE_STORAGE_LOW":"android.intent.action.DEVICE_STORAGE_LOW", "ACTION_DEVICE_STORAGE_OK":"android.intent.action.DEVICE_STORAGE_OK", "ACTION_DIAL":"android.intent.action.DIAL", "ACTION_DOCK_EVENT":"android.intent.action.DOCK_EVENT", "ACTION_EDIT":"android.intent.action.EDIT", "ACTION_EXTERNAL_APPLICATIONS_AVAILABLE":"android.intent.action.EXTERNAL_APPLICATIONS_AVAILABLE", "ACTION_EXTERNAL_APPLICATIONS_UNAVAILABLE":"android.intent.action.EXTERNAL_APPLICATIONS_UNAVAILABLE", "ACTION_FACTORY_TEST":"android.intent.action.FACTORY_TEST", "ACTION_GET_CONTENT":"android.intent.action.GET_CONTENT", "ACTION_GTALK_SERVICE_CONNECTED":"android.intent.action.GTALK_CONNECTED", "ACTION_GTALK_SERVICE_DISCONNECTED":"android.intent.action.GTALK_DISCONNECTED", "ACTION_HEADSET_PLUG":"android.intent.action.HEADSET_PLUG", "ACTION_INPUT_METHOD_CHANGED":"android.intent.action.INPUT_METHOD_CHANGED", "ACTION_INSERT":"android.intent.action.INSERT", "ACTION_INSERT_OR_EDIT":"android.intent.action.INSERT_OR_EDIT", "ACTION_LOCALE_CHANGED":"android.intent.action.LOCALE_CHANGED", "ACTION_MAIN":"android.intent.action.MAIN", "ACTION_MANAGE_PACKAGE_STORAGE":"android.intent.action.MANAGE_PACKAGE_STORAGE", "ACTION_MEDIA_BAD_REMOVAL":"android.intent.action.MEDIA_BAD_REMOVAL", "ACTION_MEDIA_BUTTON":"android.intent.action.MEDIA_BUTTON", "ACTION_MEDIA_CHECKING":"android.intent.action.MEDIA_CHECKING", "ACTION_MEDIA_EJECT":"android.intent.action.MEDIA_EJECT", "ACTION_MEDIA_MOUNTED":"android.intent.action.MEDIA_MOUNTED", "ACTION_MEDIA_NOFS":"android.intent.action.MEDIA_NOFS", "ACTION_MEDIA_REMOVED":"android.intent.action.MEDIA_REMOVED", "ACTION_MEDIA_SCANNER_FINISHED":"android.intent.action.MEDIA_SCANNER_FINISHED", "ACTION_MEDIA_SCANNER_SCAN_FILE":"android.intent.action.MEDIA_SCANNER_SCAN_FILE", "ACTION_MEDIA_SCANNER_STARTED":"android.intent.action.MEDIA_SCANNER_STARTED", "ACTION_MEDIA_SHARED":"android.intent.action.MEDIA_SHARED", "ACTION_MEDIA_UNMOUNTABLE":"android.intent.action.MEDIA_UNMOUNTABLE", "ACTION_MEDIA_UNMOUNTED":"android.intent.action.MEDIA_UNMOUNTED", "ACTION_NEW_OUTGOING_CALL":"android.intent.action.NEW_OUTGOING_CALL", "ACTION_PACKAGE_ADDED":"android.intent.action.PACKAGE_ADDED", "ACTION_PACKAGE_CHANGED":"android.intent.action.PACKAGE_CHANGED", "ACTION_PACKAGE_DATA_CLEARED":"android.intent.action.PACKAGE_DATA_CLEARED", "ACTION_PACKAGE_INSTALL":"android.intent.action.PACKAGE_INSTALL", "ACTION_PACKAGE_REMOVED":"android.intent.action.PACKAGE_REMOVED", "ACTION_PACKAGE_REPLACED":"android.intent.action.PACKAGE_REPLACED", "ACTION_PACKAGE_RESTARTED":"android.intent.action.PACKAGE_RESTARTED", "ACTION_PICK_ACTIVITY":"android.intent.action.PICK_ACTIVITY", "ACTION_PICK":"android.intent.action.PICK", "ACTION_POWER_CONNECTED":"android.intent.action.ACTION_POWER_CONNECTED", "ACTION_POWER_DISCONNECTED":"android.intent.action.ACTION_POWER_DISCONNECTED", "ACTION_POWER_USAGE_SUMMARY":"android.intent.action.POWER_USAGE_SUMMARY", "ACTION_PROVIDER_CHANGED":"android.intent.action.PROVIDER_CHANGED", "ACTION_REBOOT":"android.intent.action.REBOOT", "ACTION_RUN":"android.intent.action.RUN", "ACTION_SCREEN_OFF":"android.intent.action.SCREEN_OFF", "ACTION_SCREEN_ON":"android.intent.action.SCREEN_ON", "ACTION_SEARCH":"android.intent.action.SEARCH", "ACTION_SEARCH_LONG_PRESS":"android.intent.action.SEARCH_LONG_PRESS", "ACTION_SEND":"android.intent.action.SEND", "ACTION_SEND_MULTIPLE":"android.intent.action.SEND_MULTIPLE", "ACTION_SENDTO":"android.intent.action.SENDTO", "ACTION_SET_WALLPAPER":"android.intent.action.SET_WALLPAPER", "ACTION_SHUTDOWN":"android.intent.action.ACTION_SHUTDOWN", "ACTION_SYNC":"android.intent.action.SYNC", "ACTION_SYSTEM_TUTORIAL":"android.intent.action.SYSTEM_TUTORIAL", "ACTION_TIME_CHANGED":"android.intent.action.TIME_SET", "ACTION_TIME_TICK":"android.intent.action.TIME_TICK", "ACTION_TIMEZONE_CHANGED":"android.intent.action.TIMEZONE_CHANGED", "ACTION_UID_REMOVED":"android.intent.action.UID_REMOVED", "ACTION_UMS_CONNECTED":"android.intent.action.UMS_CONNECTED", "ACTION_UMS_DISCONNECTED":"android.intent.action.UMS_DISCONNECTED", "ACTION_USER_PRESENT":"android.intent.action.USER_PRESENT", "ACTION_VIEW":"android.intent.action.VIEW", "ACTION_VOICE_COMMAND":"android.intent.action.VOICE_COMMAND", "ACTION_WALLPAPER_CHANGED":"android.intent.action.WALLPAPER_CHANGED", "ACTION_WEB_SEARCH":"android.intent.action.WEB_SEARCH", "CATEGORY_ALTERNATIVE":"android.intent.category.ALTERNATIVE", "CATEGORY_BROWSABLE":"android.intent.category.BROWSABLE", "CATEGORY_CAR_DOCK":"android.intent.category.CAR_DOCK", "CATEGORY_CAR_MODE":"android.intent.category.CAR_MODE", "CATEGORY_DEFAULT":"android.intent.category.DEFAULT", "CATEGORY_DESK_DOCK":"android.intent.category.DESK_DOCK", "CATEGORY_DEVELOPMENT_PREFERENCE":"android.intent.category.DEVELOPMENT_PREFERENCE", "CATEGORY_EMBED":"android.intent.category.EMBED", "CATEGORY_FRAMEWORK_INSTRUMENTATION_TEST":"android.intent.category.FRAMEWORK_INSTRUMENTATION_TEST", "CATEGORY_HOME":"android.intent.category.HOME", "CATEGORY_INFO":"android.intent.category.INFO", "CATEGORY_LAUNCHER":"android.intent.category.LAUNCHER", "CATEGORY_MONKEY":"android.intent.category.MONKEY", "CATEGORY_OPENABLE":"android.intent.category.OPENABLE", "CATEGORY_PREFERENCE":"android.intent.category.PREFERENCE", "CATEGORY_SAMPLE_CODE":"android.intent.category.SAMPLE_CODE", "CATEGORY_SELECTED_ALTERNATIVE":"android.intent.category.SELECTED_ALTERNATIVE", "CATEGORY_TAB":"android.intent.category.TAB", "CATEGORY_TEST":"android.intent.category.TEST", "CATEGORY_UNIT_TEST":"android.intent.category.UNIT_TEST", "EXTRA_ALARM_COUNT":"android.intent.extra.ALARM_COUNT", "EXTRA_BCC":"android.intent.extra.BCC", "EXTRA_CC":"android.intent.extra.CC", "EXTRA_CHANGED_COMPONENT_NAME":"android.intent.extra.changed_component_name", "EXTRA_CHANGED_COMPONENT_NAME_LIST":"android.intent.extra.changed_component_name_list", "EXTRA_CHANGED_PACKAGE_LIST":"android.intent.extra.changed_package_list", "EXTRA_CHANGED_UID_LIST":"android.intent.extra.changed_uid_list", "EXTRA_DATA_REMOVED":"android.intent.extra.DATA_REMOVED", "EXTRA_DOCK_STATE":"android.intent.extra.DOCK_STATE", "EXTRA_DONT_KILL_APP":"android.intent.extra.DONT_KILL_APP", "EXTRA_EMAIL":"android.intent.extra.EMAIL", "EXTRA_INITIAL_INTENTS":"android.intent.extra.INITIAL_INTENTS", "EXTRA_INTENT":"android.intent.extra.INTENT", "EXTRA_KEY_EVENT":"android.intent.extra.KEY_EVENT", "EXTRA_PHONE_NUMBER":"android.intent.extra.PHONE_NUMBER", "EXTRA_REMOTE_INTENT_TOKEN":"android.intent.extra.remote_intent_token", "EXTRA_REPLACING":"android.intent.extra.REPLACING", "EXTRA_SHORTCUT_ICON":"android.intent.extra.shortcut.ICON", "EXTRA_SHORTCUT_ICON_RESOURCE":"android.intent.extra.shortcut.ICON_RESOURCE", "EXTRA_SHORTCUT_INTENT":"android.intent.extra.shortcut.INTENT", "EXTRA_SHORTCUT_NAME":"android.intent.extra.shortcut.NAME", "EXTRA_STREAM":"android.intent.extra.STREAM", "EXTRA_SUBJECT":"android.intent.extra.SUBJECT", "EXTRA_TEMPLATE":"android.intent.extra.TEMPLATE", "EXTRA_TEXT":"android.intent.extra.TEXT", "EXTRA_TITLE":"android.intent.extra.TITLE", "EXTRA_UID":"android.intent.extra.UID"}

class Color:
    """Write coloured text on linux terminal,
       Write normal text on Windows Command Prompt.
       Added by Luander <luander.r@samsung.com>
    """
    OKGREEN = "\033[92m"
    ENDC = "\033[0m"
    FAIL = "\033[91m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    WARNING = "\033[93m"

    def fail(self, text):
        if (os.name == "posix"):
            return self.FAIL + text + self.ENDC
        else:
            return text

    def okgreen(self, text):
        if (os.name == "posix"):
            return self.OKGREEN + text + self.ENDC
        else:
            return text

    def warning(self, text):
        if (os.name == "posix"):
            return self.WARNING + text + self.ENDC
        else:
            return text

    def okblue(self, text):
        if (os.name == "posix"):
            return self.OKBLUE + text + self.ENDC
        else:
            return text

    def header(self, text):
        if (os.name == "posix"):
            return self.HEADER + text + self.ENDC
        else:
            return text

class Response:
    """Response class"""

    def __init__(self):
        self.data = ""
        self.error = ""

    # Return if an error occurred
    def isError(self):
        if (len(self.error) > 0):
            return True
        else:
            return False

    # Return the error padded with newlines
    def getPaddedError(self):
        return "\n" + self.error.strip() + "\n"

    # Return the data padded with newlines
    def getPaddedData(self):
        return "\n" + self.data.strip() + "\n"

    # Return an error if there was one, otherwise return data (both padded with newlines)
    def getPaddedErrorOrData(self):
        if (self.isError()):
            return self.getPaddedError()
        else:
            return self.getPaddedData()

    # Return an error if there was one, otherwise return data
    def getErrorOrData(self):
        if (self.isError()):
            return self.error
        else:
            return self.data

class Session:
    """Session class"""

    def __init__(self, ip, port, direction):
        self.ip = ip
        self.port = port
        self.direction = direction
        self.socketConn = None
        # Field to manage colors on linux terminal, see #Colors for more information
        self.color = Color()

    def __del__(self):
        try:
            self.socketConn.close()
        # FIXME: Choose specific exceptions to catch
        except:
            pass

    # Returns socket connected status = True/False
    def connectSocket(self):
        try:
            self.socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.socketConn.settimeout(10.0)
            self.socketConn.connect((self.ip, self.port))
            return True
        except socket.error:
            return False

    def sendData(self, data):
        self.socketConn.sendall(data)

    def receiveData(self):
        return self.socketConn.recv(1024)

    def closeSocket(self):
        self.socketConn.close()



    #<?xml version="1.0" ?>
    #<transmission>
    #    <command>
    #        <section>provider</section>
    #        <function>query</function>
    #        <arguments>
    #            <selectionargs>ZWlzaA==</selectionargs>
    #            <selection>dzAwdHk=</selection>
    #            <projection>bG9sb2xsb2xvbG9sb2wgbG9sb2xvbG9s</projection>
    #            <URI>Y29udGVudDovL3Bldw==</URI>
    #            <sortorder>YXNj</sortorder>
    #        </arguments>
    #    </command>
    #</transmission>

    # section = section of program where command was executed from
    # function = function to execute
    # args_dict = a dict object that defines the arguments that come with the command
    # None is sent for args_dict if there are no arguments
    # Return a structured XML command
    def XMLifyCommand(self, section, function, args_dict):

        # Create document
        doc = xml.dom.minidom.Document()

        # Create root element
        root_element = doc.createElementNS("mercury-command", "transmission")

        # Create root element - command
        command_element = doc.createElementNS("mercury-command", "command")
        root_element.appendChild(command_element)

        # Create element - section
        section_element = doc.createElementNS("mercury-command", "section")
        section_element.appendChild(doc.createTextNode(section))
        command_element.appendChild(section_element)

        # Create element - function
        function_element = doc.createElementNS("mercury-command", "function")
        function_element.appendChild(doc.createTextNode(function))
        command_element.appendChild(function_element)

        # Create element - arguments
        argument_element = doc.createElementNS("mercury-command", "arguments")
        command_element.appendChild(argument_element)

        if (args_dict is not None):
        # Create elements - argument[i] by iterating through arguments that got sent to this function
            i = 1
            for key, value in args_dict.iteritems():

                # vars() creates keys with None value - this checks for a None and disregards
                if value is not None:

                    if isinstance(value, types.StringType):

                        arg_element = doc.createElementNS("mercury-command", key)
                        argument_element.appendChild(arg_element)

                        # Arguments are always base64 encoded
                        arg_element.appendChild(doc.createTextNode(base64.b64encode(value)))

                    else:

                        for val in value:

                            arg_element = doc.createElementNS("mercury-command", key)
                            argument_element.appendChild(arg_element)

                            # Arguments are always base64 encoded
                            arg_element.appendChild(doc.createTextNode(base64.b64encode(val)))

                    i = i + 1

        # Add command element to document at root level
        doc.appendChild(root_element)

        # For thorough debugging purposes
        if debug_mode:
            print doc.toprettyxml("\t", "\n", None)


        return doc.toxml()


    # Convert received XML into a Response() - very slow due to parseString
    def UnXMLifyResponse(self, xmlinput):

        # Strip the end of the response
        xmlStr = xmlinput.strip()

        # Define response
        returnValue = Response()

        # Reject malformed response - check if <transmission> tags are at start and end
        if not ((xmlStr[:36] == '<?xml version="1.0" ?><transmission>') and (xmlStr[-15:] == "</transmission>")):
            returnValue.error = "Malformed response: " + xmlStr
            return returnValue

        # Parse the XML
        doc = parseString(xmlStr)
        responses = doc.getElementsByTagName("response")
        for response in responses:
            # Get <data> text
            for data in response.getElementsByTagName("data")[0].childNodes:
                if (data.nodeType == data.TEXT_NODE):
                    lines = data.nodeValue.split("\n")
                    for line in lines:
                        if line != "":
                            returnValue.data += base64.b64decode(line)
                    break

            # Get <error> text        
            for error in response.getElementsByTagName("error")[0].childNodes:
                if (error.nodeType == error.TEXT_NODE):
                    lines = error.nodeValue.split("\n")
                    for line in lines:
                        if line != "":
                            returnValue.error += base64.b64decode(line)
                    break

        # Return error/response dict
        return returnValue



    # Convert received XML into a Response() - use regex to get data and error
    def UnXMLifyResponseRegex(self, xmlinput):

        # Strip the end of the response
        xmlStr = xmlinput.strip()

        # Define response
        returnValue = Response()

        # Reject malformed response - check if <transmission> tags are at start and end
        if not ((xmlStr[:36] == '<?xml version="1.0" ?><transmission>') and (xmlStr[-15:] == "</transmission>")):
            returnValue.error = "Malformed response: " + xmlStr
            return returnValue

        # Parse the XML using regular expressions        
        # Get text inside data and decode
        if ("<data />" not in xmlStr):
            data_regex = re.compile(r'<data>(.*)</data>', re.DOTALL)
            y = data_regex.search(xmlStr)
            for line in y.group(1).split("\n"):
                if line != "":
                    returnValue.data += base64.b64decode(line)

        # Get text inside error and decode
        if ("<error />" not in xmlStr):
            error_regex = re.compile(r'<error>(.*)</error>', re.DOTALL)
            y = error_regex.search(xmlStr)
            for line in y.group(1).split("\n"):
                if line != "":
                    returnValue.error += base64.b64decode(line)

        # Return response
        return returnValue





    # Execute a command and get a Response()
    def executeCommand(self, section, function, args_dict):
        """Send a command to the device and get a response"""

        parsedResponse = Response()

        try:

            # Open socket
            self.connectSocket()

            # Convert command to XML and send
            self.sendData(self.XMLifyCommand(section, function, args_dict) + "\n")

            # Receive until the socket is closed
            responseBuffer = ""
            receivedData = self.receiveData()
            while receivedData:
                responseBuffer = responseBuffer + receivedData
                receivedData = self.receiveData()

            # Close socket
            self.closeSocket()

            # Parse response from server
            # parsedResponse = self.UnXMLifyResponseRegex(responseBuffer) # Can use this as well but no noticeable performance gain
            parsedResponse = self.UnXMLifyResponse(responseBuffer)

        except socket.error:
            # Return that a network error occurred
            parsedResponse.error = "**Network Error** Could not reach server"
        except KeyboardInterrupt:
            # Catch Control + C to make sure that Mercury is not exited
            parsedResponse.error = "**Error** User aborted command"

        return parsedResponse



    # Download a file from the server - returns MD5 if successful - else returns error message
    def downloadFile(self, filePath, downloadFolder):

        fileSize = self.executeCommand("core", "fileSize", {'path':filePath})
        if fileSize.isError():
            return fileSize

        offset = 0

        # Create local path by joining folder and filename
        localpath = os.path.join(downloadFolder, os.path.basename(filePath))

        try:
            # Delete file
            os.unlink(localpath)
        # FIXME: Choose specific exceptions to catch
        except:
            pass

        fileContentsToMD5 = ""

        while (int(fileSize.data) > offset):

            content = self.executeCommand("core", "download", {'path':filePath, 'offset':str(offset)})

            offset += len(content.data)

            if content.isError():
                # If error occurred then return it
                return content.error
            else:
                # Write content to file
                f = open(localpath, 'ab')
                f.write(content.data)
                f.close()

                # Write to fileContents to use for MD5
                fileContentsToMD5 += content.data

        # Overwrite data with MD5 of the complete file
        content.data = md5.new(fileContentsToMD5).hexdigest()

        # Return structure
        return content

    # Upload a file to the server part by part - returns MD5 of file on server if successful - else returns error message
    def uploadFile(self, localPath, uploadFolder):

        # Create local path by joining folder and filename
        fullPath = os.path.join(uploadFolder, os.path.basename(localPath))

        # Delete existing file if there is one
        self.executeCommand("core", "delete", {'path':fullPath})

        # Read from file and send
        f = open(localPath, 'r')
        bytesRead = f.read(20480)    # Read 20KB chunks
        while len(bytesRead) > 0:
            # Send these chunks to the server
            _response = self.executeCommand("core", "upload", {'path':fullPath, 'data':bytesRead})
            bytesRead = f.read(20480)    # Read 20KB chunks
        f.close()

        # Get the MD5 of the uploaded file
        return self.executeCommand("core", "fileMD5", {'path':fullPath})
