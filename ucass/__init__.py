from time import sleep
from gpiozero import DigitalOutputDevice
import spidev
import struct


class UCASS(object):
    """
    A UCASS Object to be used as an SPI slave, uses SPI 0 by default
    :param cs_gpio: Which GPIO pin is the chip select (slave select) for this UCASS unit
    """
    def __init__(self, cs_gpio):

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 1
        self.spi.max_speed_hz = 500000
        self.cs = DigitalOutputDevice(cs_gpio, initial_value=True)
        self.cs.on()

        self.info_string = ""
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
        self.cs.off()
        a = self.spi.xfer(command)
        sleep(0.01)
        return a

    def read_info_string(self):
        self.info_string = ""
        a = self.command_byte([0x3F])
        for i in range(60):
            sleep(0.00001)
            buf = self.spi.xfer([0x06])[0]
            self.info_string += chr(buf)
        self.cs.on()

    def read_config_vars(self):
        self.command_byte([0x3C])
        self.bbs = []
        raw = []
        for i in range(38):
            sleep(0.00001)
            buf = self.spi.xfer([0x06])[0]
            raw.append(buf)
        self.cs.on()
        for i in range(16):
            self.bbs.append(byte_to_int16(raw[i*2], raw[i*2+1]))
        self.gsc = byte_to_float(raw[32], raw[33], raw[34], raw[35])
        self.id = raw[37]

    def read_histogram_data(self):
        self.command_byte([0x30])
        self.hist = []
        self.mtof = []
        raw = []
        index = 0
        for i in range(43):
            sleep(0.00001)
            buf = self.spi.xfer([0x06])[0]
            raw.append(buf)
        for i in range(16):
            self.hist.append(byte_to_int16(raw[i*2], raw[i*2+1]))
            index = index+2
        for i in range(4):
            self.mtof.append(raw[index])
            index = index+1
        self.period = byte_to_int16(raw[36], raw[37])
        self.checksum = byte_to_int16(raw[38], raw[39])
        self.reject_glitch = raw[40]
        self.reject_ltof = raw[41]
        self.reject_ratio = raw[42]
        self.cs.on()


def byte_to_int16(lsb, msb):
    return (msb << 8) | lsb


def byte_to_float(b1, b2, b3, b4):
    arr = bytearray([b1, b2, b3, b4])
    return struct.unpack('<f', arr)
