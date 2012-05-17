from merc.lib.modules import Module
import re, string

class ProviderScan(Module):
    """Usage: run information.providerscan --arg <filter>
    Search for all packages and tries to query respective providers, a filter can be added to restrict queries to a specific package 
    Credit: Luander <luander.r@samsung.com> - Samsung SIDI 
    """

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]
        
    def execute(self, session, _arg):

        reqres = session.executeCommand("packages", "info", {"filter":_arg}).getPaddedErrorOrData()
        packlist = re.findall('(?<=Package name: ).+', reqres)
        uris = []
        for package in packlist:
            path = session.executeCommand("packages", "path", {'packageName':package}).data
            # Iterate through paths returned
            for line in path.split():

                if (".apk" in line):
                    if session.executeCommand("core", "unzip", {'path':line, 'destination':'/data/data/com.mwr.mercury/'}).isError():
                        pass
                    else:

                        strings = session.executeCommand("core", "strings", {'path':'/data/data/com.mwr.mercury/classes.dex'}).data

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
                    
            for uri in uris:
                
                response = session.executeCommand("provider", "query", {"Uri":uri})
                
                if response.isError():
                    print "Unable to query -> " + package + " - " + uri 
                    continue
                else:
                    print session.color.fail("Able to query") + " -> " + package + " - " + uri
            uris = []
 
