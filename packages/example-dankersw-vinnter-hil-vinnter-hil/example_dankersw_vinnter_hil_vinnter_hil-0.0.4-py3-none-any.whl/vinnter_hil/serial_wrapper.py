from typing import List
from collections import namedtuple

from serial import Serial


class SerialInterface:
    """ Wrapper around Python's own serial package """
    _default_config: dict = {'port': '/dev/ttyACM0', 'baudrate': 115200, 'term_seq': b'uart:~$ ', 'timeout': 1}

    def __init__(self, config: dict = None) -> None:
        if config is None:
            config = self._default_config
        self.config = namedtuple('config', config.keys())(**config)

    def execute(self, cmd: str) -> List[str]:
        """ Execute a cmd synchronosly. The will halt and wait untill the termination char is received """
        print(f"Executing: {cmd!r}")
        _cmd = self._add_line_ending(line=cmd)
        rx_buffer = []
        with Serial(port=self.config.port, baudrate=self.config.baudrate, timeout=self.config.timeout) as serial:
            serial.write(_cmd.encode())
            while True:
                rx_data = serial.readline()
                if rx_data == self.config.term_seq:
                    break
                line_buffer = rx_data.decode('ascii').rstrip()
                if line_buffer != "":
                    rx_buffer.append(line_buffer)
        return rx_buffer

    def write_cmd(self, cmd: str) -> None:
        """ Write a single command out onto serial """
        print(f"Writing cmd: {cmd!r}")
        _cmd = self._add_line_ending(line=cmd)
        with Serial(port=self.config.port, baudrate=self.config.baudrate, timeout=self.config.timeout) as serial:
            serial.write(_cmd.encode())

    def read_line(self) -> str:
        """ Read one line at the time """
        with Serial(port=self.config.port, baudrate=self.config.baudrate, timeout=self.config.timeout) as serial:
            rx_data = serial.readline()
        return rx_data.decode('ascii').rstrip()

    def read_until_empty_line(self) -> str:
        running = True
        with Serial(port=self.config.port, baudrate=self.config.baudrate, timeout=5) as serial:
            while running:
                rx_buffer = serial.readline()
                if rx_buffer == b'':
                    running = False
                else:
                    yield rx_buffer.decode('ascii').rstrip()

    @staticmethod
    def _add_line_ending(line: str) -> str:
        if line[-1] != '\r':
            line += '\r'
        return line
