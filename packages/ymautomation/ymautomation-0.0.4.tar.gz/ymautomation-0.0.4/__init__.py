import paho.mqtt.client as client
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = ymautomation.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.ymautomation.com", 8883, 60)
print("sucess")
client.loop_forever()


