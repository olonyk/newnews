from datetime import datetime
import pika

class Command(object):
    def __init__(self, args):
        self.do_log = args["-l"]
        self.do_verbose = args["-v"]
        self.name = args["name"]
        # Initialize the publish/subscribe object
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

    def log(self, message):
        time = datetime.now()
        time_stamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:4}    {:15}    ".format(\
                      time.year, time.month, time.day, time.hour, time.minute, time.second,\
                      str(time.microsecond)[:3], self.name)
        message = "{}{}".format(time_stamp, message)
        print(message)
        # Publish the log message on the log topic
        try:
            self.channel.basic_publish(exchange='logs', routing_key='', body=message)
            # Except Connection Closed, try to reconnect.
        except pika.exceptions.ConnectionClosed:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange='logs', exchange_type='fanout')
    
    def read_file(self, file_to_read):
        file_data = None
        with open(file_to_read) as data_file:
            file_data = data_file.read()
        return file_data
