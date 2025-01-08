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

def find_pico_port():
    serial_ports = list_ports.comports()
    for port in serial_ports:
        if "USB Serial Device" in port.description:
            return port.device
    return None

def pico_control_thread():
    global pico_choice
    pico_port = "COM16"
    serial_port = serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    
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
        pico_control_thread()
    elif pico_choice == "off":
        print("Pico is now OFF.")
        pico_control_thread()
    

