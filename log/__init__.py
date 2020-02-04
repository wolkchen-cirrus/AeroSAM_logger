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
        log.write("ub0,ub1,ub2,ub3,ub4,ub5,ub6,ub7,ub8,ub9,ub10,ub11,ub12,ub13,ub14,ub15,ub16,GSC,ID\n")
        bb_str = ",".join(str(i) for i in bbs)
        bb_str = bb_str.replace("]", "").replace("[", "")
        log.write(bb_str)
        log.write(',')
        log.write(str(gsc))
        log.write(',')
        log.write(str(ucass_id))
        log.write('\n')
        log.write("time,pres,lat,lon,alt,vz,temp,hum,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16,b1ToF,b3ToF"
                  ",b5ToF,b7ToF,period,CSum,glitch,longToF,RejRat\n")
        log.flush()
        log.close()
