from gpiozero import DigitalOutputDevice
import spidev
from numpy import genfromtxt
import numpy as np


lut = genfromtxt('FP07DA802N_A5_LUT.txt', delimiter=',')
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
        bytes_received = self.spi.xfer2([0x00, 0x00, 0x00, 0x00])
        self.temp_cs.on()
        self.cal_fp07da802n(convert_raw_mcp(bytes_received))

    def read_hum(self):
        self.hum_cs.off()
        bytes_received = self.spi.xfer2([0x00, 0x00, 0x00, 0x00])
        self.hum_cs.on()
        self.cal_hih4000(convert_raw_mcp(bytes_received))

    def cal_fp07da802n(self, adc):
        vt = adc*self.v_sup/(2**12-1)
        rt = 1/(1/((8.2*self.v_sup)/vt-8.2)-1/47)
        rt_norm = rt/8
        self.t_deg_c = np.interp(rt_norm, lut[:, 1], lut[:, 0])

    def cal_hih4000(self, adc):
        vh = adc*self.v_sup/(2**12-1)
        rh_sens = (vh/self.v_sup-0.16)/0.0062
        self.rh_true = rh_sens/(1.0546-0.00216*self.t_deg_c)


def convert_raw_mcp(byte_arr):
    lsb_0 = byte_arr[1] & 0b00000011
    lsb_0 = bin(lsb_0)[2:].zfill(2)
    lsb_1 = byte_arr[2]
    lsb_1 = bin(lsb_1)[2:].zfill(8)
    lsb_2 = byte_arr[3]
    lsb_2 = bin(lsb_2)[2:].zfill(8)
    lsb_2 = lsb_2[0:2]
    lsb = lsb_0 + lsb_1 + lsb_2
    lsb = lsb[::-1]
    return int(lsb, base=2)
