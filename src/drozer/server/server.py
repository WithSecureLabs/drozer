import argparse

from mwr.common import cli

from drozer.server import dz, uploader

class Server(cli.Base):
    """
    drozer console COMMAND [OPTIONS]
    
    Starts a new drozer Server, or runs utilities to interact with a running
    Server.

    The drozer Server accepts connections from agents, and routes sessions
    from your console to those agents. It also exposes an HTTP server and TCP
    streams to assist you in deploying payloads to devices.
    """
    
    DefaultHost = "localhost"
    DefaultPort = 31415
    
    def __init__(self):
        cli.Base.__init__(self)
        
    def do_delete(self, arguments):
        """delete a resource from the drozer Server"""
        
        arguments.server = self.__parse_server(arguments.server)
        if arguments.ssl != None and arguments.ssl == []:
            arguments.ssl = Provider().get_keypair("drozer-server")
        
        uploader.delete(arguments, arguments.resource)

    def args_for_delete(self):
        self._parser.add_argument("resource", help="specify a resource to upload to a drozer Server")
        self._parser.add_argument("--credentials", default=None, nargs=2, metavar=("username", "password"), help="add a username/password pair that can be used to upload files to the server")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]", help="specify the address and port of the drozer server")
        self._parser.add_argument("--ssl", action=self.__build_store_zero_or_two_action(), help="enable SSL, optionally specifying the key and certificate", nargs="*")
    
    def do_start(self, arguments):
        """start a drozer Server"""
        
        dz.serve(arguments)
    
    def args_for_start(self):
        self._parser.add_argument("--credentials", action="append", default=[], nargs=2, metavar=("username", "password"), help="add a username/password pair that can be used to upload files to the server")
        self._parser.add_argument("--ping-interval", default=15, metavar="SECS", type=int, help="the interval at which to ping connected agents")
        self._parser.add_argument("--port", default=31415, metavar="PORT", type=int, help="specify the port on which to bind the server")
        self._parser.add_argument("--ssl", action=self.__build_store_zero_or_two_action(), help="enable SSL, optionally specifying the key and certificate", nargs="*")
    
    def do_upload(self, arguments):
        """upload a resource to the drozer Server"""
        
        arguments.server = self.__parse_server(arguments.server)
        if arguments.ssl != None and arguments.ssl == []:
            arguments.ssl = Provider().get_keypair("drozer-server")
        
        uploader.upload(arguments, arguments.resource, open(arguments.file).read(), magic=arguments.magic)
    
    def args_for_upload(self):
        self._parser.add_argument("resource", help="specify a resource to upload to a drozer Server")
        self._parser.add_argument("file", help="specify a resource to upload to a drozer Server")
        self._parser.add_argument("magic", nargs="?", help="specify a resource to upload to a drozer Server")
        self._parser.add_argument("--credentials", default=None, nargs=2, metavar=("username", "password"), help="add a username/password pair that can be used to upload files to the server")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]", help="specify the address and port of the drozer server")
        self._parser.add_argument("--ssl", action=self.__build_store_zero_or_two_action(), help="enable SSL, optionally specifying the key and certificate", nargs="*")
        
    def __build_store_zero_or_two_action(self):
        class RequiredLength(argparse.Action):
            def __call__(self, parser, args, values, option_string=None):
                if not (len(values) == 0 or len(values) == 2):
                    msg='argument "--{f}" requires either 0 or 2 arguments'.format(f=self.dest)
                    raise argparse.ArgumentTypeError(msg)
                setattr(args, self.dest, values)
        return RequiredLength
    
    def __parse_server(self, server):
        """
        Decode the Server endpoint parameters, from an ArgumentParser arguments
        object with a server member.

        This extracts the hostname and port, assigning a default if they are
        not provided.
        """

        if server != None:
            endpoint = server
        else:
            endpoint = ":".join([self.DefaultHost, str(self.DefaultPort)])

        if ":" in endpoint:
            host, port = endpoint.split(":")
        else:
            host = endpoint
            port = self.DefaultPort
        
        return (host, int(port))
