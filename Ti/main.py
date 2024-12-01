#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Oriëntatie op TI

Voorbeeld voor communicatie met Raspberry Pi Pico. Flash dit bestand
eerst naar de Raspberry Pi Pico. Start dan in de folder serial/PC-serial `main.py` op je laptop/PC.

(c) 2022 Hogeschool Utrecht,
Hagen Patzke (hagen.patzke@hu.nl) en
Tijmen Muller (tijmen.muller@hu.nl)
"""

import time
from functions import *

updateConformLed()

while True:
    Show()
    blink_led()
    time.sleep(0.1)
    
    

