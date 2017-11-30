import time
from multiprocessing import Process

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

try:
    from .command import Command
except SystemError:
    from command import Command
    pass

class Test(Command):
    def __init__(self, args):
        super(Test, self).__init__(args)
        self.signal = "save_msg"

        self.log("Initialized")

    def run(self):
        self.log("Running")
 
    def _callback(self, sender):
        print("Signal was sent by", sender)

class Sender(Command):
    def __init__(self, args):
        super(Sender, self).__init__(args)
        self.signal = "save_msg"

        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "a_subkey"
        pnconfig.publish_key = "a_pubkey"
        pnconfig.ssl = False
        self.pubnub = PubNub(pnconfig)
        

        self.log("Initialized")

    def publish_callback(self, result, status):
        pass

    def run(self):
        self.log("Running")
        for i in range(5):
            self.log("Sending {}".format(i))
            self.pubnub.publish().channel('my_channel').message(['hello', 'there']).async(self.publish_callback)
            time.sleep(1.5)


 
pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'demo'
pnconfig.publish_key = 'demo'
 
pubnub = PubNub(pnconfig)
 
 
def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        print("my_publish_callback, success")
        pass  # Message successfully published to specified channel.
    else:
        print("my_publish_callback, error")
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel("awesomeChannel").message("hello!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        print("message: {}".format(message.message))
        print("message: {}".format(message.channel))
        pass  # Handle new message stored in message.message
 
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('awesomeChannel').execute()
print("Hear")