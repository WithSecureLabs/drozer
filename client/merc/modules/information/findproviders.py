from merc.lib.modules import Module
import re, os, subprocess, sys, zipfile, string, tempfile

class FindProviders(Module):
    """Description: Search for all packages matching the given filter, download them locally, extract content providers and queries them (even those with set permissions).
Credit: James Stephenson - MWR Labs (run information.findproviders --arg *filter*)"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]
        
    def execute(self, session, _arg):

        reqres = session.executeCommand("packages", "info", {"filter":_arg}).getPaddedErrorOrData()
        packlist = re.findall('(?<=APK path: ).+', reqres) 
		
        tempdir = tempfile.mkdtemp() + os.sep
			
        for curpack in packlist:
            print "Downloading: " + curpack
            response = session.downloadFile(curpack, tempdir)
            if response.isError():
                print "Error while downloading: " + response.error
                continue
            try:
                filebase = os.path.basename(curpack)
                zfile = zipfile.ZipFile(tempdir + filebase)
                zfile.extract("classes.dex", tempdir)
                extf = tempdir + "classes.dex"
            except:
                print "File classes.dex not found in archive"
                dirbase = os.path.dirname(curpack)
                fwoe = os.path.split(os.path.splitext(curpack)[0])[1]
                odexfile = dirbase + os.sep + fwoe + ".odex"
                print "Downloading: " + odexfile
                response = session.downloadFile(odexfile, tempdir)
                if response.isError():
                    print "Error downloading: " + response.error 
                    continue
                extf = tempdir + fwoe + ".odex"
            
            provlist = self.datfindstr(extf)
            
            print
            for curstr in provlist:
                foundi = re.findall('content://.+', curstr)
                for foundistr in foundi:
                    if len(foundistr) > 0:
                        print "-" * int(len(foundistr))
                        print foundistr
                        print "-" * int(len(foundistr))
                        request = {}
                        request['Uri'] = foundistr
                        request['showColumns'] = "true"
                        print session.executeCommand("provider", "query", request).getPaddedErrorOrData()
            print
        self.cleanup(tempdir)
		
    def datfindstr(self, fname):
        fhand = open(fname, "rb")
        datread = fhand.read()
        curind, compstr = 0, list()
        while curind < len(datread):
            while curind < len(datread) and datread[curind] not in string.printable:
                curind += 1
            if curind >= len(datread)-1:
                break
            nextind = curind + 1
            while nextind < len(datread) and datread[nextind] in string.printable:
                nextind += 1
            if curind == nextind:
                curind += 1
                continue
            if nextind - curind > 9:
                compstr += [datread[curind:nextind]]
            curind = nextind + 2
        fhand.close()
        return compstr
        
    def cleanup(self, tempdir):
        try:
            for cur_file in os.listdir(tempdir):
                file_path = os.path.join(tempdir, cur_file)
                print "Deleting: " + file_path
                try:
                    os.unlink(file_path)
                except:
                    pass
            print "Deleting: " + tempdir
            os.rmdir(tempdir)
        except:
            pass 
