import binascii

from mwr.common.list import chunk

class FileSystem(object):
    """
    Mercury Client Library: provides utility methods for interacting with the
    Agent's file system.
    """

    def cacheDir(self):
        """
        Get the full path to the Agent's cache directory.
        """

        return str(self.getContext().getCacheDir().toString())

    def deleteFile(self, source):
        """
        Delete a file from the Agent's file system.
        """

        file_io = self.new("java.io.File", source)

        if file_io.exists() == True:
            return file_io.delete()
        else:
            return None

    def downloadFile(self, source, destination):
        """
        Copy a file from the Agent's file system to the local one.
        """

        data = self.readFile(source)

        if data:
            output = open(destination, 'w')
            output.write(str(data))
            output.close()

            return len(data)
        else:
            return None

    def exists(self, source):
        """
        Test whether or not a file exists on the Agent's file system.
        """

        file_io = self.new("java.io.File", source)

        return file_io.exists()

    def fileSize(self, source):
        """
        Get the size of a file on the Agent's file system.
        """

        file_io = self.new("java.io.File", source)

        if file_io.exists() == True:
            return file_io.length()
        else:
            return None

    def md5sum(self, source):
        """
        Calculate the MD5 checksum of a file on the Agent's file system.
        """

        FileUtil = self.loadClass("common/FileUtil.apk", "FileUtil")

        file_io = self.new("java.io.File", source)

        if file_io.exists() == True:
            return FileUtil.md5sum(file_io)
        else:
            return None

    def readFile(self, source):
        """
        Read a file from the Agent's file system, and return the data.
        """

        ByteStreamReader = self.loadClass("common/ByteStreamReader.apk", "ByteStreamReader")

        file_io = self.new("java.io.File", source)

        if file_io.exists() == True:
            file_stream = self.new("java.io.FileInputStream", file_io)

            return ByteStreamReader.read(file_stream)
        else:
            return None

    def uploadFile(self, source, destination):
        """
        Copy a file from the local file system to the Agent's.
        """

        return self.writeFile(destination, open(source, 'rb').read())

    def writeFile(self, destination, data):
        """
        Write data into a file on the Agent's file system.
        """

        ByteStreamWriter = self.loadClass("common/ByteStreamWriter.apk", "ByteStreamWriter")

        file_io = self.new("java.io.File", destination)

        if file_io.exists() != True:
            file_stream = self.new("java.io.FileOutputStream", destination)

            for c in chunk(data, 500000):
                ByteStreamWriter.writeHexStream(file_stream, binascii.hexlify(c))

            file_stream.close()
            
            return len(data)
        else:
            return None
            