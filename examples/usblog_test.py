import met
import ucass
import log
import pix
from time import sleep
from gpiozero import LED


if __name__ == '__main__':
    act_led = LED(19)
    act_led.on()
    name_string = "AeroSAM-log::"
    sd_log = log.LogFile(name_string, "/home/pi")
    usb_log = log.LogFile(name_string, "/media/usb/uav_data")
    print("".join(["Log File: ", name_string]))
    usb_log.make_headers("a", "h", "h", "h", "h", "j", "j")
