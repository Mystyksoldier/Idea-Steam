#test main.py for pico

from functions import *
import time

data = input()

while True:
    if data == "on":
        Show()
        blink_led()
        time.sleep(0.1)
    elif data == "off":
        turn_off_pico()
    else:
        turn_off_pico2()