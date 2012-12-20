import argparse
import sys

from mwr.common import cli
from mwr.droidhg.api.formatters import SystemResponseFormatter
from mwr.droidhg.api.protobuf_pb2 import Message
from mwr.droidhg.console.server import Server
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
        
        self._parser.add_argument("device", default=None, nargs='?',
            help="the unique identifier of the Agent to connect to")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]",
            help="specify the address and port of the Mercury server")
        self._parser.add_argument("--ssl", action="store_true", default=False,
            help="connect with SSL")
        self._parser.add_argument("--debug", action="store_true", default=False,
            help="enable debug mode")
        self._parser.add_argument("-c", "--command", default=None, dest="onecmd",
            help="specify a single command to run in the session")
        self._parser.add_argument("-f", "--file", default=[],
            help="source file", nargs="*")
        
        self.__server = None
        
    def do_connect(self, arguments):
        """starts a new session with a device"""

        device = self.__get_device(arguments)
        
        server = self.__getServer(arguments)
        response = server.startSession(device)
        
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
        else:
            print "error:", response.system_response.error_message

            sys.exit(-1)

    def do_devices(self, arguments):
        """lists all devices bound to the Mercury server"""

        response = self.__getServer(arguments).listDevices()

        print SystemResponseFormatter.format(response)

    def do_disconnect(self, arguments):
        """disconnects a Mercury session"""

        response = self.__getServer(arguments).stopSession(arguments.device)

        print SystemResponseFormatter.format(response)

    def do_sessions(self, arguments):
        """lists all active sessions on the Mercury server"""

        response = self.__getServer(arguments).listSessions()

        print SystemResponseFormatter.format(response)

    def __get_device(self, arguments):
        """
        Determines which device to request after connecting to the server.
        """

        if arguments.device == None:
            devices = self.__getServer(arguments).listDevices().system_response.devices

            if len(devices) == 1:
                device = devices[0].id

                print "Selecting {} ({} {} {})"\
                    .format(devices[0].id, devices[0].manufacturer,
                        devices[0].model, devices[0].software)
                print

                return device
            elif len(devices) == 0:
                print "No devices available."
                print

                sys.exit(-1)
            else:
                print "More than one device available. Please specify the target device ID."
                print

                sys.exit(-1)
        else:
            return arguments.device

    def __getServer(self, arguments):
        """
        Get a Server object which provides a connection to the selected server.
        """

        if self.__server == None:
            self.__server = Server(arguments)

        return self.__server
        