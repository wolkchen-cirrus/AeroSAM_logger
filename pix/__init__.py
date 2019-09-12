from pymavlink import mavutil
import time


class MavlinkConnection(object):
    """
    An object to represent a connection with an FC via the MAVLINK protocol
    """
    def __init__(self, port, baudrate):
        self.start_date = []
        self.start_time = []
        self.all_data_received = 0
        self.got_system_time = 0
        self.got_global_position_int = 0
        self.got_scaled_pressure = 0
        self.master = mavutil.mavlink_connection(port, baud=baudrate)
        self.wait_for_connection()
        self.master.wait_heartbeat()
        self.lat = 0
        self.lon = 0
        self.alt_m = 0
        self.vz_ms = 0
        self.press_hPa = 0
        self.epoch_time = 0
        self.boot_time = 0
        self.master.mav.request_data_stream_send(self.master.target_system, self.master.target_component,
                                                 mavutil.mavlink.MAV_DATA_STREAM_ALL, 1, 1)

    def wait_for_connection(self):
        msg = None
        while not msg:
            self.master.mav.ping_send(time.time(), 0, 0, 0)
            msg = self.master.recv_match()
            time.sleep(0.5)

    def data_packet_handler(self):
        wait = True
        msg = []
        while wait:
            msg = self.master.recv_match(blocking=False)
            if msg:
                break
        msg_type = msg.get_type()
        if msg_type == "GLOBAL_POSITION_INT":
            self.got_global_position_int = 1
            self.lat = msg.lat
            self.lon = msg.lon
            self.alt_m = msg.alt
            self.vz_ms = msg.vz
        if msg_type == "SCALED_PRESSURE":
            self.got_scaled_pressure = 1
            self.press_hPa = msg.press_abs
        if msg_type == "SYSTEM_TIME":
            self.got_system_time = 1
            self.boot_time = msg.time_boot_ms
            self.epoch_time = msg.time_unix_usec

    def fill_info_buffer(self):
        timeout = 0
        while True:
            timeout = timeout+1
            self.data_packet_handler()
            check = self.got_system_time * self.got_scaled_pressure * self.got_global_position_int
            if check == 1:
                self.all_data_received = 1
                self.got_global_position_int = 0
                self.got_scaled_pressure = 0
                self.got_system_time = 0
                break
            elif timeout == 60:
                self.all_data_received = 0
                break
            else:
                time.sleep(0.01)

    def get_date_time(self):
        while True:
            self.fill_info_buffer()
            if self.epoch_time != 0:
                break
        epoch_sec = self.epoch_time/1000000
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch_sec)))
        date_time = date_time.split()
        self.start_date = date_time[0]
        self.start_time = date_time[1]
