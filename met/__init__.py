from gpiozero import MCP3201
from numpy import genfromtxt
import numpy as np


lut = genfromtxt('FP07DA802N_A5_LUT.txt', delimiter=',')
lut = np.flipud(lut)


def read_fp07da802n(cs):
    adc = MCP3201(channel=0, select_pin=cs)
    vt = adc/4095*5
    rt = 1/(1/(41/vt-8.2)-1/47)
    rt_norm = rt/8
    t_deg_c = np.interp(rt_norm, lut[:, 1], lut[:, 0])
    return t_deg_c


def read_hih4000(cs, t_deg_c):
    adc = MCP3201(channel=0, select_pin=cs)
    vh = adc/4095*5
    rh_sens = (vh/5-0.16)/0.0062
    rh_true = rh_sens/(1.0546-0.00216*t_deg_c)
    return rh_true
