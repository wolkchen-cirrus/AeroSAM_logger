import log
import met
import ucass
from time import sleep


if __name__ == '__main__':

    super_sonde = ucass.UCASS(13)
    log_file = log.LogFile("AeroSAM_data_", "/home/jgirdwood/Documents")
    hum_cs = 15
    temp_cs = 16
    super_sonde.read_info_string()
    super_sonde.read_config_vars()
    log_file.make_headers(0, 0, super_sonde.info_string, super_sonde.bbs, super_sonde.gsc, super_sonde.id)

    while True:
        super_sonde.read_histogram_data()
        t_deg_c = met.read_fp07da802n(temp_cs)
        rh_true = met.read_hih4000(hum_cs, t_deg_c)
        log_file.write_data_log(0, 0, 0, 0, 0, 0, t_deg_c, rh_true, super_sonde.hist, super_sonde.mtof,
                                super_sonde.period, super_sonde.checksum, super_sonde.reject_glitch,
                                super_sonde.reject_ltof, super_sonde.reject_ratio)
        sleep(0.5)
