from mwr.droidhg.modules import common, Module

class Download(Module, common.ClassLoader, common.FileSystem):

    name = "Download a File"
    description = "Download a file from the Android device to your PC"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="?")
        parser.add_argument("destination", nargs="?")

    def complete(self, text, line, begidx, endidx):
        if not " " in line or begidx < line.index(" "):
            return common.path_completion.on_agent(text)
        else:
            return common.path_completion.on_console(text)

    def execute(self, arguments):
        length = self.downloadFile(arguments.source, arguments.destination)
        
        if length != None:
            self.stdout.write("Read %d bytes\n" % length)
        else:
            self.stderr.write("Could not download file. The file may not exist.\n")

class Size(Module, common.FileSystem):

    name = "Size of File"
    description = "Calculate the size of file on the Android device"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("target", nargs="?")

    def complete(self, text, line, begidx, endidx):
        return common.path_completion.on_agent(text)

    def execute(self, arguments):
        size = self.fileSize(arguments.target)

        if size != None:
            if size > 1024:
                self.stdout.write("%s (%d bytes)\n" % (self.format_file_size(size), size))
            else:
                self.stdout.write("%s\n" % (self.format_file_size(size)))
        else:
            self.stderr.write("Could not determine file size. The file may not exist.\n")

class MD5Sum(Module, common.ClassLoader, common.FileSystem):

    name = "md5 Checksum of File"
    description = "md5 Checksum of File"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("target", nargs="?")

    def complete(self, text, line, begidx, endidx):
        return common.path_completion.on_agent(text)

    def execute(self, arguments):
        md5sum = self.md5sum(arguments.target)

        if md5sum != None:
            self.stdout.write("%s\n" % md5sum)
        else:
            self.stderr.write("Could not calculate the md5 checksum. The file may not exist.\n")

class Upload(Module, common.ClassLoader, common.FileSystem):

    name = "Upload a File"
    description = "Upload a file from your PC to the Android device"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("source", nargs="?")
        parser.add_argument("destination", nargs="?")

    def complete(self, text, line, begidx, endidx):
        if not " " in line or begidx < line.index(" "):
            return common.path_completion.on_console(text)
        else:
            return common.path_completion.on_agent(text)

    def execute(self, arguments):
        length = self.uploadFile(arguments.source, arguments.destination)

        if length != None:
            self.stdout.write("Written %d bytes\n" % length)
        else:
            self.stderr.write("Could not upload file.\n")
