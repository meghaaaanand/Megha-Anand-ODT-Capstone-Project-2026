from machine import Pin, time_pulse_us
import time
# Define Trigger and Echo pins
trig = Pin(18, Pin.OUT)
echo = Pin(4, Pin.IN)
buzz = Pin(21,Pin.OUT)

while True:
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000) 
    if duration < 0:
        print("No object detected (Timeout)")
    else:
        
        distance = duration / 58
        if distance <12:
            buzz.on()
            time.sleep(0.1)
            buzz.off()
            time.sleep(0.1)
            
        print("Distance:", distance, "cm")
        

    time.sleep(0.1)