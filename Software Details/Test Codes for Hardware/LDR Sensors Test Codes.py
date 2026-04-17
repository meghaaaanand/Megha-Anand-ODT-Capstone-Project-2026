from machine import Pin
import time


ldr1 = Pin(25, Pin.IN, Pin.PULL_UP)
ldr2 = Pin(32, Pin.IN, Pin.PULL_UP)
ldr3 = Pin(34, Pin.IN, Pin.PULL_UP)
buzz = Pin(21,Pin.OUT)


while True:
    # Read sensor values continously
    
    val1 = ldr1.value()
    val2 = ldr2.value()
    val3 = ldr3.value()
    

#Make each if statement comment and check each ldr sensor 1 by 1
    
    if val1== 0:
        buzz.on()
        time.sleep(0.1)
        buzz.off()
        time.sleep(1)
        print("Light Detected")
    if val2 == 0:
        print("Light Detected")
        buzz.on()
        time.sleep(0.1)
        buzz.off()
        time.sleep(1)
    if val3 == 0:
        print("Light Detected")
        buzz.on()
        time.sleep(0.1)
        buzz.off()
        time.sleep(1)
    
    else:
        print("no light") 

        
    time.sleep(0.2)