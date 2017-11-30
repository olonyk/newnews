from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

def publish_callback(result, status):
    print(result)
    print(status)
    # Handle PNPublishResult and PNStatus

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-ec413276-b805-11e6-b737-xxxxx'
pnconfig.publish_key = 'pub-c-528502df-76a6-4f07-8636-xxxxx'

pubnub = PubNub(pnconfig)

pubnub.publish().channel("awesomeChannel").message("hello!!").async(publish_callback)

