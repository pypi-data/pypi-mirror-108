from collections import namedtuple
from time import sleep

from .serial_wrapper import SerialInterface
from .gpio_wrapper import GpioInterface


class HardwareControler:
    def __init__(self, serial_config: dict, gpio_config: dict, pinout: dict):
        self.pinout = namedtuple('pinout', pinout.keys())(**pinout)
        self._serial = SerialInterface(config=serial_config)
        self._gpio = GpioInterface(config=gpio_config)

    def setup_wireless_adapter(self):
        """ Setting up the shell for automatic actions """
        self._serial.execute(cmd="shell colors off")
        self._serial.execute(cmd="shell echo off")

    def trigger_reset(self, period: int):
        """ Blocking reset action, setting the reset pin high for period seconds"""
        self._gpio.write(self.pinout.reset, True)
        sleep(period)
        self._gpio.write(self.pinout.reset, False)

    def power_device_under_test(self, power_state: bool):
        """ Turns the device under test on/off """
        self._gpio.write(self.pinout.power, power_state)

    def enable_bluetooth(self):
        """ Prepars the wireless adapter for BT actions """
        self._serial.execute(cmd="bt enable")

    def sync_serial(self, cmd: str) -> list:
        """ Executes a serial command in blocking fashion, waiting until the termincation char is reached """
        return self._serial.execute(cmd=cmd)

    def async_serial(self, cmd: str):
        pass

    def gpio_write(self, pin: int, state: bool) -> None:
        self._gpio.write(pin=pin, state=state)

    def gpio_read(self, pin: int) -> int:
        pass

