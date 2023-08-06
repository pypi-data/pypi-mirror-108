from collections import namedtuple

from pigpio import pi


class GpioInterface:
    _default_config: dict = {'host': 'localhost', 'port': 8888}

    def __init__(self, config: dict = None) -> None:
        if config is None:
            config = self._default_config
        self.config = namedtuple('config', config.keys())(**config)
        self.gpio_pi = pi(host=self.config.host, port=self.config.port)

    def __del__(self) -> None:
        self.gpio_pi.stop()

    def write(self, pin: int, state: bool) -> None:
        self.gpio_pi.write(gpio=pin, level=state)

    def read(self, pin: int) -> int:
        return self.gpio_pi.read(gpio=pin)
