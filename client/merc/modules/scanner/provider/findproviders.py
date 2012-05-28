from merc.lib.modules import Module
import re, string

class ProviderScan(Module):
    """Usage: run scanner.provider.providerscan --arg <filter>
Search for all packages and tries to query respective providers, a filter can be added to restrict queries to a specific package 
Credit: Luander <luander.r@samsung.com> - Samsung SIDI
Updated by: Tyrone - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["scanner", "provider"]
        
    def execute(self, session, _arg):
        
        uris = []
        resultList = []

        # Get list of all authorities and make content uri's out of them
        providerinfo = session.executeCommand("provider", "info", {}).getPaddedErrorOrData()
        authorities = re.findall('(?<=Authority: ).+', providerinfo)
        for authority in authorities:
            uris.append("content://" + authority)
            
        # Query each found content uri     
        for uri in uris:
            
            response = session.executeCommand("provider", "query", {"Uri":uri})
            
            if response.isError():
                print "Unable to query -> " + uri 
                continue
            else:
                print session.color.red("Able to query") + " -> " + uri
                
                # Append it to result list if it is not a duplicate
                if uri not in resultList:
                    resultList.append(uri)
                    
        uris = []
        
        # Get content uris out of all packages dex and odex files
        reqres = session.executeCommand("packages", "info", {"filter":_arg}).getPaddedErrorOrData()
        packlist = re.findall('(?<=Package name: ).+', reqres)
        
        for package in packlist:
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
                                uris.append(string[string.upper().find("CONTENT"):]) 

                        # Delete classes.dex
                        session.executeCommand("core", "delete", {'path':'/data/data/com.mwr.mercury/classes.dex'})

                if (".odex" in line):
                    strings = session.executeCommand("core", "strings", {'path':line}).data

                    for string in strings.split():
                        if (("CONTENT://" in string.upper()) and ("CONTENT://" != string.upper())):
                            uris.append(string[string.upper().find("CONTENT"):])
        
            # Query each found content uri     
            for uri in uris:
                
                response = session.executeCommand("provider", "query", {"Uri":uri})
                
                # Make sure that no duplicates are queried
                if uri not in resultList:
                
                    if response.isError():
                        print "Unable to query -> " + package + " - " + uri 
                        continue
                    else:
                        print session.color.red("Able to query") + " -> " + package + " - " + uri
                        resultList.append(uri)
                else:
                    print session.color.purple("Duplicate query skipped") + " -> " + package + " - " + uri
                        
            uris = []
            
        # Generate a summary
        print session.color.blue('\nSummary of valid content URIs:\n')
        for uri in resultList:
            print uri
           
        print ""
