from StringIO import StringIO
import unittest

from mwr.cinnibar.api import builders, frame
from mwr.cinnibar.api.protobuf_pb2 import Message

class FrameTestCase(unittest.TestCase):

    class MockSocket:

        def __init__(self, fragments):
            self.fragments = fragments
            self.recvd = []
        
        def recv(self, length):
            self.recvd.append(length)
            
            return self.fragments.pop(0)
    
    def testItShouldBuildFrameFromMessage(self):
        message = Message(id=1, type=Message.REFLECTION_REQUEST).SerializeToString()

        assert frame.Frame.fromMessage(message).length == len(message)

    def testItShouldShowFrameIsValid(self):
        assert frame.Frame(2, 11, "the payload").isValid()

    def testItShouldShowFrameIsNotValid(self):
        assert not frame.Frame(2, 10, "the payload").isValid()

    def testItShouldExtractTheMessage(self):
        message = Message(id=1, type=Message.REFLECTION_REQUEST).SerializeToString()

        assert isinstance(frame.Frame(2, len(message), message).message(), Message)

    def testItShouldShowTheMessageTypeAsReflectionRequest(self):
        message = Message(id=1, type=Message.REFLECTION_REQUEST).SerializeToString()

        assert frame.Frame(2, len(message), message).messageType() == "REFLECTION_REQUEST"

    def testItShouldShowTheMessageTypeAsReflectionResponse(self):
        message = Message(id=1, type=Message.REFLECTION_RESPONSE).SerializeToString()

        assert frame.Frame(2, len(message), message).messageType() == "REFLECTION_RESPONSE"

    def testItShouldShowTheMessageTypeAsSystemRequest(self):
        message = Message(id=1, type=Message.SYSTEM_REQUEST).SerializeToString()

        assert frame.Frame(2, len(message), message).messageType() == "SYSTEM_REQUEST"

    def testItShouldShowTheMessageTypeAsSystemResponse(self):
        message = Message(id=1, type=Message.SYSTEM_RESPONSE).SerializeToString()

        assert frame.Frame(2, len(message), message).messageType() == "SYSTEM_RESPONSE"

    def testItShouldReadFrameFromAStream(self):
        stream = StringIO()
        stream.write("\x00\x00\x00\x02\x00\x00\x00\x0bthe payload")
        stream.seek(0)

        assert frame.Frame.readFrom(stream) != None     # we have read a frame
        assert stream.tell() > 0                        # we have advanced the stream

    def testItShouldNotReadPartialFrameFromAStream(self):
        stream = StringIO()
        stream.write("\x00\x00\x00\x02\x00\x00\x00\x0bthe")
        stream.seek(0)

        # the length is 0x0000000b (dec 11), but we only provide 3 bytes of
        # actual payload

        assert frame.Frame.readFrom(stream) == None     # we haven't read a frame
        assert stream.tell() == 0                       # we have left the stream intact

    def testItShouldReadFrameFromASocket(self):
        socket = FrameTestCase.MockSocket(["\x00\x00\x00\x02\x00\x00\x00\x0b", "the payload"])

        assert frame.Frame.readFromSocket(socket) != None
        assert socket.recvd == [8, 11]

    def testItShouldReadFragmentedFrameFromASocket(self):
        socket = FrameTestCase.MockSocket(["\x00\x00\x00\x02\x00\x00\x00\x0b", "the", " payload"])
        
        assert frame.Frame.readFromSocket(socket) != None
        assert socket.recvd == [8, 11, 8]


def FrameTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(FrameTestCase("testItShouldBuildFrameFromMessage"))
    suite.addTest(FrameTestCase("testItShouldShowFrameIsValid"))
    suite.addTest(FrameTestCase("testItShouldShowFrameIsNotValid"))
    suite.addTest(FrameTestCase("testItShouldExtractTheMessage"))
    suite.addTest(FrameTestCase("testItShouldShowTheMessageTypeAsReflectionRequest"))
    suite.addTest(FrameTestCase("testItShouldShowTheMessageTypeAsReflectionResponse"))
    suite.addTest(FrameTestCase("testItShouldShowTheMessageTypeAsSystemRequest"))
    suite.addTest(FrameTestCase("testItShouldShowTheMessageTypeAsSystemResponse"))
    suite.addTest(FrameTestCase("testItShouldReadFrameFromAStream"))
    suite.addTest(FrameTestCase("testItShouldNotReadPartialFrameFromAStream"))
    suite.addTest(FrameTestCase("testItShouldReadFrameFromASocket"))
    suite.addTest(FrameTestCase("testItShouldReadFragmentedFrameFromASocket"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(FrameTestSuite())
