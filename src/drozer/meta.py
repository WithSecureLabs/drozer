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
version = Version("2.3.4", "2015-02-19")

contact = "drozer@mwrinfosecurity.com"
description = "The Leading Android Security Testing Framework"
license = "BSD (3 clause)"
keywords = "drozer android security framework"
url = "http://mwr.to/drozer"

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
