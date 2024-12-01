from machine import ADC, PWM, Pin, I2C
from pico_i2c_lcd import I2cLcd
import time
import machine
import neopixel
from data import *

led = Pin("LED", Pin.OUT)

time.sleep(0.5)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

acd = ADC(Pin(26))

acd_value = acd.read_u16()

np1 = neopixel.NeoPixel(machine.Pin(2), 30)
np1b = neopixel.NeoPixel(machine.Pin(2), 30)
np2 = neopixel.NeoPixel(machine.Pin(3), 30)

SPEED_OF_SOUND = 343

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

#Test if reboot was a succes
def updateConformLed():
    for _ in range(5):
        led(0)
        time.sleep(.1)
        led(1)
        time.sleep(.1)

#Friends List With lcd
def CalculateACDPResentage():
    listNumber = len(fruits)
    acd_value = acd.read_u16()
    return (acd_value / 65535) * listNumber - 1

previous_number = -1

def Show():
    global previous_number
    current_number = int(CalculateACDPResentage())

    if current_number != previous_number:
        previous_number = current_number
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(fruits[current_number][0])
        lcd.move_to(0, 1)
        lcd.putstr(fruits[current_number][1])
        
    
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

def blink_led():
    if measure_distance() < 0.15:
        for i in range(29, -1, -1):
            if i % 2 == 0:
                np1[i] = (255, 0, 0)
                np2[i] = (255, 255, 255)
                np1.write()
                np2.write()
                time.sleep(0.1)
                np1b[i] = (255, 0, 255)
                np1b.write()
                time.sleep(0.2)
            else:
                np1[i] = (0, 255, 255)
                np2[i] = (255, 0, 255)
                np1.write()
                np2.write()
                time.sleep(0.1)
    else:
        for i in range(30):
            np1[i] = (0, 0, 0)
            np2[i] = (0, 0, 0)
            np1.write()
            np2.write()
    
