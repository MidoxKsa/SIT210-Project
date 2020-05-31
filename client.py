import paho.mqtt.client as mqtt
import requests


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    client.subscribe("MySensor/HighTemp")
    client.subscribe("MySensor/LowTemp")
    client.subscribe("MySensor/HighHumi")
    client.subscribe("MySensor/LowHumi")
 

def on_message(client, userdata, msg):
    
    print(msg.topic+" "+str(msg.payload))
    playloadStr = str(msg.payload)
    
    if (playloadStr == "b'TempHigh'"):
        print("high temperature at the new born's room")
        requests.post("https://maker.ifttt.com/trigger/high_temp/with/key/c98Zt5XbfU1rgVdH84Y23K")
        

    if (playloadStr == "b'TempLow'"):
        print("Low temperature at the new born's room")
        requests.post("https://maker.ifttt.com/trigger/low_temp/with/key/c98Zt5XbfU1rgVdH84Y23K")
        
    if(playloadStr == "b'HumiHigh'"):
        print("high humidity at the new born's room")
        requests.post("https://maker.ifttt.com/trigger/high_humi/with/key/c98Zt5XbfU1rgVdH84Y23K")
        #x= requests.post("https://maker.ifttt.com/trigger/high_humi/with/key/c98Zt5XbfU1rgVdH84Y23K")
        #print(x.text,"***")
        
    if (playloadStr == "b'HumiLow'"):
        print("Low hmidity at the new born's room")
        requests.post("https://maker.ifttt.com/trigger/low_humi/with/key/c98Zt5XbfU1rgVdH84Y23K")
        
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()
