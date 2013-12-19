import os

from drozer.modules import common, Module

class Start(Module, common.Shell):

    name = "Enter into an interactive Linux shell."
    description = "Execute Linux commands in a shell in the context of drozer."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["shell"]

    def add_arguments(self, parser):
        pass

    def execute(self, arguments):
        self.push_completer(self.null_complete, os.path.sep.join([os.path.expanduser("~"), ".drozer_shrc"]))
        self.shellStart()
        self.pop_completer()

class Exec(Module, common.Shell):

    name = "Execute a single Linux command."
    description = "Execute a single Linux command from the context of drozer."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "BSD (3 clause)"
    path = ["shell"]

    def add_arguments(self, parser):
        parser.add_argument("command", help="the Linux command to execute")

    def execute(self, arguments):
        if arguments.command == None:
            print "No command specified."
            return
            
        self.stdout.write("%s\n" % self.shellExec(arguments.command))
