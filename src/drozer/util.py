import argparse
import socket
    
DefaultHost = "localhost"
DefaultPort = 31415
    
def parse_server(server_string):
    """
    Decode the Server endpoint parameters, as we expect them to be passed into a CLI.
    This extracts the hostname and port, assigning a default if they are not provided.
    """
    
    host = DefaultHost
    port = DefaultPort
    
    if server_string != None and server_string.find(":") == -1:
        host = server_string
    elif server_string != None:
        host, port = server_string.split(":", 1)
    
    return (socket.gethostbyname(host), int(port))
        
class StoreZeroOrTwo(argparse.Action):
    
    def __call__(self, parser, args, values, option_string=None):
        if not (len(values) == 0 or len(values) == 2):
            msg='argument "--{f}" requires either 0 or 2 arguments'.format(f=self.dest)
            raise argparse.ArgumentTypeError(msg)
        setattr(args, self.dest, values)
