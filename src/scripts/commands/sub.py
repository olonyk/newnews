from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
 
pnconfig = PNConfiguration()
 
pnconfig.publish_key = 'demo'
pnconfig.subscribe_key = 'demo'
 
pubnub = PubNub(pnconfig)
 
my_listener = SubscribeListener()
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels('awesomeChannel').execute()
pubnub.subscribe().channels('awesomeChannel2').execute()

my_listener.wait_for_connect()
print('connected')

while True:
    result = my_listener.wait_for_message_on('awesomeChannel')
    print("subscription: {}".format(result.subscription))
    print("channel:      {}".format(result.channel))
    print("message:      {}".format(result.message))
    break
 
pubnub.unsubscribe().channels('awesomeChannel').execute()
my_listener.wait_for_disconnect()
 
print('unsubscribed')