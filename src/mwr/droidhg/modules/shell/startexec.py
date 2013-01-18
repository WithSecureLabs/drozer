from mwr.droidhg.modules import common, Module

class Start(Module, common.ClassLoader, common.Shell):

    name = "Enter into an interactive Linux shell."
    description = "Execute Linux commands in a shell in the context of Mercury."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["shell"]

    def add_arguments(self, parser):
        pass

    def execute(self, arguments):
        self.shellStart()

class Exec(Module, common.ClassLoader, common.Shell):

    name = "Execute a single Linux command."
    description = "Execute a single Linux command from the context of Mercury."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["shell"]

    def add_arguments(self, parser):
        parser.add_argument("command", nargs='?', help="the Linux command to execute")

    def execute(self, arguments):
        if arguments.command == None:
            print "No command specified."
            return
            
        self.stdout.write("%s\n" % self.shellExec(arguments.command))
