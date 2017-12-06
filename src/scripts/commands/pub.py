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
my_listener.wait_for_connect()
print('connected')
 
pubnub.publish().channel('awesomeChannel').message({'fieldA': 'awesome', 'fieldB': 10}).sync()
result = my_listener.wait_for_message_on('awesomeChannel')
print(result.message)
 
pubnub.unsubscribe().channels('awesomeChannel').execute()
my_listener.wait_for_disconnect()
 
print('unsubscribed')