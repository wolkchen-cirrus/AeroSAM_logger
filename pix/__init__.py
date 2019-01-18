from pymavlink import mavutil
import time


class MavlinkConnection(object):
    """
    An object to represent a connection with an FC via the MAVLINK protocol
    """
    def __init__(self):
        self.master = mavutil.mavlink_connection('udpout:0.0.0.0:9000')
        self.wait_for_connection()
        self.master.wait_heartbeat()
        self.info_buffer = []
        self.lat = 0
        self.lon = 0
        self.alt_m = 0
        self.vz_ms = 0
        self.press_hPa = 0
        self.epoch_time = 0
        self.master.mav.request_data_stream_send(self.master.target_system, self.master.target_component,
                                                 mavutil.mavlink.MAV_DATA_STREAM_ALL, 4, 1)

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
            self.lat = msg.lat
            self.lon = msg.lon
            self.alt_m = msg.alt
            self.vz_ms = msg.vz
        if msg_type == "RAW_PRESSURE":
            self.press_hPa = msg.press_abs
            self.epoch_time = msg.usec

    def fill_info_buffer(self):
        self.info_buffer = []
        self.data_packet_handler()
        self.info_buffer.append(self.epoch_time)
        self.info_buffer.append(self.press_hPa)
        self.info_buffer.append(self.lat)
        self.info_buffer.append(self.lon)
        self.info_buffer.append(self.alt_m)
        self.info_buffer.append(self.vz_ms)
