from serial.tools import list_ports
import serial
from functions import *

def read_serial(port):
    line = port.read(1000)
    return line.decode()

def picoCommand(command, serial_port):
    if command == "on":
        print("Sending 'on' command to Pico...")
        data = "on\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)
    elif command == "off":
        print("Sending 'off' command to Pico...")
        data = "off\r"
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

def find_pico_port():
    serial_ports = list_ports.comports()
    for port in serial_ports:
        if "Pico" in port.description:
            return port.device
    return None
