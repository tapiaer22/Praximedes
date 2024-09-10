import logging
from bleak import BleakClient, BleakScanner
from functools import wraps

'''
Below are the modes that can be used:
    "Pulsating rainbow": 37,
    "Pulsating red": 38,
    "Pulsating green": 39,
    "Pulsating blue": 40,
    "Pulsating yellow": 41,
    "Pulsating cyan": 42,
    "Pulsating purple": 43,
    "Pulsating white": 44,
    "Pulsating red/green": 45,
    "Pulsating red/blue": 46,
    "Pulsating green/blue": 47,
    "Rainbow strobe": 48,
    "Red strobe": 49,
    "Green strobe": 50,
    "Blue strobe": 51,
    "Yellow strobe": 52,
    "Cyan strobe": 53,
    "Purple strobe": 54,
    "white strobe": 55,
    "Rainbow jumping change": 56,
    "Pulsating RGB": 97,
    "RGB jumping change": 98,
    "Music Mode": 99
'''

