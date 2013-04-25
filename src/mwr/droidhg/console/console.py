import getpass
import sys

from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.api.transport.exceptions import ConnectionError

from mwr.common import cli, path_completion

from mwr.droidhg.api.formatters import SystemResponseFormatter
from mwr.droidhg.connector import ServerConnector
from mwr.droidhg.console.session import Session, DebugSession

class Console(cli.Base):
    """
    mercury console [OPTIONS] COMMAND
    
    Starts a new Mercury Console to interact with an Agent.

    The Mercury Console connects to an Agent and allows you to interact with the
    system from the context of the agent application on the device. The console
    can connect directly to an agent, if its embedded server is enabled, or through
    a Mercury Server that the agent is connected to.
    """

    def __init__(self):
        cli.Base.__init__(self)
        
        self._parser.add_argument("device", default=None, nargs='?', help="the unique identifier of the Agent to connect to")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]", help="specify the address and port of the Mercury server")
        self._parser.add_argument("--ssl", action="store_true", default=False, help="connect with SSL")
        self._parser.add_argument("--debug", action="store_true", default=False, help="enable debug mode")
        self._parser.add_argument("--password", action="store_true", default=False, help="the agent requires a password")
        self._parser.add_argument("-c", "--command", default=None, dest="onecmd", help="specify a single command to run in the session")
        self._parser.add_argument("-f", "--file", default=[], help="source file", nargs="*")
        
        self.__server = None
        
    def do_connect(self, arguments):
        """starts a new session with a device"""
        
        if arguments.password:
            password = getpass.getpass()
        else:
            password = None

        device = self.__get_device(arguments)
        
        server = self.__getServerConnector(arguments)
        response = server.startSession(device, password)
        
        if response.type == Message.SYSTEM_RESPONSE and\
            response.system_response.status == Message.SystemResponse.SUCCESS:
            session_id = response.system_response.session_id

            try:
                if(arguments.debug):
                    session = DebugSession(server, session_id)
                else:
                    session = Session(server, session_id)

                if len(arguments.file) > 0:
                    session.do_load(" ".join(arguments.file))
                    session.do_exit("")
                elif arguments.onecmd != None:
                    session.onecmd(arguments.onecmd)
                    session.do_exit("")
                else:
                    session.cmdloop()
            except KeyboardInterrupt:
                print
                print "Caught SIGINT, terminating your session."
            finally:
                session.do_exit("")
                
            self.__getServerConnector(arguments).close()
        else:
            self.handle_error(RuntimeError(response.system_response.error_message), fatal=True)

    def do_devices(self, arguments):
        """lists all devices bound to the Mercury server"""

        response = self.__getServerConnector(arguments).listDevices()

        print SystemResponseFormatter.format(response)

        self.__getServerConnector(arguments).close()

    def do_disconnect(self, arguments):
        """disconnects a Mercury session"""

        response = self.__getServerConnector(arguments).stopSession(arguments.device)

        print SystemResponseFormatter.format(response)
        
        self.__getServerConnector(arguments).close()
        
    def get_completion_suggestions(self, action, text, **kwargs):
        if action.dest == "server":
            return ["localhost:31415"]
        elif action.dest == "file":
            return path_completion.complete(text)
        elif action.dest == "device":
            return None
        elif action.dest == "onecmd":
            return None
        
    def handle_error(self, throwable, fatal=False):
        """error handler: shows an exception message, before terminating"""
        
        if str(throwable) == "connection reset by peer":
            sys.stderr.write("The Mercury server is not available. Please double check the address and port.\n\n")
        elif str(throwable) == "'NoneType' object has no attribute 'id'":
            sys.stderr.write("Expected a response from the server, but there was none.\nThe server may be unavailable, or may be expecting you to connect using SSL.\n\n")
        elif isinstance(throwable, ConnectionError) or fatal == True:
            sys.stderr.write("There was a problem connecting to the Mercury server.\n\n")
            sys.stderr.write("Things to check:\n\n")
            sys.stderr.write(" - is the Mercury Server running?\n")
            sys.stderr.write(" - have you set up appropriate adb port forwards?\n")
            sys.stderr.write(" - have you specified the correct hostname and port with --server?\n")
            sys.stderr.write(" - is the server protected with SSL (add an --ssl switch)?\n")
            sys.stderr.write(" - is the agent protected with a password (add a --password switch)?\n\n")
            if(hasattr(throwable, 'cause')):
                sys.stderr.write("Debug Information:\n")
                sys.stderr.write("%s\n\n" % str(throwable.cause))
            
            sys.exit(1)
        else:
            cli.Base.handle_error(self, throwable)

    def __get_device(self, arguments):
        """
        Determines which device to request after connecting to the server.
        """

        if arguments.device == None:
            devices = self.__getServerConnector(arguments).listDevices().system_response.devices

            if len(devices) == 1:
                device = devices[0].id

                print "Selecting %s (%s %s %s)\n" % (devices[0].id, devices[0].manufacturer, devices[0].model, devices[0].software)

                return device
            elif len(devices) == 0:
                print "No devices available.\n"

                sys.exit(-1)
            else:
                print "More than one device available. Please specify the target device ID.\n"

                sys.exit(-1)
        else:
            return arguments.device

    def __getServerConnector(self, arguments):
        """
        Get a Server object which provides a connection to the selected server.
        """

        if self.__server == None:
            self.__server = ServerConnector(arguments, self.__manage_trust)

        return self.__server
    
    def __manage_trust(self, provider, certificate, peer):
        """
        Callback, invoked when connecting to a server with SSL, to manage the trust
        relationship with that server based on SSL certificates.
        """
        
        trust_status = provider.trusted(certificate, peer)
            
        if trust_status < 0:
            print "Mercury has established an SSL Connection to %s:%d." % peer
            print "The server has provided an SSL Certificate with the SHA-1 Fingerprint:"
            print "%s\n" % provider.digest(certificate)
            
            if trust_status == -2:
                print "WARNING: this host has previously used a certificate with the fingerprint:"
                print "%s\n" % provider.trusted_certificate_for(peer)
            
            while(True):
                print "Do you want to accept this certificate? [yna] ",
                
                selection = raw_input().strip().lower()
                
                if selection == "n":
                    sys.exit(-2)
                elif selection == "y":
                    print
                    break
                elif selection == "a":
                    print "Adding certificate to known hosts.\n"
                    provider.trust(certificate, peer)
                    break
                    