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

class LED_Source():
    def __init__(self, device_address, logs=True):
        self.device_address = device_address
        self.RX_CHAR_UUID = ""
        self.TX_CHAR_UUID = ""
        self.client = None
        self.Modes = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 
         47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 
         97, 98, 99]
        self.Speed = 5
        
        #For logs
        self.logs = logs
        if self.logs:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"{self.__class__.__name__} initialized")