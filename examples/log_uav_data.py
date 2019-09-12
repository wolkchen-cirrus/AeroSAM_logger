import met
import ucass
import log
import pix
from time import sleep
from time import time
from gpiozero import LED


if __name__ == '__main__':
    print "------------------------------------------------"
    act_led = LED(19)
    act_led.on()
    sleep(10)
    resolution_ms = 1
    run_forever = True
    run_time = 10
    met_module = met.MetSensorModule(18, 24, 4.39)
    print "MET Sensors Connected"
    ss = ucass.UCASS(25)
    print("UCASS Connected")
    mavcon = pix.MavlinkConnection('/dev/ttyS0', 57600)
    print("Mavlink Connected")
    mavcon.get_date_time()
    name_string = "_".join(["AeroSAM-log", mavcon.start_date.replace('-', ''), mavcon.start_time.replace(':', '')])
    sd_log = log.LogFile(name_string, "/home/pi")
    usb_log = log.LogFile(name_string, "/media/usb/uav_data")
    print("".join(["Log File: ", name_string]))
    ss.read_info_string()
    ss.read_config_vars()
    print("Creating SD Log File")
    sd_log.make_headers(mavcon.start_date, mavcon.start_time, str(int(mavcon.epoch_time/1000)), ss.info_string,
                        ss.bbs, ss.gsc, ss.id)
    print("Creating USB Log File")
    usb_log.make_headers(mavcon.start_date, mavcon.start_time, str(int(mavcon.epoch_time/1000)), ss.info_string,
                         ss.bbs, ss.gsc, ss.id)
    t0 = mavcon.boot_time
    print("Starting Main Loop")
    loop_num = 0
    while True:
        act_led.off()
        if (loop_num % 10) == 0:
            print "Getting GPS Time"
            mavcon.get_date_time()
            t1 = mavcon.boot_time
        else:
            t1 = time()
        mavcon.fill_info_buffer()
        ss.read_histogram_data()
        met_module.read_hum()
        met_module.read_temp()
        sd_log.write_data_log(t1, mavcon.press_hPa, mavcon.lat, mavcon.lon, mavcon.alt_m, mavcon.vz_ms,
                              met_module.t_deg_c, met_module.rh_true, ss.hist, ss.mtof, ss.period, ss.checksum,
                              ss.reject_glitch, ss.reject_ltof, ss.reject_ratio)
        print "Written to SD log"
        usb_log.write_data_log(t1, mavcon.press_hPa, mavcon.lat, mavcon.lon, mavcon.alt_m, mavcon.vz_ms,
                               met_module.t_deg_c, met_module.rh_true, ss.hist, ss.mtof, ss.period, ss.checksum,
                               ss.reject_glitch, ss.reject_ltof, ss.reject_ratio)
        print "written to USB log"
        if (loop_num % 10) == 0:
            mavcon.get_date_time()
            t2 = mavcon.boot_time
        else:
            t2 = time()
        delay_ms = resolution_ms-(t2-t1)
        act_led.on()
        loop_num += 1
        if delay_ms > 0:
            sleep(delay_ms/1000)
        else:
            print("Loop Time Exceeds Resolution")
        if (run_forever is False) & (loop_num > run_time):
            print("Loop Finished")
            break
