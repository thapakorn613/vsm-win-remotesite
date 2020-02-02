import classes.paho.mqtt.client as mqtt

class mqttSubscribe:
    def __init__(self):

        self.version    =   1

    def on_connect(client, userdata, flags, rc):
        print("Connected with Code : "+ str(rc))
        print("MQTT Connected.")
        client.subscribe("remotelab")

    def on_message(client, userdata,msg):
        print(str(msg.payload))

    def mqttConnect(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect("soldier.cloudmqtt.com",14222,60)
        client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
        client.loop_forever()