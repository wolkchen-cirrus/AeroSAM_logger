import os


class LogFile(object):
    """
    An object representing a log file to store data
    :param base_name: Basic file name to be created i.e. tuna_01, tuna_02, etc.
    :param path: Path to file, recommended in /home/user/... or /media/usb_stick/...
    """
    def __init__(self, base_name, path):
        self.base_name = str(base_name)
        self.name = self.make_file(path)

    def make_file(self, path):
        name = self.base_name
        name += "_00.csv"
        path_name = path
        for i in range(100):
            path_name = path
            name_l = list(name)
            name_l[-1-5] = str(int(i / 10))
            name_l[-1-4] = str(int(i % 10))
            name = "".join(name_l)
            path_name += '/'
            path_name += name
            if os.path.exists(path_name) is False:
                break
        return path_name

    def write_data_log(self, time, pres, lat, lon, alt, vz, temp, hum, counts,
                       tof, period, c_sum, glitch, l_tof, rej_rat):
        data_array = [time, pres, lat, lon, alt, vz, temp, hum, counts, tof, period, c_sum, glitch, l_tof, rej_rat]
        log = open(self.name, "a+")
        data_array = ",".join(str(i) for i in data_array)
        data_array = data_array.replace("]", "").replace("[", "")
        log.write(data_array)
        log.write('\n')
        log.flush()
        log.close()

    def make_headers(self, date, time, epoch, info_str, bbs, gsc, ucass_id):
        log = open(self.name, "a+")
        log.write(date)
        log.write(',')
        log.write(time)
        log.write(',')
        log.write(str(epoch))
        log.write('\n')
        log.write(info_str)
        log.write('\n')
        log.write("bb0,bb1,bb2,bb3,bb4,bb5,bb6,bb7,bb8,bb9,bb10,bb11,bb12,bb13,bb14,bb15,GSC,ID\n")
        bb_str = ",".join(str(i) for i in bbs)
        bb_str = bb_str.replace("]", "").replace("[", "")
        log.write(bb_str)
        log.write(',')
        log.write(str(gsc))
        log.write(',')
        log.write(str(ucass_id))
        log.write('\n')
        log.write("time,pres,lat,lon,alt,vz,temp,hum,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b1ToF,b3ToF"
                  ",b7ToF,period,CSum,glitch,longToF,RejRat\n")
        log.flush()
        log.close()
