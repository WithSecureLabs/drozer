import argparse
import logging
import sys

try:
    from twisted import internet
    from twisted.internet import ssl, task
    from twisted.internet.protocol import ServerFactory
except ImportError:
    print "drozer Server requires Twisted to run."
    print "Run 'easy_install twisted==10.2.0' to fetch this dependency."
    sys.exit(-1)

from mwr.common import cli, logger

from drozer import meta
from drozer.server.heartbeat import heartbeat
from drozer.server.protocol_switcher import ProtocolSwitcher
from drozer.ssl.provider import Provider

class Server(cli.Base):
    """
    drozer console [OPTIONS] COMMAND
    
    Starts a new drozer Server, or runs utilities to interact with a running
    Server.

    The drozer Server accepts connections from agents, and routes sessions
    from your console to those agents. It also exposes an HTTP server and TCP
    streams to assist you in deploying payloads to devices.
    """
    
    def __init__(self):
        cli.Base.__init__(self)
        
        self._parser.add_argument("--credentials", action="append", default=[], nargs=2, metavar=("username", "password"), help="add a username/password pair that can be used to upload files to the server")
        self._parser.add_argument("--port", default=31415, metavar="PORT", type=int, help="specify the port on which to bind the server")
        self._parser.add_argument("--ping-interval", default=15, metavar="SECS", type=int, help="the interval at which to ping connected agents")
        self._parser.add_argument("--ssl", action=self.__build_store_zero_or_two_action(), help="enable SSL, optionally specifying the key and certificate", nargs="*")
        self._parser.add_argument("--version", action="store_true", help="display the installed drozer version")
    
    def do_start(self, arguments):
        """start a drozer Server"""
        task.LoopingCall(heartbeat).start(arguments.ping_interval)
        
        if arguments.ssl != None:
            print "Starting drozer Server, listening on 0.0.0.0:%d (with SSL)" % arguments.port
    
            if arguments.ssl == []:
                print "Using default SSL key material..."
                
                arguments.ssl = Provider().get_keypair("drozer-server")
            
            internet.reactor.listenSSL(arguments.port,
                                       DrozerServer(dict(arguments.credentials)),
                                       ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
        else:
            print "Starting drozer Server, listening on 0.0.0.0:%d" % arguments.port
            
            internet.reactor.listenTCP(arguments.port,
                                       DrozerServer(dict(arguments.credentials)))
        
        internet.reactor.run()
    
    def __build_store_zero_or_two_action(self):
        class RequiredLength(argparse.Action):
            def __call__(self, parser, args, values, option_string=None):
                if not (len(values) == 0 or len(values) == 2):
                    msg='argument "--{f}" requires either 0 or 2 arguments'.format(f=self.dest)
                    raise argparse.ArgumentTypeError(msg)
                setattr(args, self.dest, values)
        return RequiredLength


class DrozerServer(ServerFactory):
    """
    Implements a Twisted ServerFactory, which implements the ProtocolSwitcher
    protocol to support running multiple protocols on a port.
    """

    protocol = ProtocolSwitcher

    def __init__(self, credentials):
        self.protocol.credentials = credentials
        