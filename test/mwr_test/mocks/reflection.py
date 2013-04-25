from mwr.cinnibar import reflection
from mwr.cinnibar.api.protobuf_pb2 import Message

class MockReflector(reflection.Reflector):

    def __init__(self, session):
        reflection.Reflector.__init__(self, session)

        self.sent = None
        self.reply_with = []

    def buildErrorReply(self, error_message):
        message = Message(id=555, type=Message.REFLECTION_RESPONSE)
        message.reflection_response.session_id = "555"
        message.reflection_response.status = Message.ReflectionResponse.ERROR
        message.reflection_response.errormessage = error_message

        return message

    def buildObjectReply(self, ref):
        message = Message(id=555, type=Message.REFLECTION_RESPONSE)
        message.reflection_response.session_id = "555"
        message.reflection_response.status = Message.ReflectionResponse.SUCCESS
        message.reflection_response.result.type = Message.Argument.OBJECT
        message.reflection_response.result.object.reference = ref

        return message

    def buildPrimitiveReply(self, type, int):
        message = Message(id=555, type=Message.REFLECTION_RESPONSE)
        message.reflection_response.session_id = "555"
        message.reflection_response.status = Message.ReflectionResponse.SUCCESS
        message.reflection_response.result.type = Message.Argument.PRIMITIVE
        message.reflection_response.result.primitive.type = type
        message.reflection_response.result.primitive.int = int

        return message

    def buildSuccessReply(self):
        message = Message(id=555, type=Message.REFLECTION_RESPONSE)
        message.reflection_response.session_id = "555"
        message.reflection_response.status = Message.ReflectionResponse.SUCCESS

        return message

    def replyWith(self, message):
        self.reply_with.append(message)

    def sendAndReceive(self, factory):
        self.sent = Message()
        self.sent.ParseFromString(factory.setId(555).setSessionId("555").build())

        if len(self.reply_with) > 0:
            return self.reply_with.pop(0)
        else:
            return None
