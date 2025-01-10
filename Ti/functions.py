from machine import ADC, PWM, Pin, I2C
from pico_i2c_lcd import I2cLcd
import time
import machine
import neopixel
import sys
from data import *

led = Pin("LED", Pin.OUT)

time.sleep(0.5)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

i2c_1 = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)
I2C_ADDR_1 = i2c_1.scan()[0]
lcd_1 = I2cLcd(i2c_1, I2C_ADDR_1, 2, 16)



rbutton = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)

lbutton = Pin(13, Pin.IN, pull=Pin.PULL_DOWN)

acd = ADC(Pin(26))

acd_value = acd.read_u16()

np1 = neopixel.NeoPixel(machine.Pin(2), 30)

SPEED_OF_SOUND = 343

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

def turn_off_pico():
    global previous_number
    previous_number = -1
    lcd.clear()
    lcd_1.clear()
    lcd.hal_backlight_off
    for i in range(30):
        np1[i] = (0, 0, 0)
    np1.write()
    
#Test if reboot was a succes
def updateConformLed():
    for _ in range(5):
        led(0)
        time.sleep(.1)
        led(1)
        time.sleep(.1)


def getFriends():
    return [friend for friend in friends if friend["friend_status"] == "Online"]

FriendsList = getFriends()

#Friends List With lcd
def CalculateACDPResentage():
    listNumber = len(FriendsList)
    acd_value = acd.read_u16()
    return (acd_value / 65535) * listNumber - 1

previous_number = -1

def Show():
    global previous_number
    current_number = int(CalculateACDPResentage())

    if current_number != previous_number: #prevstate != on
        previous_number = current_number
        friend = FriendsList[current_number]
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(friend["friend_name"])
        lcd.move_to(0, 1)
        lcd.putstr(friend["current_game"])
        
#the hover lights
    
def measure_distance():
    # Send a 10 microsecond pulse to trigger the sensor
    trigger_pin.value(0)
    time.sleep_us(2)
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)
    
    
    # Wait for the echo_pin and measure the time
    while echo_pin.value() == 0:
        start_time = time.ticks_us()
    
    while echo_pin.value() == 1:
        end_time = time.ticks_us()
    
    # Calculate elapsed time in microseconds
    elapsed_time = time.ticks_diff(end_time, start_time)
    
    # Calculate the distance
    distance = (SPEED_OF_SOUND * elapsed_time) / (2 * 1_000_000)
    return distance

def led():
    ledcolor = (255, 0, 255)
    for i in range(30):
        np1[i] = ledcolor
        np1.write()

def blink_led():
    if measure_distance() < 0.15:
        for i in range(30):
            if i % 2 == 0:
                np1[i] = (255, 0, 0)
                np1.write()
                time.sleep(0.1)
            else:
                np1[i] = (0, 255, 255)
                np1.write()
                time.sleep(0.1)
    else:
        led()
        
        
number = 0


sensor = machine.ADC(4)

def read_temperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value            
    temperature = 27 - (volt - 0.706) / 0.001721
    return int(temperature)


def lcd_temp():
    lcd_1.clear()
    lcd_1.move_to(1, 0)
    lcd_1.putstr("Steam Box temp") 
    lcd_1.move_to(2, 1)
    lcd_1.putstr(f"{read_temperature()}°C")
    
def cpu_temp():
    lcd_1.clear()
    lcd_1.move_to(2, 0)
    lcd_1.putstr("CPU temp") 
    lcd_1.move_to(2, 1)
    lcd_1.putstr("70°C")

def gpu_temp():
    lcd_1.clear()
    lcd_1.move_to(2, 0)
    lcd_1.putstr("GPU temp") 
    lcd_1.move_to(2, 1)
    lcd_1.putstr("65°C")
    
functions = [lcd_temp, cpu_temp, gpu_temp]

current_function_index = 0

def menuOptions():
    global current_function_index
    
    if rbutton.value():
        current_function_index = (current_function_index + 1) % len(functions)
        functions[current_function_index]()
    
    if lbutton.value():
        current_function_index = (current_function_index - 1) % len(functions)
        functions[current_function_index]()
        