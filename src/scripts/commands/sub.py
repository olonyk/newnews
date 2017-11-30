from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        print(presence)

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost

        elif status.category == PNStatusCategory.PNConnectedCategory:
        # Connect event. You can do stuff like publish, and know you'll get it.
        # Or just use the connected event to confirm you are subscribed for
        # UI / internal notifications, etc
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        # Happens as part of our regular operation. This event happens when
        # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
        # Handle message decryption error. Probably client configured to
        # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        print(message.message)

class HandleDisconnectsCallback(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            # internet got lost, do some magic and call reconnect when ready
            pubnub.reconnect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # do some magic and call reconnect when ready
            pubnub.reconnect()
        else:
            print("here")
            pubnub.reconnect()
 
    def presence(self, pubnub, presence):
        pass
 
    def message(self, pubnub, message):
        print(message.message)
        pass
        
pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c'
pnconfig.publish_key = 'pub-c'
pubnub = PubNub(pnconfig)

disconnect_listener = HandleDisconnectsCallback()

#pubnub.add_listener(MySubscribeCallback())
pubnub.add_listener(disconnect_listener)
pubnub.subscribe().channels('awesomeChannel').execute()


 

 
 
