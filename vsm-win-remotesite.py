# from classes.testGogo.py import TestGogo
import classes.testGogo as test
# import classes.gogotalk as gogotalk
#import classes.gogotalk_on_win as gogotalk
import paho.mqtt.client as mqtt

messageCome = ""

def callZoom(message):
    #  gogo all cmd
    msg = message.split(" ")
    if (msg[0] == "open"):
        print("beep")
    else:
        print("test else")


def on_connect(client, userdata, flags, rc):
    print("Connected with Code : "+ str(rc))
    print("MQTT Connected.")
    # Subscribe 
    client.subscribe("demo1")

def on_message(client, userdata,msg):
    messageCome = str(msg.payload.decode("utf-8"))
    # do something here 

    cmdProcess(messageCome)
    
    print("print msg : "+messageCome)
    

if __name__=='__main__':
    # gogoTest.processCommand()
    print("mqtt starting")
    # mqttConnect()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("soldier.cloudmqtt.com",14222,60)
    #client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    client.loop_forever()




