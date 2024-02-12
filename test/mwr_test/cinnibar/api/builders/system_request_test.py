import unittest

from mwr.cinnibar.api import builders
from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.reflection.types import ReflectedType

class SystemRequestFactoryTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = builders.SystemRequestFactory

    def testItShouldBuildAListDevicesMessage(self):
        message = self.factory.listDevices().builder

        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.LIST_DEVICES

    def testItShouldBuildAListSessions(self):
        message = self.factory.listSessions().builder
        
        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.LIST_SESSIONS

    def testItShouldBuildAPingMessage(self):
        message = self.factory.ping().builder
        
        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.PING

    def testItShouldBuildAStartSessionMessage(self):
        message = self.factory.startSession("987654321").builder

        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.START_SESSION
        assert message.system_request.device.id == "987654321"
        assert message.system_request.device.manufacturer == "N/A"
        assert message.system_request.device.model == "N/A"
        assert message.system_request.device.software == "N/A"

    def testItShouldBuildAStopSessionMessage(self):
        class MockSession:

            def __init__(self, session_id):
                self.session_id = session_id

        message = self.factory.stopSession(MockSession("987654321")).builder

        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.STOP_SESSION
        assert message.system_request.session_id == "987654321"

    def testItShouldBuildAStopSessionIdMessage(self):
        message = self.factory.stopSessionId("987654321").builder

        assert message.type == Message.SYSTEM_REQUEST
        assert message.system_request.type == Message.SystemRequest.STOP_SESSION
        assert message.system_request.session_id == "987654321"

    def testItShouldAddDevice(self):
        class MockDevice:

            def __init__(self, device_id, manufacturer, model, software):
                self.device_id = device_id
                self.manufacturer = manufacturer
                self.model = model
                self.software = software

        factory = self.factory(Message.SystemRequest.LIST_DEVICES) # the type of message isn't important
        factory.addDevice(MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0"))
        message = factory.builder

        assert message.system_request.device.id == "987654321"
        assert message.system_request.device.manufacturer == "Widget Corp"
        assert message.system_request.device.model == "Mobile 1"
        assert message.system_request.device.software == "4.2.0"

    def testItShouldAddDeviceId(self):
        factory = self.factory(Message.SystemRequest.LIST_DEVICES) # the type of message isn't important
        factory.addDeviceId("987654321")
        message = factory.builder

        assert message.system_request.device.id == "987654321"
        assert message.system_request.device.manufacturer == "N/A"
        assert message.system_request.device.model == "N/A"
        assert message.system_request.device.software == "N/A"

    def testItShouldSetId(self):
        factory = self.factory(Message.SystemRequest.LIST_DEVICES) # the type of message isn't important
        factory.setId(42)
        message = factory.builder

        assert message.id == 42

    def testItShouldSetSessionId(self):
        factory = self.factory(Message.SystemRequest.LIST_DEVICES) # the type of message isn't important
        factory.setSessionId("42")
        message = factory.builder

        assert message.system_request.session_id == "42"


def SystemRequestFactoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAListDevicesMessage"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAListSessions"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAPingMessage"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAStartSessionMessage"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAStopSessionMessage"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldBuildAStopSessionIdMessage"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldAddDevice"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldAddDeviceId"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldSetId"))
    suite.addTest(SystemRequestFactoryTestCase("testItShouldSetSessionId"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(SystemRequestFactoryTestSuite())
