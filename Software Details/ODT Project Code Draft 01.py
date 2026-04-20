#Import all modules ie neopixel, dht, from machine import pin, time, machine in general
# SENSORS USED ::::: Temperature, Ultrasonic for water level, LDR, Humidity, PH sensor probe (IDEALLY)
# APP Interface along with it :::Digitally monitor, Water level of reservoir, TEMP, HUMIDITY, LIGHT RECEIVED, WHEN WAS IT LAST WATERED.
#Time.ticks continous timer or timer in app

import machine
from machine import Pin, time_pulse_us
import neopixel
import time
import dht
import bluetooth
import random
#coding for relay module how does it work


conn_handle = None
value = ""
name = "Megha ESP32" #Name of Your ESP32 (Change it to avoid Confusion)
ble = bluetooth.BLE()

ble.active(False)
time.sleep(0.5)
ble.active(True)
ble.config(gap_name=name)

service_UUID = bluetooth.UUID("6e400001-b5a3-f393-e0a9-e50e24dcca9e")
char_UUID = bluetooth.UUID("6e400002-b5a3-f393-e0a9-e50e24dcca9e")

char = (char_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY)
service = (service_UUID, (char,),)
((char_handle,),) = ble.gatts_register_services((service,))

def event_occured(event, data):
    global conn_handle 
    if event == 1:
        conn_handle = data[0]
        print("Connected")
    elif event == 2:
        conn_handle = None
        print("Disconnected")
        advertise(name)
                  
def advertise(device_name):
    name_bytes = device_name.encode()
    flags = bytearray([0x02, 0x01, 0x06])
    short_name = bytearray([len(name_bytes) + 1, 0x08]) + name_bytes
    full_name = bytearray([len(name_bytes) + 1, 0x09]) + name_bytes
    adv_data = flags + short_name + full_name
    ble.gap_advertise(50, adv_data=adv_data)
    print("Awating Connection...Advertising as:", device_name)


ble.irq(event_occured)
advertise(name)

#for ultrasonic sensor : Brown = VCC, Grey = GND, White = Echo , Black = Trig 
neo = neopixel.NeoPixel(Pin(12),16)
temphumi = dht.DHT22(Pin(14))
buzz = Pin(21,Pin.OUT)
trig = Pin(18, Pin.OUT)
echo = Pin(23, Pin.IN)
ldr1 = Pin(25, Pin.IN, Pin.PULL_UP) #top on circuit
ldr2 = Pin(32, Pin.IN, Pin.PULL_UP) #bottom on circuit
ldr3 = Pin(34, Pin.IN, Pin.PULL_UP) # middle circuit

for i in range(16):
    neo[i] = (0,0,0)
neo.write()
time.sleep(1)



#def functions for : Temp and Humidity Sensor (20 to 25 degree celsius) , Ultrasonic for water level, LDR (time ticks until 5-6 hours)

#alert when temp, humidity, and water level go haywire.

def TH() :
    try:
        temphumi.measure() 
        temp = temphumi.temperature() 
        hum = temphumi.humidity()
        print(temp)
        print(hum)
        return temp, hum

    except OSError:
        print("Failed to read from sensor")
        return -100, -100

    
def waterlevel():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()
    duration = time_pulse_us(echo, 1, 30000)  # 30 ms timeout
    if duration < 0:
        print("No object detected (Timeout)")
        return 100
    else:
        distance = duration / 58
        print("Distance:", distance, "cm")
        return distance
    
    
def ldrtop():
    lightval1 =ldr1.value()
    return lightval1
    #if lightval1 == 0 light detected

def ldrmiddle():
    lightval2 =ldr2.value()
    return lightval2
    #if lightval1 == 0 light detected

def ldrbottom():
    lightval3 =ldr3.value()
    return lightval3
    #if lightval1 == 0 light detected
    
def sysgood():
    for i in range(16):
        neo[i] = (0,255,0)
    neo.write()
    buzz.off()
    
def syswarning():
    for i in range(16):
        neo[i] = (255,255,0)
    neo.write()
    buzz.on()
    time.sleep(0.2)
    buzz.off()
    time.sleep(0.5)
        
def systrouble():
    for i in range(16):
        neo[i] = (255,0,0)
    neo.write()
    buzz.on()
    time.sleep(0.2)
    buzz.off()
    time.sleep(0.1)
    
    
    

while True:
    temp, hum = TH()
    water = waterlevel()
    top = ldrtop()
    middle = ldrmiddle()
    bottom = ldrbottom()

    # count light sensors detecting light
    ldrcount = 0
    if top == 0:
        ldrcount = ldrcount + 1
    if middle == 0:
        ldrcount = ldrcount + 1
    if bottom == 0:
        ldrcount = ldrcount + 1

#trouble conditions red beep beep 
    if temp == -100 or hum == -100:
        systrouble()
        status = "TROUBLE : DHT sensor not working!"

    elif temp < 18:
        systrouble()
        status = "TROUBLE : Temperature below recommended! "
        
    elif temp > 30:
        systrouble()
        status = "TROUBLE : Temperature above recommended! "

    elif hum < 40:
        systrouble()
        status = "TROUBLE : Humidity below recommended!"
        
    elif hum > 80:
        systrouble()
        status = "TROUBLE : Humidity above recommended!"

    elif water > 25:
        systrouble()
        status = "TROUBLE : Low water level! Please Refill!"

    elif ldrcount == 0:
        systrouble()
        status = "TROUBLE : No light being received!"

#warning condition yellow
    elif (18 <= temp < 20):
        syswarning()
        status = "WARNING : Temperature about to go below recommended!"
        
    elif (28 < temp <= 30):
        syswarning()
        status = "WARNING : Temperature about to go above recommended!"

    elif (40 <= hum < 45):
        syswarning()
        status = "WARNING : Humidity about to go below recommended!"
    
    elif (75 < hum <= 80):
        syswarning()
        status = "WARNING : Humidity about to go above recommended!"

    elif water > 20:
        syswarning()
        status = "WARNING : Water level about to go down!"

    elif ldrcount == 1 or ldrcount == 2:
        syswarning()
        status = "WARNING : Partial light on hydroponic system!"

    # GOOD CONDITION
    else:
        sysgood()
        status = "GOOD"

    # ---------------- DEBUG PRINT ----------------
    print("Ambient Temperature :", temp)
    print("Ambient Humidity:", hum)
    print("Water Level:", water)
    print("Top:", top, "Middle:", middle, "Bottom:", bottom)
    print("System Status:", status)

    data = "Ambient Temperature :{}, Ambient Humidity :{},Water Level :{:.2f},Top LDR :{},Middle LDR :{},Bottom LDR :{},System Status :{}".format(
        temp, hum, water, top, middle, bottom, status
    )

    ble.gatts_write(char_handle, data.encode())

    if conn_handle is not None:
        ble.gatts_notify(conn_handle, char_handle)
    
    time.sleep(1)