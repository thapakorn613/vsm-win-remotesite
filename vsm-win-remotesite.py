# from classes.testGogo.py import TestGogo
import classes.testGogo as test
# import classes.gogotalk as gogotalk
#import classes.gogotalk_on_win as gogotalk
import paho.mqtt.client as mqtt
import webbrowser
from subprocess import call
import os
import signal
import subprocess

messageCome = ""

bedugMode = True

def openLink():
    url = 'http://localhost:3000/'
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(url)

def callZoom():
    openLink()
    call(["node", "index.js"])

def closeZoom():
    print("something")

def getZoom(message):
    #  gogo all cmd
    msg = message.split(" ")
    if (msg[0] == "open"):
        callZoom()
        print("open zoom id demo1 !!! ")
    else:
        closeZoom()
        print("close zoom id demo1 !!! ")


def on_connect(client, userdata, flags, rc):
    print("Connected with Code : "+ str(rc))
    print("MQTT Connected.")
    # Subscribe 
    client.subscribe("remotelab/site/demo1")

def on_message(client, userdata,msg):
    messageCome = str(msg.payload.decode("utf-8"))
    # do something here 
    getZoom(messageCome)
    print("print msg : "+messageCome)
    

if __name__=='__main__':
    print("mqtt starting")
    # mqttConnect()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    if(bedugMode == True):
        client.connect("soldier.cloudmqtt.com",14222,61)
        client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    else:
        client.connect("soldier.cloudmqtt.com",14222,61)
        client.username_pw_set("obpkkwdc","1lUnSF15XpWM")
    client.loop_forever()




