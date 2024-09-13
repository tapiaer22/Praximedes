# Praximedes
Control LED lights (HappyLighting), play music, and input voice commands with python! 

## [LED_Source.py](https://github.com/tapiaer22/Praximedes/blob/main/src/LED_Source.py)
Easily light up your space with `LED_Source`! 💡✨

This module contains the class `LED_Source` that could be used to manipulate LED lights from Happy Lighting by using python code. All methods are async and awaitable, 

Initialization:
```python
led = LED_Source(device_address, logs=True)  #  Initialize class (with logs by default)
```
- **device_address**: the mac address of the BLE device (required)
- **logs**: output logs and messages to a file (optional)

Actions:
- **Connect**:
  <br>After initializing the class, you must use the `async connect()` method to start a BLE connection
```python
led = LED_Source("00:00:00:00:00:00")  #  Initialize class (with logs by default)
await led.connect()
await led.disconnect()
```
- Disconnect
- Turn LED lights ON/OFF
- Scan for LED devices nearby
- Change color of LED lights
- Change mode of LED lights
- Chill mode (customizeed method)
## Praximedes.py

## Spotify_Controller.py

## main.py

## config
### colors.json
### devices.json
### spotify_client_info.json
### custom.json
