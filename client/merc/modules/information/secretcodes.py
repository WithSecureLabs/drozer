
import os
import re
import base64

from merc.lib.modules import Module
from merc.lib.reflect import Reflect

class SecretCodes(Module):
    """Description: Get all secret codes from the Manifest
Credit: Mike Auty - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["information"]

    def execute(self, session, args):
        """ Provides an example run using the reflection classloader
        
            To create the jar file, compile the file.class then issue the following:
            dx --dex --output file.apk file.class
        """

        packagesinfo = session.executeCommand("packages", "info", {}).getPaddedErrorOrData()
        packages = re.findall('(?<=Package name: ).+', packagesinfo)

        f = open(os.path.join(os.path.dirname(__file__), "secretcodes.apk"), "rb")
        classdata = f.read()
        f.close()

        r = Reflect(session)
        classloader = r.classload(base64.b64encode(classdata))

        cls = classloader.loadClass("ManifestReader")

        ctx = r.getctx()
        obj = r.construct(cls)
        for package in packages:
            print "Package:", package
            codelist = obj.main(ctx, package)
            for i in codelist:
                print "  ", i
