import met
import ucass
import log
import pix
from time import sleep


if __name__ == '__main__':
    resolution_ms = 500
    run_forever = False
    run_time = 10
    ss = ucass.UCASS(25)
    print("UCASS Connected")
    mavcon = pix.MavlinkConnection('/dev/ttyS0', 57600)
    print("Mavlink Connected")
    mavcon.get_date_time()
    name_string = "_".join(["AeroSAM-log", mavcon.start_date, mavcon.start_time])
    sd_log = log.LogFile(name_string, "/home/pi")
    print("".join(["Log File: ", name_string]))
    met_module = met.MetSensorModule(23, 24, 4)
    print("MET Sensors Connected")
    ss.read_info_string()
    ss.read_config_vars()
    sd_log.make_headers(mavcon.start_date, mavcon.start_time, int(mavcon.epoch_time/1000), ss.info_string,
                        ss.bbs, ss.gsc, ss.id)
    t0 = mavcon.boot_time
    while True:
        mavcon.get_date_time()
        t1 = mavcon.boot_time
        mavcon.fill_info_buffer()
        ss.read_histogram_data()
        met_module.read_hum()
        met_module.read_temp()
        sd_log.write_data_log(mavcon.boot_time, mavcon.press_hPa, mavcon.lat, mavcon.lon, mavcon.alt_m, mavcon.vz_ms,
                              met_module.t_deg_c, met_module.rh_true, ss.hist, ss.mtof, ss.period, ss.checksum,
                              ss.reject_glitch, ss.reject_ltof, ss.reject_ratio)
        mavcon.get_date_time()
        t2 = mavcon.boot_time
        delay_ms = resolution_ms-(t2-t1)
        if delay_ms > 0:
            sleep(delay_ms/1000)
        else:
            print("Loop Time Exceeds Resolution")
        if (not run_forever) & ((mavcon.boot_time-t0) > run_time*1000):
            print("Loop Finished")
            break
