import sys

from mwr.common import cli, console

from drozer.shellcode import builder

class ShellCodeManager(cli.Base):
    """
    drozer shellcode COMMAND [OPTIONS]
    
    A utility for crafting shellcode to deliver drozer onto an Android device.
    """
    
    def __init__(self):
        cli.Base.__init__(self)
    
    def args_for_build(self):
        self._parser.add_argument("module", help="specify the shellcode module to use")
        self._parser.add_argument("--format", choices=builder.Formats, default=builder.Formats[0], help="specify the format for the shellcode (Raw bytes, Unicode or heX string)")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]", help="specify the address and port of the drozer server")
        
    def do_build(self, arguments):
        """build some shellcode"""
        
        print builder.Builder().build(arguments.module, arguments)

    def args_for_info(self):
        self._parser.add_argument("module", help="specify the shellcode module to use")
        
    def do_info(self, arguments):
        """prints information about a shellcode module"""
        
        module = builder.Builder().module(arguments.module)
        
        print module.usage.formatted_description()
        
    def do_list(self, arguments):
        """list the available shellcode modules"""
        
        shellcode_builder = builder.Builder() 
        
        sys.stdout.write(console.format_dict(dict(map(lambda m: [m, shellcode_builder.module(m).name], shellcode_builder.modules()))) + "\n")
        