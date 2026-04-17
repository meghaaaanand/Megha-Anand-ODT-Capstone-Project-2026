import dht
import machine
from machine import Pin
import time
import neopixel

temphumi = dht.DHT22(Pin(14))
neo = neopixel.NeoPixel(Pin(12),16)

while True:
    try:
        temphumi.measure()  # take reading

        temp = temphumi.temperature()   # in °C
        hum = temphumi.humidity()
        print(temp)
        print(hum)
        time.sleep(0.2)
        if temp<27 and hum < 66:
            for i in range(16):
                neo[i] = (0,255,0)
                neo.write()
                time.sleep(0.1)
            for i in range(16):
                neo[i] = (0,0,0)
                time.sleep(0.1)
                neo.write()
        else :
            for i in range(16):
                neo[i] = (255,0,0)
                neo.write()
                time.sleep(0.1)
            for i in range(16):
                neo[i] = (0,0,0)
                time.sleep(0.1)
                neo.write()

    except OSError:
        print("Failed to read from sensor")

    time.sleep(2)