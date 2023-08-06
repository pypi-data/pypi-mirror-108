import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("ymtest", password="ym")
client.connect("mqtt.ymautomation.com", 1883, 60)

print("success")
client.publish("test","hi")
print("done")
client.loop_forever()


