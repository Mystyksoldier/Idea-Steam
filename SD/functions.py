from userdata import users
import os

def onlineFriends():
    return [user for user in users if user["status"] == "online"]

def printOnlineFriends(friend):
    print(friend["username"])

global pico_choice
pico_choice = "off"

def picoOnOrOff(command):
    if command == "on":
        pico_choice = "on"
        print("Pico is now on.")
    elif command == "off":
        pico_choice = "off"
        print("Pico is now off.")

    if pico_choice == "on":
        os.system("python SD\pico_functions.py")
