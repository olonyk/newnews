from .command import Command
from pydispatch import dispatcher
from multiprocessing import Process
import time

class Test(Command):
    def __init__(self, args):
        super(Test, self).__init__(args)
        self.log("Initialized")
        self.signal = "save_msg"

    def run(self):
        self.log("Running")
        dispatcher.connect(self.handle_event, signal=self.signal, sender=dispatcher.Any)
        pro = Sender()
        pro.start()
        pro.join()
 
    def handle_event(self, sender):
        print("Signal was sent by", sender)

class Sender(Process):
    def run(self):
        for i in range(5):
            print("Sending {}".format(i))
            dispatcher.send(signal="save_msg", sender="Message nr: {}".format(i))
            time.sleep(1)