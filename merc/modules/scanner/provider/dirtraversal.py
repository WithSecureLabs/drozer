from merc.lib.modules import Module
import re

class DirTraversal(Module):

    """Description: Checks all content providers for basic directory traversal vulnerabilities
Credit: Nils - MWR Labs
Updated by: Tyrone - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "provider"]

    def execute(self, session, _arg):
        
        # Create file to be traversed to
        session.executeCommand("shell", "executeSingleCommand", {"args":"echo testing > /data/data/com.mwr.mercury/traverse"}).getPaddedErrorOrData()
        
        # Get all authorities
        info = session.executeCommand("provider", "info", None).getPaddedErrorOrData()
        auths = re.findall('(?<=Authority: ).+', info)

        vuln = []
        for a in auths:
            print("Checking " + a)
            request = {'Uri': "content://" + a + "/../../../../../../../../../../../../../../../../data/data/com.mwr.mercury/traverse"}
            
            response = session.executeCommand("provider", "read", request)

            if not ((response.isError() or len(response.data) == 0)):
                print session.color.red(a + " is vulnerable to directory traversal!")
                vuln.append(a)

        print ""

        if len(vuln) > 0:
            print session.color.red("Vulnerable providers:")
            for v in vuln:
                print v
        else:
            print session.color.green("No vulnerable providers found!")
            

        print ""
        
        # Remove traversal file
        session.executeCommand("shell", "executeSingleCommand", {"args":"rm /data/data/com.mwr.mercury/traverse"}).getPaddedErrorOrData()

