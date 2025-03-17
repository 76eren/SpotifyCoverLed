from abc import ABC, abstractmethod

# Interface for all devices
class Device(ABC):
    def __init__(self):
        self.color = (0, 0, 0)
        self.enabled = False
        self.type = None


    @abstractmethod
    def set_colour(self, colour):
        pass