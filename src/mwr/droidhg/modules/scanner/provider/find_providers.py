from mwr.cinnibar.reflection import ReflectionException

from mwr.droidhg.modules import common, Module

class FindUris(Module, common.ClassLoader, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile):

    name = "Search for content providers that can be queried from our context."
    description = "Search for content providers that can be queried from our context."
    examples = "run scanner.provider.findproviders"
    author = "Luander (luander.r@samsung.com)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["scanner", "provider"]

    def add_arguments(self, parser):
        parser.add_argument("-a", "--package", help="specify a package to search")
    
    def execute(self, arguments):
        accessible_uris = set([])
        
        # attempt to query each content uri
        for uri in self.findAllContentUris(arguments.package):
            try:
                response = self.contentResolver().query(uri)
            except ReflectionException:
                response = None
            
            if response == None:
                self.stdout.write("Unable to Query  %s\n" % uri)
            else:
                self.stdout.write("Able to Query    %s\n" % uri)

                accessible_uris.add(uri)

        # print out a report
        self.stdout.write("Accessible content URIs:\n")
        for uri in accessible_uris:
            self.stdout.write("  %s\n" % uri)
