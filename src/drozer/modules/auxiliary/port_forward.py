from drozer.modules import common, Module
from pydiesel.reflection import ReflectionException
import binascii, thread, socket, select

class PortForward(Module, common.ClassLoader):

    name = "Start a port forward"
    description = ""
    examples = """dz> run auxiliary.portforward -rh 192.168.5.1 -rp 5555 -lp 4444
    Tunneling :4444 -> 192.168.5.1:5555
    dz> Established tunnel to 192.168.5.1:5555"""
    author = "Ben Campbell"
    date = "2013-11-19"
    license = "BSD (3 clause)"
    path = ["auxiliary"]

    def add_arguments(self, parser):
        parser.add_argument("-rh", "--remote-host", help="the remote host to connect to")
        parser.add_argument("-rp", "--remote-port", help="the remote port to connect to")
        parser.add_argument("-lp", "--local-port", default=4444, help="the local port to listen on")


    def server_thread(self, *settings):
        local_port = settings[0]
        remote_host = settings[1]
        remote_port = settings[2]

        dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            dock_socket.bind(('', local_port))
        except socket.error as e:
            if e.errno == 10048:
                self.stdout.write("Error: Local port is in use: %s\n" %(local_port))
                return None
            else:
                raise
                
        dock_socket.listen(5)
        self.stdout.write("Tunneling :%s -> %s:%s\n" % (local_port, remote_host, remote_port))
        client_socket = dock_socket.accept()[0]
        thread.start_new_thread(self.forwarder,(client_socket, remote_host, remote_port))

    def forwarder(self, client_socket, remote_host, remote_port):
        byte_stream_writer = self.loadClass("common/ByteStreamWriter.apk", "ByteStreamWriter")
        byte_stream_reader = self.loadClass("common/ByteStreamReader.apk", "ByteStreamReader")

        try:
            java_socket = self.new("java.net.Socket", remote_host, remote_port)
        except ReflectionException as e:
            if "ECONNREFUSED" in e.message:
                self.stdout.write("Remote connection refused: %s:%s.\n" %(remote_host, remote_port))
                return None
            else:
                raise
                
        java_output_stream = java_socket.getOutputStream()
        java_input_stream = java_socket.getInputStream()
        
        self.stdout.write("Established tunnel to %s:%s\n" % (remote_host, remote_port))
        try:
            while True:
                rlist, wlist, elist = select.select([client_socket], [client_socket], [], 1)

                for sock in rlist:
                    self.forward_python_to_java(client_socket, java_output_stream, byte_stream_writer)

                for sock in wlist:
                    self.forward_java_to_python(java_input_stream, client_socket, byte_stream_reader)

        except socket.error as e:
            if e.errno == 10054:
                self.stdout.write("Local connection closed\n")
            else:
                raise
        finally:
            client_socket.shutdown(socket.SHUT_RDWR)
            java_socket.close()
        

    def forward_python_to_java(self, source, output_stream, byte_stream_writer):
            string = source.recv(1024)
            if string:
                byte_stream_writer.writeHexStream(output_stream, binascii.hexlify(string))

    def forward_java_to_python(self, input_stream, destination, byte_stream_reader): 
        available = input_stream.available()
        if available:
            string = byte_stream_reader.read(input_stream,0,available)
            if string:
                destination.sendall(str(string))
    
    def execute(self, arguments):
        local_port = int(arguments.local_port)
        remote_port = int(arguments.remote_port)
        remote_host = arguments.remote_host

        settings = (local_port, remote_host, remote_port)
        thread.start_new_thread(self.server_thread, settings)

    def usage(self):
        """
        Forward port on the local (drozer) host to a remote host accessible by the android device
        """
        
        return """
<p>PortForwarder listens on the local host for a connection, and tries to establish a connection to a remote host
from the android device. If this connection succeeds it tries to forward the traffic. This module currently will
only forward a single connection at a time.</p>"""
