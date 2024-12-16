from functions import *
import time

turn_off_pico()

status = "off"

while True:
    
    data = input()

    if data == "on":
        status = "on"
    elif data == "off":
        status = "off"
        turn_off_pico()
        
    while status == "on":
        Show()
        blink_led()
        time.sleep(0.1)
        
        # if i add this the functions Show and blink_led will wait until there is a new input()
        data = input()
        
        if data == "off":
            turn_off_pico()
            break
            
        
    
