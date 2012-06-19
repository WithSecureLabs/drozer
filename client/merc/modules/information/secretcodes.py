import re
import zipfile
import cStringIO as StringIO
from merc.lib.modules import Module
from androguard.core.bytecodes import apk
import xml.etree.cElementTree as etree

class SecretCodes(Module):
    """Description: Get all secret codes from the Manifest
Credit: Mike Auty - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]

    def execute(self, session, _args):

        # Check if busybox exists
        if session.executeCommand("core", "fileSize", {'path':'/data/data/com.mwr.mercury/busybox'}).isError():
            print "\nRun setup.busybox first and then retry\n"
            return

        packagesinfo = session.executeCommand("packages", "info", {}).getPaddedErrorOrData()
        packages = re.findall('(?<=Package name: ).+', packagesinfo)

        for package in packages:
            # Get the path of the apk and add a sentinel
            path = session.executeCommand("packages", "path", {'packageName': package}).data
            path += "\n"

            apkfn = path[:path.find("\n")]

            fileSize = session.executeCommand("core", "fileSize", {'path':apkfn})
            if fileSize.isError():
                print "[" + package + "] Failed to determine filesize for APK"
            elif int(fileSize.data) > 5000000:
                print "[" + package + "] Not downloading, file's too big"
            else:
                print "[" + package + "] Downloading " + apkfn
                offset = 0
                bindata = ""
                while (int(fileSize.data) > offset):
                    content = session.executeCommand("core", "download", {'path':apkfn, 'offset':str(offset)})
                    offset += len(content.data)

                    if content.isError():
                        print "[" + package + "] Unable to download binary data for APK"
                        break
                    else:
                        bindata += content.data
                if len(bindata) == int(fileSize.data):
                    try:
                        axml = zipfile.ZipFile(StringIO.StringIO(bindata)).read('AndroidManifest.xml')
                        e = etree.fromstring(apk.AXMLPrinter(axml).getBuff())
                        etree.ElementTree(e).write("/tmp/" + package + ".xml")
                        for item in e.iter("data"):
                            if item.get('{http://schemas.android.com/apk/res/android}scheme') == 'android_secret_code':
                                print "[" + package + "] SECRET CODE: " + item.get('{http://schemas.android.com/apk/res/android}host')
                    except IOError:
                        print "[" + package + "] Failed to extract AndroidManifest.xml"
                    except Exception, e:
                        print e
