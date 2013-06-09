from pydiesel.reflection import ReflectionException

from drozer.modules.common import file_system, loader

class Shell(file_system.FileSystem, loader.ClassLoader):
    """
    Wrapper around the Android Shell, that allows commands to be executed.
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
        
        shell = self.new("com.mwr.jdiesel.util.Shell")
        
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
            
    def __get_variables(self):
        return "; ".join(map(lambda k: "export %s=\"%s\"" % (k, self.variables[k]), self.variables))
        
    def __send_variables(self, shell):
        shell.write(self.__get_variables())
        shell.read()
