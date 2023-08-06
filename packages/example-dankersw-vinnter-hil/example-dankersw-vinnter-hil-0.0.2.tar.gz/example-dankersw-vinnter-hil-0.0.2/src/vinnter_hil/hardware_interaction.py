#from .serial_wrapper import SerialInterface
from .gpio_wrapper import GpioInterface


class HardwareController:
    def __init__(self):
        print("hw init")

    def gpio(self):
        gp = GpioInterface()
        print("exec a gpio thing")

