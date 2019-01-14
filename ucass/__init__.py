from time import sleep
from gpiozero import DigitalOutputDevice
import spidev


class _UCASS(object):
    """
    A UCASS Object to be used as an SPI slave
    :param cs_gpio: Which GPIO pin is the chip select (slave select) for this UCASS unit
    """
    def __init__(self, cs_gpio):

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode(1)
        self.spi.max_speed_hz = 500000
        self._cs = DigitalOutputDevice(cs_gpio, initial_value=True)

        self.info_string = []
        self.bbs = []
        self.hist = []
        self.mtof = []
        self.period = 0
        self.gsc = 0
        self.id = 0
        self.checksum = 0
        self.reject_glitch = 0
        self.reject_ratio = 0
        self.reject_ltof = 0

    def command_byte(self, command):
        self._cs.off()
        self.spi.xfer([command])
        sleep(0.01)

    def read_info_string(self):
        self.command_byte(0x3F)
        for i in range(60):
            sleep(0.00001)
            buf = self.spi.xfer(0x06)
            self.info_string.append(buf)
        self._cs.on()

    def read_config_vars(self):
        self.command_byte(0x3C)
        raw = []
        for i in range(38):
            sleep(0.00001)
            buf = self.spi.xfer(0x06)
            raw.append(buf)
        self._cs.on()
