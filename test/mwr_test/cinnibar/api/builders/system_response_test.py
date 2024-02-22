import unittest

from mwr.cinnibar.api import builders
from mwr.cinnibar.api.protobuf_pb2 import Message
from mwr.cinnibar.reflection.types import ReflectedType

class SystemResponseFactoryTestCase(unittest.TestCase):

    class MockDevice:

        def __init__(self, device_id, manufacturer, model, software):
            self.device_id = device_id
            self.manufacturer = manufacturer
            self.model = model
            self.software = software

    class MockSession:

        def __init__(self, session_id, device_id):
            self.session_id = session_id
            self.device = SystemResponseFactoryTestCase.MockDevice(device_id, "N/A", "N/A", "N/A")

    def setUp(self):
        self.factory = builders.SystemResponseFactory

    def testItShouldBuildABoundMessage(self):
        message = self.factory.bound(SystemResponseFactoryTestCase.MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0")).builder

        assert message.type == Message.SYSTEM_RESPONSE
        assert message.system_response.type == Message.SystemResponse.BOUND
        assert message.system_response.status == Message.SystemResponse.SUCCESS
        assert message.system_response.devices[0].id == "987654321"
        assert message.system_response.devices[0].manufacturer == "Widget Corp"
        assert message.system_response.devices[0].model == "Mobile 1"
        assert message.system_response.devices[0].software == "4.2.0"

    def testItShouldBuildAErrorMessage(self):
        message = self.factory.error(Message.SystemResponse.BOUND, "errorMessage").builder

        assert message.type == Message.SYSTEM_RESPONSE
        assert message.system_response.type == Message.SystemResponse.BOUND
        assert message.system_response.status == Message.SystemResponse.ERROR
        assert message.system_response.error_message == "errorMessage"

    def testItShouldBuildAListDevicesMessage(self):
        message = self.factory.listDevices([SystemResponseFactoryTestCase.MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0"),
            SystemResponseFactoryTestCase.MockDevice("999999999", "Widget Corp", "Mobile 2", "4.2.0")]).builder

        assert message.type == Message.SYSTEM_RESPONSE
        assert message.system_response.type == Message.SystemResponse.DEVICE_LIST
        assert message.system_response.status == Message.SystemResponse.SUCCESS
        assert message.system_response.devices[0].id == "987654321"
        assert message.system_response.devices[0].manufacturer == "Widget Corp"
        assert message.system_response.devices[0].model == "Mobile 1"
        assert message.system_response.devices[0].software == "4.2.0"
        assert message.system_response.devices[1].id == "999999999"
        assert message.system_response.devices[1].manufacturer == "Widget Corp"
        assert message.system_response.devices[1].model == "Mobile 2"
        assert message.system_response.devices[1].software == "4.2.0"

    def testItShouldBuildAUnboundMessage(self):
        message = self.factory.unbound(SystemResponseFactoryTestCase.MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0")).builder

        assert message.type == Message.SYSTEM_RESPONSE
        assert message.system_response.type == Message.SystemResponse.UNBOUND
        assert message.system_response.status == Message.SystemResponse.SUCCESS
        assert message.system_response.devices[0].id == "987654321"
        assert message.system_response.devices[0].manufacturer == "Widget Corp"
        assert message.system_response.devices[0].model == "Mobile 1"
        assert message.system_response.devices[0].software == "4.2.0"

    def testItShouldAddADevice(self):
        factory = self.factory.bound(SystemResponseFactoryTestCase.MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0"))
        factory.addDevice(SystemResponseFactoryTestCase.MockDevice("999999999", "Widget Corp", "Mobile 2", "4.2.0"))
        message = factory.builder

        assert message.system_response.devices[0].id == "987654321"
        assert message.system_response.devices[0].manufacturer == "Widget Corp"
        assert message.system_response.devices[0].model == "Mobile 1"
        assert message.system_response.devices[0].software == "4.2.0"
        assert message.system_response.devices[1].id == "999999999"
        assert message.system_response.devices[1].manufacturer == "Widget Corp"
        assert message.system_response.devices[1].model == "Mobile 2"
        assert message.system_response.devices[1].software == "4.2.0"

    def testItShouldMakeError(self):
        factory = self.factory.error(Message.SystemResponse.BOUND, "errorMessage")
        factory.isError()
        message = factory.builder

        assert message.system_response.status == Message.SystemResponse.ERROR

    def testItShouldMakeSuccess(self):
        factory = self.factory.bound(SystemResponseFactoryTestCase.MockDevice("987654321", "Widget Corp", "Mobile 1", "4.2.0"))
        factory.isSuccess()
        message = factory.builder

        assert message.system_response.status == Message.SystemResponse.SUCCESS

    def testItShouldSetErrorMessage(self):
        factory = self.factory.error(Message.SystemResponse.BOUND, "errorMessage")
        factory.setErrorMessage("otherMessage")
        message = factory.builder

        assert message.system_response.error_message == "otherMessage"


def SystemResponseFactoryTestSuite():
    suite = unittest.TestSuite()

    suite.addTest(SystemResponseFactoryTestCase("testItShouldBuildABoundMessage"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldBuildAErrorMessage"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldBuildAListDevicesMessage"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldBuildAUnboundMessage"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldAddADevice"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldMakeError"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldMakeSuccess"))
    suite.addTest(SystemResponseFactoryTestCase("testItShouldSetErrorMessage"))

    return suite
  
if __name__ == "__main__":
    unittest.TextTestRunner().run(SystemResponseFactoryTestSuite())
