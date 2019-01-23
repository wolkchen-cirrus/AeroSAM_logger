from gpiozero import DigitalOutputDevice
import spidev
from numpy import genfromtxt
import numpy as np


lut = genfromtxt('FP07DA802N_A5_LUT.txt', delimiter=',')
lut = np.flipud(lut)


class MetSensorModule(object):

    def __init__(self, temp_cs, hum_cs):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2000000
        self.spi.mode = 0b00
        self.t_deg_c = 0
        self.rh_true = 0
        self.temp_cs = DigitalOutputDevice(temp_cs, initial_value=True)
        self.hum_cs = DigitalOutputDevice(hum_cs, initial_value=True)
        self.temp_cs.on()
        self.hum_cs.on()

    def read_temp(self):
        self.temp_cs.off()
        bit1 = self.spi.xfer([0x00])
        bit2 = self.spi.xfer([0x00])
        self.temp_cs.on()
        adc = bit1
        adc = adc << 8
        adc = adc | bit2
        adc = adc >> 1
        adc = adc & 0b00000000000000000000111111111111
        self.cal_fp07da802n(adc)

    def read_hum(self):
        self.hum_cs.off()
        bit1 = self.spi.xfer([0x00])
        bit2 = self.spi.xfer([0x00])
        self.hum_cs.on()
        adc = bit1
        adc = adc << 8
        adc = adc | bit2
        adc = adc >> 1
        adc = adc & 0b00000000000000000000111111111111
        self.cal_hih4000(adc)

    def cal_fp07da802n(self, adc):
        vt = adc/4095*5
        rt = 1/(1/(41/vt-8.2)-1/47)
        rt_norm = rt/8
        self.t_deg_c = np.interp(rt_norm, lut[:, 1], lut[:, 0])

    def cal_hih4000(self, adc):
        vh = adc/4095*5
        rh_sens = (vh/5-0.16)/0.0062
        self.rh_true = rh_sens/(1.0546-0.00216*self.t_deg_c)
