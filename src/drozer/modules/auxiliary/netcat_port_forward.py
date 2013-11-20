from drozer.modules import common, Module
import thread

class NCPortForward(Module, common.BusyBox):

    name = "Start a port forward using netcat"
    description = ""
    examples = """dz> run auxiliary.ncportforward -rp 1234 -rh 192.168.5.50
    Starting port forward on 4444 -> 192.168.5.50:1234 ...

    Now use `adb forward tcp:4444 tcp:4444` and connect to localhost:4444 ..."""
    author = "Ben Campbell"
    date = "2013-11-19"
    license = "BSD (3 clause)"
    path = ["auxiliary"]

    def add_arguments(self, parser):
        parser.add_argument("-lp", "--local-port", default=4444, help="the port (on device) to start the port forward on")
        parser.add_argument("-rh", "--remote-host", help="the remote host to connect to")
        parser.add_argument("-rp", "--remote-port", help="the port to connect to")
    
    def execute(self, arguments):
        if not self.isBusyBoxInstalled:
            self.stderr.write("This command requires BusyBox to complete. Run tools.setup.busybox and then retry.\n")
            return None
        
        lp = str(arguments.local_port)
        rp = str(arguments.remote_port)
        rh = arguments.remote_host
        self.stdout.write("Starting port forward on %s -> %s:%s ...\n" % (lp, rh, rp))
        self.stdout.write("Now use `adb forward tcp:%s tcp:%s` and connect to localhost:%s ...\n" % (lp, lp, lp))
        command = "nc -l -p %s -e busybox nc %s %s &" % (lp, rh, rp)
        self.busyBoxExec(command)

    def usage(self):
        """
        Forward a port on the device to a remote host
        """
        
        return """
<p>PortForwarder forwards a port on the device to a remote host and port.</p>
<p>With PortForwarder (and `adb forward`, you can forward traffic through the android device. This can be useful to access internal
network interfaces which aren't exposed to adb.</p>"""
