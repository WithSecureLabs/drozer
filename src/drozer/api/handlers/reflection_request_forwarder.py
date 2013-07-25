from pydiesel.api.builders import ReflectionResponseFactory
from pydiesel.api.protobuf_pb2 import Message

from drozer.session import Sessions
from drozer.device import DeviceGoneAway

class ReflectionRequestForwarder:
    """
    ReflectionRequestForwarder is given all REFLECTION_REQUEST messages
    received by a Server. It finds the Session, based on the session_id, and
    forwards the Message to the Device.

    The Handler returns a reply that is wishes to send.
    """
    
    def __init__(self, connection, logger):
        self.connection = connection
        self.__logger = logger
    
    def handle(self, message):
        """
        handle() is passed messages for the ReflectionRequestForwarder to
        forward.
        """

        if message.type != Message.REFLECTION_REQUEST:
            raise Exception("is not a REFLECTION_REQUEST")
        if not message.HasField('reflection_request'):
            raise Exception("does not contain a REFLECTION_REQUEST")
        
        session = Sessions.get(message.reflection_request.session_id)

        if session is not None:
            try:
                session.device.write(message.SerializeToString())
            except DeviceGoneAway as e:
                session.console.write(ReflectionResponseFactory.fatal(str(e)).inReplyTo(message).build())

                session.console.transport.loseConnection()
        else:
            print "no session:", message.reflection_request.session_id
            