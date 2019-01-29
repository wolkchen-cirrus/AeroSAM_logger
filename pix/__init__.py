from pymavlink import mavutil
import time


class MavlinkConnection(object):
    """
    An object to represent a connection with an FC via the MAVLINK protocol
    """
    def __init__(self, port, baudrate):
        self.got_raw_imu = 0
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
        self.master.mav.request_data_stream_send(self.master.target_system, self.master.target_component,
                                                 mavutil.mavlink.MAV_DATA_STREAM_POSITION, 40, 1)
        self.master.mav.request_data_stream_send(self.master.target_system, self.master.target_component,
                                                 mavutil.mavlink.MAV_DATA_STREAM_RAW_SENSORS, 40, 1)

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
        if msg_type == "RAW_IMU":
            self.got_raw_imu = 1
            self.epoch_time = msg.time_usec

    def fill_info_buffer(self):
        timeout = 0
        while True:
            timeout = timeout+1
            self.data_packet_handler()
            check = self.got_raw_imu * self.got_scaled_pressure * self.got_global_position_int
            if (check == 1) | (timeout == 60):
                break
