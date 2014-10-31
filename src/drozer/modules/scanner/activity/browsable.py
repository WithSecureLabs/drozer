from drozer.modules import common, Module
import xml.etree.ElementTree as ET

class Browsable(Module, common.PackageManager, common.Assets):
    name = "Get all BROWSABLE activities that can be invoked from the web browser"
    description = "Get all BROWSABLE activities that can be invoked from the web browser through the use of a custom data handler. This can indicate the presence of an entry point into application code from a web browser."
    examples = """
dz> run scanner.activity.browsable
Package: com.android.contacts
  Invocable URIs:
    tel://
  Classes:
    .activities.PeopleActivity
    com.android.contacts.NonPhoneActivity

Package: com.android.calendar
  Invocable URIs:
    http://www.google.com/calendar/event (PATTERN_PREFIX)
  Classes:
    GoogleCalendarUriIntentFilter

Package: com.android.browser
  Invocable URIs:
    http://
  Classes:
    BrowserActivity

Package: com.android.music
  Invocable URIs:
    http://
    content://
  Classes:
    AudioPreview

Package: com.android.mms
  Invocable URIs:
    sms://
    mms://
  Classes:
    .ui.ComposeMessageActivity
"""
    author = "Tyrone (@mwrlabs)"
    date = "2014-10-31"
    license = "BSD (3-clause)"
    path = ["scanner", "activity"]
    permissions = ["com.mwr.dz.permissions.GET_CONTEXT"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", help="specify a package to search")
        parser.add_argument("-f", "--filter", action="store", dest="filter", default=None, help="filter term")

    def execute(self, arguments):

        # One or all packages
        if arguments.package != None:
            packages = [self.packageManager().getPackageInfo(arguments.package, 0)]
        else:
            packages = self.packageManager().getPackages()

        for package in packages:
            try:
                returned = self.getBrowsable(package.packageName)
                if (len(returned['uris']) > 0) or (len(returned['classNames']) > 0):
                    if arguments.filter:
                        # Make sure filter value is in returned schemes or package name
                        if arguments.filter in ''.join(returned['uris']) or arguments.filter in ''.join(returned['classNames']) or arguments.filter in package.packageName:
                            showResult = True
                        else:
                            showResult = False
                    else:
                        showResult = True

                    if showResult:
                        self.stdout.write("Package: %s\n" % str(package.packageName))
                        self.stdout.write("  Invocable URIs:\n")
                        for i in returned['uris']:
                            self.stdout.write("    %s\n" % str(i))
                        self.stdout.write("  Classes:\n")
                        for i in returned['classNames']:
                            self.stdout.write("    %s\n" % str(i))
                        self.stdout.write("\n")
            except Exception, e:
                pass # amazing error checking
            
    # Get browsable activities that use data attribute
    def getBrowsable(self, packagename):
        uris = []
        classNames = []
        manifest = self.getAndroidManifest(packagename)
        root = ET.fromstring(manifest)

        for activity in root.find('application').findall('activity'):
            for intentfilter in activity.findall('intent-filter'):
                final = ""
                foundBrowsable = False
                category = intentfilter.findall('category')
                for cat in category:
                    if cat.get('name') == "android.intent.category.BROWSABLE":
                        foundBrowsable = True

                if foundBrowsable:
                    name = activity.get('name')
                    if name not in classNames:
                        classNames.append(name)

                    data = intentfilter.find('data')
                    if data is not None:
                        final += data.get('scheme', '')
                        final += "://"
                        final += data.get('host', '')
                        final += ":" + data.get('port', '') if len(data.get('port', '')) > 0 else ""
                        final += data.get('path', '') + " (PATTERN_LITERAL)" if len(data.get('path', '')) > 0 else ""
                        final += data.get('pathPrefix', '') + " (PATTERN_PREFIX)" if len(data.get('pathPrefix', '')) > 0 else ""
                        final += data.get('pathPattern', '') + " (PATTERN_SIMPLE_GLOB)" if len(data.get('pathPattern', '')) > 0 else ""

                        # Test for duplicates and ignore intent filters that only use mime types
                        if final not in uris and final != "://":
                            uris.append(final)
        return {"uris": uris, "classNames": classNames}
