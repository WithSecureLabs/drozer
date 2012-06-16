import re

import logging

from merc.lib.modules import Module
from merc.lib.reflect import Reflect

class Reflection(Module):
    """Description: Get all secret codes from the Manifest
Credit: Mike Auty - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["test"]

    def execute(self, session, _args):

        packagesinfo = session.executeCommand("packages", "info", {}).getPaddedErrorOrData()
        packages = re.findall('(?<=Package name: ).+', packagesinfo)

        r = Reflect(session)
        ctx = r.getctx()
        pm = ctx.getPackageManager()

        #intent = r.construct(r.resolve('android.content.Intent'), "android.provider.Telephony.SECRET_CODE")
        #receivers = pm.queryBroadcastReceivers(intent, 0)
        #print receivers.size()._native

        enddoc = startdoc = None

        for package in packages:
            print package
            am = ctx.createPackageContext(package, 0).getAssets()
            xml = am.openXmlResourceParser("AndroidManifest.xml")

            # Cache these values
            enddoc = xml.END_DOCUMENT._native
            starttag = xml.START_TAG._native

            while (xml.next()._native != enddoc):
                if xml.getEventType()._native == starttag:
                    if str(xml.getName()) == 'data':
                        attcount = int(xml.getAttributeCount()._native)
                        if attcount == 2:
                            if str(xml.getAttributeValue(0)) == 'android_secret_code':
                                print "    " + str(xml.getAttributeValue(1))
