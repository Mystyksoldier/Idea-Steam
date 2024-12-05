from serial.tools import list_ports
import serial
from functions import *

def read_serial(port):
    """Read data from serial port and return as string."""
    line = port.read(1000)
    return line.decode()

def picoCommand(command, serial_port):
    if command == "on":
        print("Sending 'on' command to Pico...")
        data = "on\r"  # Sends the command to turn the Pico on
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)
    elif command == "off":
        print("Sending 'off' command to Pico...")
        data = "off\r"  # Sends the command to put the Pico to sleep
        serial_port.write(data.encode())
        pico_output = read_serial(serial_port)
        pico_output = pico_output.replace('\r\n', ' ')
        print("[PICO] " + pico_output)

# Manually select the serial port that connects to the Pico
serial_ports = list_ports.comports()

print("[INFO] Serial ports found:")
for i, port in enumerate(serial_ports):
    print(str(i) + ". " + str(port.device))

pico_port = 'OM16'

# Open a connection to the Pico
with serial.Serial(port=pico_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
    if serial_port.isOpen():
        print("[INFO] Using serial port", serial_port.name)
    else:
        print("[INFO] Opening serial port", serial_port.name, "...")
        serial_port.open()

    while True:
        choice = pico_choice

        if choice == 'on':
            picoCommand('on', serial_port)
        elif choice == 'off':
            picoCommand('off', serial_port)
