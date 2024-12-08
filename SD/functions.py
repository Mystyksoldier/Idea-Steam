from userdata import users
import os
import threading
import serial
import time
from pico_functions import *

def onlineFriends():
    return [user for user in users if user["status"] == "online"]

def printOnlineFriends(friend):
    print(friend["username"])

def pico_control_thread():
    global pico_choice
    serial_ports = list_ports.comports()
    pico_port = serial_ports[0].device
    serial_port = serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    
    if serial_port.isOpen():
        print("[INFO] Pico system connected.")
        if pico_choice == "on":
            picoCommand("on", serial_port)
        elif pico_choice == "off":
            picoCommand("off", serial_port)

def picoOnOrOff(command):
    global pico_choice
    pico_choice = command
    if pico_choice == "on":
        print("Pico is now ON.")
    elif pico_choice == "off":
        print("Pico is now OFF.")
    
    threading.Thread(target=pico_control_thread, daemon=True).start()
