from mwr.cinnibar.reflection import ReflectionException

from mwr.droidhg.modules.common.package_manager import PackageManager

class Provider(object):
    """
    Mercury Client Library: provides utility methods for interacting with content
    providers.
    """

    __content_resolver_proxy = None

    class ContentResolverProxy(object):
        """
        Wrapper for the native Java ContentResolver object, which provides
        convenience methods for constructing some requests and handling some of
        the return types.
        """

        def __init__(self, module):
            self.__module = module
            self.__content_resolver = module.getContext().getContentResolver()

        def delete(self, uri, selection, selectionArgs):
            """
            Delete from a content provider, given filter conditions.
            """
            client = self.__content_resolver.acquireUnstableContentProviderClient(self.parseUri(uri))
            returnVal = None
            try:
                returnVal = client.delete(self.parseUri(uri), selection, selectionArgs)
            except ReflectionException as e:
                if e.message.startswith("Unknown Exception"):
                    raise ReflectionException("Error during provider operation. It looks like the Content Provider crashed.")
                else:
                    raise
            client.release()

            return returnVal

        def insert(self, uri, contentValues):
            """
            Insert contentValues into a content provider.
            """
            client = self.__content_resolver.acquireUnstableContentProviderClient(self.parseUri(uri))
            returnVal = None
            try:
                returnVal = client.insert(self.parseUri(uri), contentValues)
            except ReflectionException as e:
                client.release()
                if e.message.startswith("Unknown Exception"):
                    raise ReflectionException("Error during provider operation. It looks like the Content Provider crashed.")
                else:
                    raise
            client.release()

            return returnVal

        def parseUri(self, uri):
            """
            Convert a String into a Java URI Object.
            """

            return self.__module.klass("android.net.Uri").parse(uri)

        def query(self, uri, projection=None, selection=None, selectionArgs=None, sortOrder=None):
            """
            Query a database-backed content provider, with an optional projection,
            filter conditions and sort order.
            """

            client = self.__content_resolver.acquireUnstableContentProviderClient(self.parseUri(uri))
            returnCursor = None
            try:
                returnCursor = client.query(self.parseUri(uri), projection, selection, selectionArgs, sortOrder)
            except ReflectionException as e:
                client.release()
                if e.message.startswith("Unknown Exception"):
                    raise ReflectionException("Error during provider operation. It looks like the Content Provider crashed.")
                else:
                    raise
            client.release()

            return returnCursor
            

        def read(self, uri):
            """
            Read a file from a file-system-based content provider.
            """

            ByteStreamReader = self.__module.loadClass("common/ByteStreamReader.apk", "ByteStreamReader")

            client = self.__content_resolver.acquireUnstableContentProviderClient(self.parseUri(uri))
            if client == None:
                return None

            fileDescriptor = None

            try:
                fileDescriptor = client.openFile(self.parseUri(uri), "r")
            except ReflectionException as e:
                client.release()
                if e.message.startswith("Unknown Exception"):
                    raise ReflectionException("Error during provider operation. It looks like the Content Provider crashed.")
                else:
                    raise

            client.release()

            if fileDescriptor == None:
                return None

            return str(ByteStreamReader.read(self.__module.new("java.io.FileInputStream", fileDescriptor.getFileDescriptor())))

        def update(self, uri, contentValues, selection, selectionArgs):
            """
            Update records in a content provider with contentValues.
            """
            client = self.__content_resolver.acquireUnstableContentProviderClient(self.parseUri(uri))
            returnVal = None
            try:
                returnVal = client.update(self.parseUri(uri), contentValues, selection, selectionArgs)
            except ReflectionException as e:
                client.release()
                if e.message.startswith("Unknown Exception"):
                    raise ReflectionException("Error during provider operation. It looks like the Content Provider crashed.")
                else:
                    raise

            client.release()
            
            return returnVal
            
    def contentResolver(self):
        """
        Get a ContentResolver to interact with a ContentProvider.
        """

        if self.__content_resolver_proxy == None:
            self.__content_resolver_proxy = Provider.ContentResolverProxy(self)

        return self.__content_resolver_proxy

    def findAllContentUris(self, package):
        """
        Search a package (or packages) for content providers, by searching the
        manifest and looking for content:// paths in the binary.
        """

        uris = set([])

        # collect content uris by enumerating all authorities, and uris detected
        # in the source
        
        if package == None:
            for package in self.packageManager().getPackages(PackageManager.GET_PROVIDERS):
                try:
                    uris = uris.union(self.__search_package(package))
                except ReflectionException as e:
                    if "java.util.zip.ZipException: unknown format" in e.message:
                        self.stderr.write("Skipping package %s, because we cannot unzip it..." % package.applicationInfo.packageName)
                    else:
                        raise
        else:
            package = self.packageManager().getPackageInfo(package, PackageManager.GET_PROVIDERS)

            try:
                uris = uris.union(self.__search_package(package))
            except ReflectionException as e:
                if "java.util.zip.ZipException: unknown format" in e.message:
                    self.stderr.write("Skipping package %s, because we cannot unzip it..." % package.applicationInfo.packageName)
                else:
                    raise

        return uris
        
    def findContentUris(self, package):
        """
        Search a package for content providers, by looking for content:// paths
        in the binary.
        """

        self.deleteFile("/".join([self.cacheDir(), "classes.dex"]))

        content_uris = []
        for path in self.packageManager().getSourcePaths(package):
            strings = []

            if ".apk" in path:
                dex_file = self.extractFromZip("classes.dex", path, self.cacheDir())

                if dex_file != None:
                    strings = self.getStrings(dex_file.getAbsolutePath())

                    dex_file.delete()
                
                # look for an odex file too, because some system packages do not
                # list these in sourceDir
                strings += self.getStrings(path.replace(".apk", ".odex")) 
            elif (".odex" in path):
                strings = self.getStrings(path)
            
            content_uris.append((path, filter(lambda s: ("CONTENT://" in s.upper()) and ("CONTENT://" != s.upper()), strings)))

        return content_uris

    def getResultSet(self, cursor):
        """
        Get a result set from a database cursor, as a 2D array.
        """

        rows = []
        blob_type = self.klass("android.database.Cursor").FIELD_TYPE_BLOB

        if cursor != None:
            columns = cursor.getColumnNames()
            rows.append(columns)

            cursor.moveToFirst()
            while cursor.isAfterLast() == False:
                row = []

                for i in xrange(len(columns)):
                    if(cursor.getType(i) == blob_type):
                        row.append("%s (Base64-encoded)" % (cursor.getBlob(i).base64_encode()))
                    else:
                        row.append(cursor.getString(i))

                rows.append(row)

                cursor.moveToNext()

            return rows
        else:
            return None

    def __search_package(self, package):
        """
        Search a package's manifest and binary for content provider URIs, and
        create a union set of them.
        """

        print "Scanning %s..." % package.packageName

        uris = set([])

        if package.providers != None:
            for provider in package.providers:
                if provider.authority != None:
                    uris.add("content://%s" % provider.authority)
        for (path, content_uris) in self.findContentUris(package.packageName):
            if len(content_uris) > 0:
                for uri in content_uris:
                    uris.add(uri[uri.upper().find("CONTENT"):])

        return uris
        
