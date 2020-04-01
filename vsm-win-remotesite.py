from subprocess import call

import paho.mqtt.client as mqtt
import webbrowser as edge
import os
import signal
import subprocess
import time

messageCome = ""
bedugMode = True

def closeZoom():
    try:
        os.system('TASKKILL /F /IM MicrosoftEdge.exe')
        os.system('TASKKILL /F /IM Zoom.exe')
    except Exception , err:
        print str(err)
    
def openBrowser():
    url_demo1 = 'https://zoom.us/j/7602679734'
    edge.open_new(url_demo1)
    
def getZoom(message):
    #  gogo all cmd
    msg = message.split(" ")
    if (msg[0] == "open"):
        print("open zoom id demo1 !!! ")
        openBrowser()
    elif (msg[0] == "close"):
        print("close zoom id demo1 !!! ")
        closeZoom()

def on_connect(client, userdata, flags, rc):
    print("Connected with Code : "+ str(rc))
    print("MQTT Connected.")
    # Subscribe 
    client.subscribe("remotelab/site/demo1")

def on_message(client, userdata,msg):
    messageCome = str(msg.payload.decode("utf-8"))
    # do something here 
    print("print msg : "+messageCome)
    getZoom(messageCome)
    
if __name__=='__main__':
    print("mqtt starting")
    # mqttConnect 
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    if(bedugMode == True):
        client.connect("soldier.cloudmqtt.com",14222,60)
        client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    else:
        client.connect("soldier.cloudmqtt.com",14222,60)
        client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    client.loop_forever()




