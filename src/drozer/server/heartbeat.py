from drozer.device import Devices

def heartbeat():
    """
    Send a drozer Ping to every connected device.

    Devices that do not respond will be swept up later by the runtime.
    """

    for device in Devices:
        device.ping()
        