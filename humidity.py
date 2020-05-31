import Adafruit_DHT
from gpiozero import LED
import requests
import time
from tkinter import *
import threading
import RPi.GPIO as GPIO
import paho.mqtt.publish as publish

ok = True
gui = Tk()
gui.title("MySensor")

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

HighTemp = LED(17)
GoodTemp = LED(27)
LowTemp = LED(22)

HighHumi = LED(18)
GoodHumi = LED(23)
LowHumi = LED(24)


def main():
    def start():
        
        while ok == True:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
              print("Temp=", temperature, "C","    " "Humidity= %", humidity)
            else:
                print("Failed to retrieve data from humidity sensor")
            
            if temperature > 22:
                HighTemp.on()
                publish.single("MySensor/HighTemp", "TempHigh", hostname="test.mosquitto.org")
            
            else:
                HighTemp.off()
                
            if temperature <= 22 and temperature >= 20:
                GoodTemp.on()
                
            else:
                GoodTemp.off()
                
            if temperature < 20:
                LowTemp.on()
                publish.single("MySensor/LowTemp", "TempLow", hostname="test.mosquitto.org")
                

            else:
                LowTemp.off()
                
            if humidity > 60:
                HighHumi.on()
                publish.single("MySensor/HighHumi", "HumiHigh", hostname="test.mosquitto.org")
                
            else:
                HighHumi.off()
                
            if humidity <= 60 and humidity >= 30:
                GoodHumi.on()
                
            else:
                GoodHumi.off()
                
            if humidity < 30:
                LowHumi.on()
                publish.single("MySensor/LowHumi", "HumiLow", hostname="test.mosquitto.org")
                
            else:
                LowHumi.off()
            time.sleep(3)
    thread = threading.Thread(target = start)
    thread.start()
    
def SwitchOn ():
    global ok
    ok = True
    main()
    print("On")
    
def SwitchOff():
    global ok
    ok = False
    gui.destroy()
    print("Shutdown!")
    
    
    
    




On = Button(gui, text = "Turn On", command = SwitchOn, bg = "green", height = 2, width = 12)
Off = Button(gui, text = "Turn Off", command = SwitchOff, bg = "red", height = 2, width = 12)

On.grid(row=0,column=1)
Off.grid(row=2,column=1)


gui.mainloop()
