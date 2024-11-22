from machine import ADC, PWM, Pin, I2C
from pico_i2c_lcd import I2cLcd
import time

acd = ADC(Pin(26))

fruits = [
    ["Apple", "Apple Tree"],
    ["Banana", "Banana Tree"],
    ["Cherry", "Cherry Tree"],
    ["Date", "Date Palm Tree"],
    ["Elderberry", "Elder Tree"],
    ["Fig", "Fig Tree"],
    ["Grape", "Grape Vine"],
    ["Honeydew", "Melon Plant"],
    ["Indian Fig", "Indian Fig Tree"],
    ["Jackfruit", "Jackfruit Tree"],
    ["Kiwi", "Kiwi Vine"],
    ["Lemon", "Lemon Tree"],
    ["Mango", "Mango Tree"],
    ["Nectarine", "Nectarine Tree"],
    ["Orange", "Orange Tree"],
    ["Papaya", "Papaya Tree"],
    ["Quince", "Quince Tree"],
    ["Raspberry", "Raspberry Bush"],
    ["Strawberry", "Strawberry Plant"],
    ["Tangerine", "Tangerine Tree"]
]

time.sleep(0.5)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)


acd_value = acd.read_u16()

def CalculateACDPResentage():
    listNumber = len(fruits)
    acd_value = acd.read_u16()
    return (acd_value / 65535) * listNumber - 1


def Show():
    number = int(CalculateACDPResentage())
    if number != int(CalculateACDPResentage()):
        lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(fruits[int(number)][0])
    lcd.move_to(0, 1)
    lcd.putstr(fruits[int(number)][1])

while True:
    Show()


