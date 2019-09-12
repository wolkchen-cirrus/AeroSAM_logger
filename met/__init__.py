from gpiozero import DigitalOutputDevice
import spidev
from numpy import genfromtxt
import numpy as np


lut = genfromtxt('/home/pi/FP07DA802N_A5_LUT.txt', delimiter=',')
lut = np.flipud(lut)


class MetSensorModule(object):

    def __init__(self, temp_cs, hum_cs, supply):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 976000
        self.spi.mode = 0b00
        self.t_deg_c = 0
        self.rh_true = 0
        self.temp_cs = DigitalOutputDevice(temp_cs, initial_value=True)
        self.hum_cs = DigitalOutputDevice(hum_cs, initial_value=True)
        self.temp_cs.on()
        self.hum_cs.on()
        self.v_sup = supply

    def read_temp(self):
        self.temp_cs.off()
        bytes_received = self.spi.xfer2([0x00, 0x00])
        self.temp_cs.on()
        self.cal_fp07da802n(convert_raw_mcp(bytes_received))

    def read_hum(self):
        self.hum_cs.off()
        bytes_received = self.spi.xfer2([0x00, 0x00])
        self.hum_cs.on()
        self.cal_hih4000(convert_raw_mcp(bytes_received))

    def cal_fp07da802n(self, adc):
        try:
            vt = adc*float(self.v_sup)/(2**12-1)
            rt = 1/(1/((8.2*self.v_sup)/vt-8.2)-1/47)
            rt_norm = rt/8
            self.t_deg_c = np.interp(rt_norm, lut[:, 1], lut[:, 0])
        except ZeroDivisionError:
            print("Met Module Not Connected")
            pass

    def cal_hih4000(self, adc):
        vh = adc*float(self.v_sup)/(2**12-1)
        rh_sens = (vh/self.v_sup-0.16)/0.0062
        self.rh_true = rh_sens/(1.0546-0.00216*self.t_deg_c)


def convert_raw_mcp(byte_arr):
    msb = byte_arr[1]
    msb = msb >> 1
    lsb = byte_arr[0] & 0b00011111
    lsb = lsb << 7
    return lsb + msb
