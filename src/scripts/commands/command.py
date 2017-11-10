from datetime import datetime

class Command(object):
    def __init__(self, args):
        self.do_log = args["-l"]
        self.do_verbose = args["-v"]
        self.name = args["name"]
    
    def log(self, message):
        time = datetime.now()
        time_stamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:4}\t{:11}\t".format(\
                      time.year, time.month, time.day, time.hour, time.minute, time.second,\
                      str(time.microsecond)[:3], self.name)
        message = "{}{}".format(time_stamp, message)
        print(message)
    
    def read_file(self, file_to_read):
        file_data = None
        with open(file_to_read) as data_file:
            file_data = data_file.read()
        return file_data