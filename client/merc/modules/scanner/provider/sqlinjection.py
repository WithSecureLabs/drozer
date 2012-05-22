from merc.lib.modules import Module
import re, string

class sqlinjection(Module):
    """Description: Find SQL injection vulnerabilities in content providers
Credit: Rob M && Tyrone Erasmus - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "provider"]
        
    def execute(self, session, _arg):
        
        queryList = []
        projectionList = []
        selectionList = []
        
        print "\n[*] Getting a list of all content uri's to query..."
        print "\t- Fetching authorities..."

        # Get list of all authorities and make content uri's out of them
        providerinfo = session.executeCommand("provider", "info", {}).getPaddedErrorOrData()
        authorities = re.findall('(?<=Authority: ).+', providerinfo)
        for authority in authorities:
            queryList.append("content://" + authority)
            
        print "\t- Digging deep..."
        
        # Get list of all packages
        packagesinfo = session.executeCommand("packages", "info", {}).getPaddedErrorOrData()
        packages = re.findall('(?<=Package name: ).+', packagesinfo)
        for package in packages:
            path = session.executeCommand("packages", "path", {'packageName':package}).data
            
            # Iterate through paths returned
            for line in path.split():

                if (".apk" in line):
                    if session.executeCommand("core", "unzip", {'path':line, 'destination':'/data/data/com.mwr.mercury/'}).isError():
                        pass
                    else:

                        strings = session.executeCommand("provider", "finduri", {'path':'/data/data/com.mwr.mercury/classes.dex'}).data

                        for string in strings.split():
                            if (("CONTENT://" in string.upper()) and ("CONTENT://" != string.upper())):
                                queryList.append(string[string.upper().find("CONTENT"):]) 

                        # Delete classes.dex
                        session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})

                if (".odex" in line):
                    strings = session.executeCommand("provider", "finduri", {'path':line}).data

                    for string in strings.split():
                        if (("CONTENT://" in string.upper()) and ("CONTENT://" != string.upper())):
                            queryList.append(string[string.upper().find("CONTENT"):])
                    
                    
        print "[*] Checking for SQL injection...\n"
        
        # Check all found URI's for injection in projection and selection
        for uri in queryList:
            
            projectioninject = session.executeCommand("provider", "query", {"Uri":uri, "projection":"'"})
            selectioninject = session.executeCommand("provider", "query", {"Uri":uri, "selection":"'"})
            
            if "unrecognized token" in projectioninject.error:
                print "Injection point:", session.color.fail("projection") + " - " + uri
                
                if uri not in projectionList:
                        projectionList.append(uri)
            else:
                if "unrecognized token:" in selectioninject.error:
                    print "Injection point:", session.color.warning("selection") + " - " + uri
                    
                    if uri not in selectionList:
                        selectionList.append(uri)
                        
        # Generate a summary
        print session.color.okblue('\n[*] Summary\n    -------')
        print session.color.fail("\nInjection in projection:")
        for uri in projectionList:
            print uri
            
        print session.color.fail("\nInjection in selection:")
        for uri in selectionList:
            print uri
        print ""
