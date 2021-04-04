from io import StringIO

from pydiesel.api.protobuf_pb2 import Message

class SystemResponseFormatter:
    """
    The SystemResponseFormatter can take a SYSTEM_RESPONSE message, and format
    it in a human-readable way for display on the screen.

    It can print:

      - device lists;
      - session identifiers; and
      - session lists.

    It will not print:

      - pong;
      - bound; or
      - unbound.
    """

    def __init__(self, message):
        self.__buffer = StringIO()
        self.__message = message
    
    @classmethod
    def format(cls, message):
        """
        Formats a system message, and returns it as a String.
        """

        if message.type != Message.SYSTEM_RESPONSE:
            return "not a SYSTEM_RESPONSE"
        else:
            return cls(message).doFormat().flush()
    
    def doFormat(self):
        """
        Prepares the internal representation of the SystemResponse message.
        """

        if self.__type() == Message.SystemResponse.DEVICE_LIST:
            self.__print_device_list()
        elif self.__type() == Message.SystemResponse.SESSION_ID:
            self.__print_session_id()
        elif self.__type() == Message.SystemResponse.SESSION_LIST:
            self.__print_session_list()
        #elif self.__type() == Message.SystemResponse.PONG:
        #elif self.__type() == Message.SystemResponse.BOUND:
        #elif self.__type() == Message.SystemResponse.UNBOUND
        else:
            self.__print("unknown SYSTEM_RESPONSE type:",
                self.__message.system_response.type)

        return self

    def flush(self):
        """
        Retrieve the string representation of the SystemResponse that was
        previously generated by doFormat().
        """

        return self.__buffer.getvalue()

    def __print(self, *messages):
        """
        Writes a series of strings into the internal StringIO buffer.
        """

        self.__buffer.write(" ".join([str(m) for m in messages]))
        self.__buffer.write("\n")

    def __print_device_list(self):
        """
        Formats a DEVICE_LIST system message.
        """

        if len(self.__message.system_response.devices) > 0:
            self.__print("List of Bound Devices")
            self.__print()
            self.__print("{:<16}  {:<20} {:<20}  {:<10}"\
                .format("Device ID", "Manufacturer", "Model", "Software"))

            for device in self.__message.system_response.devices:
                self.__print("{:<16}  {:<20} {:<20}  {:<10}"\
                    .format(device.id, device.manufacturer, device.model,
                        device.software))
        else:
            self.__print("No Bound Devices.")

    def __print_session_id(self):
        """
        Formats a SESSION_ID system message.
        """

        if self.__message.system_response.status == Message.SystemResponse.ERROR:
            self.__print("error:",
                self.__message.system_response.error_message)
        else:
            self.__print("session:",
                self.__message.system_response.session_id)

    def __print_session_list(self):
        """
        Formats a SESSION_LIST system message.
        """

        if len(self.__message.system_response.sessions) > 0:
            self.__print("List of Sessions")
            self.__print()
            self.__print("{:<27}  {:<16}".format("Session ID", "Device ID"))

            for sess in self.__message.system_response.sessions:
                self.__print("{:<27}  {:<16}".format(sess.id, sess.device_id))
        else:
            self.__print("No Sessions.")

    def __type(self):
        """
        Determines the type of the SystemResponse.
        """

        return self.__message.system_response.type
