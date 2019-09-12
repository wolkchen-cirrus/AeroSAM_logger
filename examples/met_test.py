import met
import ucass
from time import sleep

MET = met.MetSensorModule(18, 24, 4.39)
sonde = ucass.UCASS(25)

i = 0
while True:
	MET.read_temp()
	MET.read_hum()

	sonde.read_info_string()

	print MET.t_deg_c
	print MET.rh_true
	print sonde.info_string
	print

	sleep(0.5)
	i += 1
	if i == 5:
		break
