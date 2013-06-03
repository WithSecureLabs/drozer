#!/usr/bin/python

import argparse
import logging
import sys

try:
    from twisted import internet
    from twisted.internet import ssl, task
except ImportError:
    print "drozer Server requires Twisted to run."
    print "Run 'easy_install twisted==10.2.0' to fetch this dependency."
    sys.exit(-1)

from mwr.common import logger

from drozer import meta
from drozer.server import DrozerServer, heartbeat
from drozer.ssl.provider import Provider

logger.setLevel(logging.DEBUG)
logger.addStreamHandler()

def store_zero_or_two():
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not (len(values) == 0 or len(values) == 2):
                msg='argument "--{f}" requires either 0 or 2 arguments'.format(f=self.dest)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength

parser = argparse.ArgumentParser(description='Start a drozer Server, to route agent and console connections.')
parser.add_argument("--log", default=None, help="specify the log file to write to")
parser.add_argument("--no-http", default=False, action="store_true", help="do not start the integrated HTTP server")
parser.add_argument("--port", default=31415, metavar="PORT", type=int, help="specify the port on which to bind the server")
parser.add_argument("--ping-interval", default=15, metavar="SECS", type=int, help="the interval at which to ping connected agents")
parser.add_argument("--ssl", action=store_zero_or_two(), help="enable SSL, optionally specifying the key and certificate", nargs="*")
parser.add_argument("--version", action="store_true", help="display the installed drozer version")

arguments = parser.parse_args(sys.argv[2::])

if arguments.version:
    meta.print_version()
    sys.exit(0)
    
if arguments.log != None:
    logger.addFileHandler(arguments.log)

task.LoopingCall(heartbeat).start(arguments.ping_interval)

if arguments.ssl != None:
    print "Starting drozer Server, listening on 0.0.0.0:%d (with SSL)" % arguments.port
    
    if arguments.ssl == []:
        print "Using default SSL key material..."
        
        arguments.ssl = Provider().get_keypair("drozer-server")
    
    internet.reactor.listenSSL(arguments.port,
                               DrozerServer(not arguments.no_http),
                               ssl.DefaultOpenSSLContextFactory(*arguments.ssl))
else:
    print "Starting drozer Server, listening on 0.0.0.0:%d" % arguments.port
    
    internet.reactor.listenTCP(arguments.port,
                               DrozerServer(not arguments.no_http))

internet.reactor.run()
