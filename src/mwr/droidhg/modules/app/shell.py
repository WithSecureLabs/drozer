from mwr.droidhg.modules import Module

class Start(Module):

    name = "Enter into an interactive Linux shell."
    description = "Execute Linux commands in a shell in the context of droidhg."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["shell"]

    def add_arguments(self, parser):
      pass

    def execute(self, arguments):
        shell = self.new("com.mwr.droidhg.shell.Shell")

        prompt = ""
        while (prompt.upper() != "EXIT"):
            shell.write(prompt)
            response = shell.read()
            self.stdout.write(response.strip())
            self.stdout.write(" ")
            prompt = raw_input().replace("$BB", "/data/data/com.mwr.droidhg.agent/busybox")
        
        shell.close()

class Exec(Module):

    name = "Execute a Linux command."
    description = "Execute a Linux command in the context of droidhg."
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
            
        shell = self.new("com.mwr.droidhg.shell.Shell")

        shell.write(arguments.command.replace("$BB", "/data/data/com.mwr.droidhg.agent/busybox"))
        response = shell.read()
        self.stdout.write(response.strip() + "\n")
        
        shell.close()
