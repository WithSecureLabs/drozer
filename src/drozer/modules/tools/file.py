from drozer.modules import common, Module

class Download(Module, common.ClassLoader, common.FileSystem):

    name = "Download a File"
    description = "Download a file from the Android device to your PC"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("source")
        parser.add_argument("destination")

    def execute(self, arguments):
        length = self.downloadFile(arguments.source, arguments.destination)
        
        if length != None:
            self.stdout.write("Read %d bytes\n" % length)
        else:
            self.stderr.write("Could not download file. The file may not exist.\n")
    
    def get_completion_suggestions(self, action, text, line, **kwargs):
        if action.dest == "source":
            return common.path_completion.on_agent(text, self)
        elif action.dest == "destination":
            return common.path_completion.on_console(text)

class Size(Module, common.FileSystem):

    name = "Get size of file"
    description = "Calculate the size of file on the Android device"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("target")

    def execute(self, arguments):
        size = self.fileSize(arguments.target)

        if size != None:
            if size > 1024:
                self.stdout.write("%s (%d bytes)\n" % (self.format_file_size(size), size))
            else:
                self.stdout.write("%s\n" % (self.format_file_size(size)))
        else:
            self.stderr.write("Could not determine file size. The file may not exist.\n")

    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "target":
            return common.path_completion.on_agent(text)

class MD5Sum(Module, common.ClassLoader, common.FileSystem):

    name = "Get md5 Checksum of file"
    description = "md5 Checksum of File"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("target")

    def execute(self, arguments):
        md5sum = self.md5sum(arguments.target)

        if md5sum != None:
            self.stdout.write("%s\n" % md5sum)
        else:
            self.stderr.write("Could not calculate the md5 checksum. The file may not exist.\n")

    def get_completion_suggestions(self, action, text, line, **kwargs):
        if action.dest == "target":
            return common.path_completion.on_agent(text)

class Upload(Module, common.ClassLoader, common.FileSystem):

    name = "Upload a File"
    description = "Upload a file from your PC to the Android device"
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["tools", "file"]

    def add_arguments(self, parser):
        parser.add_argument("source")
        parser.add_argument("destination")
        

    def execute(self, arguments):
        length = self.uploadFile(arguments.source, arguments.destination)

        if length != None:
            self.stdout.write("Written %d bytes\n" % length)
        else:
            self.stderr.write("Could not upload file.\n")

    def get_completion_suggestions(self, action, text, line, **kwargs):
        if action.dest == "source":
            return common.path_completion.on_console(text)
        elif action.dest == "destination":
            return common.path_completion.on_agent(text, self)
            
