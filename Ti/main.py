from functions import *
from database import *
import time
import select
import sys
import machine


turn_off_pico()
data = "off"

def usb_any():
    rlist, _, _ = select.select([sys.stdin], [], [], 0)  # Non-blocking check
    return bool(rlist)

while True:
        
    if data != "on":
        data = input()
    
    if data == "on":

        Show()
        blink_led()
        menuOptions()

        if usb_any():
            data = input()
        else:
            continue
       
    if data == "off":
        print("Received off")
        turn_off_pico()
    
