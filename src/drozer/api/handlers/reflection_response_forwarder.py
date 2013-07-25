from pydiesel.api.protobuf_pb2 import Message

from drozer.session import Sessions

class ReflectionResponseForwarder:
    """
    ReflectionResponseForwarder is given all REFLECTION_RESPONSE messages
    received by a Server. It finds the Session, based on the session_id, and
    forwards the Message to the Console.
    """
    
    def __init__(self, connection, logger):
        self.connection = connection
        self.__logger = logger
    
    def handle(self, message):
        """
        handle() is passed messages for the ReflectionResponseForwarder to
        forward.
        """

        if message.type != Message.REFLECTION_RESPONSE:
            raise Exception("is not a REFLECTION_RESPONSE")
        if not message.HasField('reflection_response'):
            raise Exception("does not contain a REFLECTION_RESPONSE")
        
        session = Sessions.get(message.reflection_response.session_id)

        if session is not None:
            session.console.write(message.SerializeToString())
        else:
            print "no session:", message.reflection_response.session_id
            