from itertools import izip

class ShellCode(object):
    
    def append(self, byte_or_bytes):
        """
        Add a byte or list of bytes to the current shell code. 
        """
        
        if hasattr(byte_or_bytes, '__iter__'):
            self.__shell_code.extend(byte_or_bytes)
        else:
            self.__shell_code.append(byte_or_bytes)

    def asHex(self):
        return "".join(map(lambda b: "\\x%0.2X" % b, self.__shell_code))

    def asRaw(self):
        return "".join(map(lambda b: "%s" % chr(b), self.__shell_code))

    def asUnicode(self):
        shell_code = len(self.__shell_code) % 2 == 0 and self.__shell_code or self.__shell_code + [0]
        
        return "".join(map(lambda bs: "\\u%0.2X%0.2X" % (bs[1], bs[0]), izip(*[iter(shell_code)] * 2)))

    def execute(self, arguments):
        """
        Implementation of the Module execute() method. Requests that the shell
        code is generated, before formatting it and printing to stdout.
        """
        
        self.__shell_code = []
        
        if not isinstance(arguments.server, tuple):
            arguments.server = self.parse_server(arguments.server)
        
        self.generate(arguments)
        
        if arguments.format == "R":
            return self.asRaw()
        elif arguments.format == "U":
            return self.asUnicode()
        elif arguments.format == "X":
            return self.asHex()

    def hexifyInetAddr(self, inet_addr):
        return map(lambda s: int(s), inet_addr.split("."))
    
    def hexifyInt32(self, int32):
        byte = "%.4X" % int32
        
        return [int("0x" + byte[0:2], 16), int("0x" + byte[2:4], 16)]
    
    def hexifyNull(self):
        return 0x00
    
    def hexifyString(self, string):
        return map(lambda c: ord(c), string)
    
    def parse_server(self, server_string):
        if server_string == None:
            return ("10.0.2.2", 31415)
        elif server_string.find(":") == -1:
            return (server_string, 31415)
        else:
            (host, port) = server_string.split(":", 1)
            
            return (host, int(port))
