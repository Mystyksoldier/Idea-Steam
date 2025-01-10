from userdata import *
from session import Session
import serial
from pico_functions import *
import json
import json
from serial.tools import list_ports
from database import *

session = Session()

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
        picoCommand(pico_choice, serial_port)
    elif pico_choice == "off":
        picoCommand(pico_choice, serial_port)


def picoOnOrOff(command):
    global pico_choice
    pico_choice = command
    if pico_choice == "on":
        print("Pico is now ON.")
        pico_control_thread()
    elif pico_choice == "off":
        print("Pico is now OFF.")
        pico_control_thread()
    

def load_session_data():
    try:
        with open('session_data.json', 'r') as f:
            session_data = json.load(f)
            return session_data.get('username', None)
    except FileNotFoundError:
        return None
    

def getData():
    username = load_session_data()
    get_steam_data_for_user(username)

def top3games():
    # Load all game data
    games = load_game_data()

    # Sort games by playtime in descending order and get the top 3
    sorted_games = sorted(games, key=lambda x: x[2], reverse=True)[:3]

    # Prepare the top 3 games for display with numbering
    top3games = []
    for index, game in enumerate(sorted_games, start=1):
        game_name = game[1]
        playtime_hours = game[2]
        top3games.append(f"{index}. {game_name}: {playtime_hours} hrs")  # Add numbering to each game

    return top3games





