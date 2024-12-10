import threading
import serial
import time
from pico_functions import *

def find_pico_port():
    serial_ports = list_ports.comports()
    for port in serial_ports:
        if "USB Serial Device" in port.description:
            return port.device
    return None

print(find_pico_port())

