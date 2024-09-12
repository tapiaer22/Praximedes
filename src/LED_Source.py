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
    
    async def connect(self):
        try:
            self.client = BleakClient(self.device_address)
            if self.logs: self.logger.info(f"Connecting to device: {self.device_address}")
            print(f"Connecting to device: {self.device_address}")
            await self.client.connect()
            for service in self.client.services:
                if service.description == "Generic Access Profile":
                    for char in service.characteristics:
                        if self.logs: self.logger.info(f"Set RX_CHAR_UUID with {char.uuid}")
                        print(f"Set RX_CHAR_UUID with {char.uuid}")
                        self.RX_CHAR_UUID = char.uuid

                elif service.description == "Vendor specific":
                    for char in service.characteristics:
                        if (','.join(char.properties) == "write-without-response,write") and self.TX_CHAR_UUID == "":
                            if self.logs: self.logger.info(f"Set TX_CHAR_UUID with {char.uuid}")
                            print(f"Set TX_CHAR_UUID with {char.uuid}")
                            self.TX_CHAR_UUID = char.uuid
            if self.logs: self.logger.info(f"Connected to device {self.device_address}")
            print(f"Connected to device {self.device_address}")

        except Exception as e:
            if self.logs:self.logger.error(f"Failed to connect to LED: {e}")
            raise ConnectionError(f"Failed to connect to LED: {e}")
    
    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            if self.logs: self.logger.info(f"Disconnected from device {self.device_address}")
            print(f"Disconnected from device {self.device_address}")
        else:
            if self.logs: self.logger.info("Cannot disconnect: there is no device connected")
            print("Cannot disconnect: there is no device connected")

    async def scan_devices(self):
        try:
            if self.logs: self.logger.info("Scanning for LED devices...")
            print("Scanning for LED devices...")
            devices = await BleakScanner.discover(timeout=7.0)
            if devices:
                if self.logs: self.logger.info("Devices found:")
                print("Devices found:")
                #Show LED devices only
                for device in devices:
                    if str(device.name).startswith("QHM"):
                        if self.logs: self.logger.info(f"Name: {device.name}\t ID: {device.address}")
                        print(f"Name: {device.name}\t ID: {device.address}")
            else:
                if self.logs: self.logger.warning("No devices found! :[")
                print("No devices found! :[")
        except Exception as e:
            if self.logs: self.logger.error(f"Could not scan for devices: {e}")
            print(f"Could not scan for devices: {e}")                  

    async def change_color(self, R, G, B):
        # Check for connection
        if not self.client or not self.client.is_connected:
            if self.logs: self.logger.error("No LED device connected: cannot change color")
            raise ConnectionError("No LED device connected: cannot change color")
        # Send command to change color
        try:
            # Characteristic to change color
            brightness = (int(10 * 255 / 100) & 0xFF)
            color_command = bytearray([86, R, G, B, brightness, 256-16, 256-86])

            # Write the command to the characteristic
            await self.client.write_gatt_char(self.TX_CHAR_UUID, color_command)
            if self.logs: self.logger.info(f"Color R:{R} G:{G} B:{B} command sent")
            print(f"Color R:{R} G:{G} B:{B} command sent")

        except Exception as e:
            if self.logs: self.logger.error(f"Failed to send colors to LED source: {e}")
            raise Exception(f"Failed to send colors to LED source: {e}")

    async def change_power(self, state="ON"):
        # Check for connection
        if not self.client or not self.client.is_connected:
            if self.logs: self.logger.error("No LED device connected: cannot change color")
            raise ConnectionError("No LED device connected")
        
        # Set command values
        if state == "0" or state == "OFF":
            mode = 36   # Value for Off
            state = "OFF"
        else: 
            mode = 35   # Value for ON
            state = "ON"
        power_command = bytearray([204,mode,51])

        # Write the command to the characteristic
        await self.client.write_gatt_char(self.TX_CHAR_UUID, power_command)
        if self.logs: self.logger.info(f"Turn {state} LED command sent")
        print(f"Turn {state} LED command sent")
    
    async def change_mode(self, idx):
        # Check for connection
        if not self.client or not self.client.is_connected:
            if self.logs: self.logger.error("No LED device connected: cannot change color")
            raise ConnectionError("No LED device connected")
         
        # Set command values
        mode_value = self.Modes[idx]
        mode_command = bytearray([256 - 69, mode_value, (self.Speed & 0xFF), 68])

        # Write the command to the characteristic
        await self.client.write_gatt_char(self.TX_CHAR_UUID, mode_command)

        if self.logs: self.logger.info(f"Change Mode with ID {mode_value} Speed {self.Speed}")
        print(f"Change Mode with ID {mode_value} and Speed {self.Speed}")

    async def ChillMode(self):
        # Check for connection
        if not self.client or not self.client.is_connected:
            if self.logs: self.logger.error("No LED device connected")
            raise ConnectionError("No LED device connected")

        await self.change_power("ON")
        #Change mode to pulsating purple, and slow pulsating rate
        self.Speed = 9
        await self.change_mode(6)

        if self.logs: self.logger.info("Chill mode on LED set!")
        print("Chill mode on LED set!")

    #Missing function to change speed