import time
from Devices.Logitech.EngineNotFoundException import LogitechEngineNotFoundException
from Devices.device import Device
from Devices.devices import DeviceType
import ctypes
import os

def check_if_engine_exists():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "", "LogitechLedEnginesWrapper.dll")):
        raise LogitechEngineNotFoundException("Logitech LED SDK not found. Please install it from https://www.logitechg.com/en-gb/innovation/developer-lab.html and place LogitechLedEnginesWrapper.dll in the same package as the other Logitech scripts")

class Keyboard(Device):
    def __init__(self):
        super().__init__()

        check_if_engine_exists()

        self.type = DeviceType.LOGITECH_KEYBOARD
        dll_path = os.path.join(os.path.dirname(__file__), "", "LogitechLedEnginesWrapper.dll")
        self.sdk = ctypes.WinDLL(dll_path)
        self.sdk.LogiLedInit()

    def set_colour(self, colour):
        self.sdk.LogiLedSetLighting(colour[0], colour[1], colour[2])

