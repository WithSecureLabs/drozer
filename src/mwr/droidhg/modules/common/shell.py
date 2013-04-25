from mwr.cinnibar.reflection import ReflectionException

class Shell(object):
    """
    Mercury Client Library: provides a wrapper around the Android Shell, allowing
    commands to be executed.
    """

    def shellExec(self, command):
        """
        Execute a single Shell command on the Agent.
        """

        ShellWrapper = self.loadClass("common/ShellWrapper.apk", "ShellWrapper")

        return ShellWrapper.execute(command.replace("$BB", "/data/data/com.mwr.droidhg.agent/busybox"))
    
    def shellStart(self, command=""):
        """
        Create an interactive Linux shell on the Agent, optionally passing the
        first command.
        """
        
        shell = self.new("com.mwr.droidhg.shell.Shell")
        
        try:
            while shell.valid():
                shell.write(command)
                response = shell.read()
                self.stdout.write(response.strip())
                if not shell.valid():
                    break
                self.stdout.write(" ")
                command = raw_input().replace("$BB", "/data/data/com.mwr.droidhg.agent/busybox")
            
            shell.close()
        except ReflectionException as e:
            if e.message == "valid for class com.mwr.droidhg.shell.Shell":
                self.shellStartCompatibility(command)
            else:
                raise
    
    def shellStartCompatibility(self, command=""):
        shell = self.new("com.mwr.droidhg.shell.Shell")
        
        while command.upper() != "EXIT":
            shell.write(command)
            response = shell.read()
            self.stdout.write(response.strip())
            self.stdout.write(" ")
            command = raw_input().replace("$BB", "/data/data/com.mwr.droidhg.agent/busybox")
            