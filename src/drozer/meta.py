from urllib2 import HTTPError, URLError, urlopen, Request
from xml.etree import ElementTree

class Version:

    def __init__(self, version, date):
        major, minor, patch = version.split(".")

        self.date = date
        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)

    def __eq__(self, other):
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __gt__(self, other):
        return self.major > other.major or \
            self.major == other.major and self.minor > other.minor or \
            self.major == other.major and self.minor == other.minor and self.patch > other.patch

    def __lt__(self, other):
        return self.major < other.major or \
            self.major == other.major and self.minor < other.minor or \
            self.major == other.major and self.minor == other.minor and self.patch < other.patch

    def __str__(self):
        return "%d.%d.%d" % (self.major, self.minor, self.patch)


name = "drozer"
vendor = "MWR InfoSecurity"
version = Version("2.4.4", "2017-11-09")

contact = "drozer@mwrinfosecurity.com"
description = "The Leading Android Security Testing Framework"
license = "BSD (3 clause)"
keywords = "drozer android security framework"
url = "http://mwr.to/drozer"

long_description = '''
drozer (formerly Mercury) is the leading security testing framework for Android.

drozer allows you to search for security vulnerabilities in apps and devices by assuming the role of an app and interacting with the Dalvik VM, other apps' IPC endpoints and the underlying OS.

drozer provides tools to help you use, share and understand public Android exploits. It helps you to deploy a drozer Agent to a device through exploitation or social engineering. Using weasel (MWR's advanced exploitation payload) drozer is able to maximise the permissions available to it by installing a full agent, injecting a limited agent into a running process, or connecting a reverse shell to act as a Remote Access Tool (RAT).

drozer is open source software, maintained by MWR InfoSecurity, and can be downloaded from: http://mwr.to/drozer
'''

def latest_version():
    try:
        xml = urlopen(Request("https://www.mwrinfosecurity.com/products/drozer/community-edition/manifest.xml", None, {"user-agent": "drozer: %s" % version}), None, 1).read()
        doc = ElementTree.fromstring(xml)
        
        return max(map(lambda n: Version(n.text[1:], n.attrib['release_date']), doc.findall('version')))
    except HTTPError:
        return None
    except URLError:
        return None

def print_version():
    print "%s %s\n" % (name, version)
