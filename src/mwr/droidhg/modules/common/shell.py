from pydiesel.reflection import ReflectionException

from mwr.droidhg.modules.common import file_system, loader

class Shell(file_system.FileSystem, loader.ClassLoader):
    """
    Mercury Client Library: provides a wrapper around the Android Shell, allowing
    commands to be executed.
    """

    def shellExec(self, command):
        """
        Execute a single Shell command on the Agent.
        """

        ShellWrapper = self.loadClass("common/ShellWrapper.apk", "ShellWrapper")

        return ShellWrapper.execute("%s; %s" % (self.__get_variables(), command))
    
    def shellStart(self, command=""):
        """
        Create an interactive Linux shell on the Agent, optionally passing the
        first command.
        """
        
        shell = self.new("com.mwr.droidhg.shell.Shell")
        
        try:
            if shell.valid():
                self.__send_variables(shell)
                    
            while shell.valid():
                shell.write(command)
                response = shell.read()
                self.stdout.write(response.strip())
                if not shell.valid():
                    break
                self.stdout.write(" ")
                command = raw_input()
            
            shell.close()
        except ReflectionException as e:
            if e.message == "valid for class com.mwr.droidhg.shell.Shell":
                self.shellStartCompatibility(command)
            else:
                raise
    
    def shellStartCompatibility(self, command=""):
        shell = self.new("com.mwr.droidhg.shell.Shell")
        
        self.__send_variables(shell)
        
        while command.upper() != "EXIT":
            shell.write(command)
            response = shell.read()
            self.stdout.write(response.strip())
            self.stdout.write(" ")
            command = raw_input()
            
    def __get_variables(self):
        return "; ".join(map(lambda k: "export %s=\"%s\"" % (k, self.variables[k]), self.variables))
        
    def __send_variables(self, shell):
        shell.write(self.__get_variables())
        shell.read()