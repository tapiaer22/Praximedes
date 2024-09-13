# Praximedes
Control LED lights (HappyLighting), play music, and input voice commands with python! 

## [LED_Source.py](https://github.com/tapiaer22/Praximedes/blob/main/src/LED_Source.py)
Easily light up your space with `LED_Source`! 💡✨

This module contains the class `LED_Source` that could be used to manipulate LED lights from Happy Lighting by using python code. All methods are async and awaitable, 

### Initialization:
```python
led = LED_Source(device_address, logs=True)  #  Initialize class (with logs by default)
```
- **device_address**: the MAC address of the BLE device (required)
- **logs**: output logs and messages to a file (optional)

### Methods:
- `connect()`
  <br>After initializing the class, you must use the `async connect()` method to start a BLE connection
```python
led = LED_Source("00:00:00:00:00:00")  #  Initialize class (with logs by default)
await led.connect()  # Connect to 00:00:00:00:00:00
```

- `disconnect()`
  <br>Assuming you had a connection with the BLE device, you can manually disconnect from it
```python
await led.disconnect()  # Manually disconnect from current BLE device
```

- `change_power(state="ON")`
  <br>Turn on LED lights with parameter state="ON", or turn off LED lights with state="OFF"
```python
await led.change_power(state="ON")    # Turrn on LED lights
await led.change_power(state="OFF")   # Turn off LED lights
await led.change_power()  # Turns on LED lights by default
```
  
- `scan_devices()`
  <br>Scans for nearby LED devices from Happy Lighting, printing their name and MAC address 
```python
await led.scan_devices()  # Scan for Happy Lighting LED devices
# Output:
# Devices found:
# Name: QHM-LED0  ID: 00:00:00:00:00:00
# Name: QHM-LED1  ID: 00:00:00:00:00:01
```
  
- `change_color(R,G,B)`
  <br>Changes the color of LED lights using RGB values
  - R: red component of color (int between 0 and 255)
  - G: green component of color (int between 0 and 255)
  - B: blue component of color (int between 0 and 255)
```python
await led.change_color(255,0,0)  # Change color to RED
await led.change_color(128,0,128)  # Change color to PURPLE
await led.change_color(0,255,0)  # Change color to GREEN
```
  
- `change_mode(idx)`
  <br>Changes mode of LED lights. There are 23 modes, so idx stands for the index of the known modes. idx is an int between 0 - 22 (inclusive), and the modes could be found in the module [here](https://github.com/tapiaer22/Praximedes/blob/main/src/LED_Source.py)
```python
await led.change_mode(0)  # Pulsating rainbow
await led.change_mode(1)  # Pulsating red
await led.change_mode(9)  # Pulsating red/blue
```
  
- `ChillMode()`
  <br>Customized chill feature made by the developer. Sets the LED lights to a chill color and customized settings for a chill environment
```python
await led.ChillMode()  # Set LED to a chill environment
```

### Examples
A simple scenario to turn on lights, change color to red, and disconnect from the device
```python
import asyncio
# Put class LED_Source with dependencies here, or import it

async def yeah():
    led = LED_Source("MAC address here")    #Initialize LED source
    await led.connect()     # Connect to device
    await led.change_power()    # Turn on device
    await led.change_color(255,0,0)     # Change LED light color to Red
    await led.disconnect()  # Disconnect from device (optional)

asyncio.run(yeah())     # Run async function
```

A scenario to turn on lights and change to mode Pulsating green/blue
```python
import asyncio
# Put class LED_Source with dependencies here, or import it

async def green_blue():
    led = LED_Source("MAC address here")    #Initialize LED source
    await led.connect()     # Connect to device
    await led.change_power()    # Turn on LED lights
    await led.change_mode(10)    # Change mode to Pulsating green/blue

asyncio.run(green_blue())     # Run async function
```

A scenario to engage in chill mode
```python
import asyncio
# Put class LED_Source with dependencies here, or import it

async def set_chill():
    led = LED_Source("MAC address here")    #Initialize LED source
    await led.connect()     # Connect to device
    await led.ChillMode()   # set LED lights to a chill environment

asyncio.run(set_chill())     # Run async function
```

## Praximedes.py

## Spotify_Controller.py

## main.py

## config
### colors.json
### devices.json
### spotify_client_info.json
### custom.json
