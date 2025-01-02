#For modules
import logging.handlers
import os
import sys
import speech_recognition as sr
#For async functionalities
import asyncio
from PyQt5.QtWidgets import QApplication
import qasync
#Classes for Praximedes tools
from Praximedes import Praximedes
#For Logging
import traceback, logging
#For ML
import re
#For parsing arguments in terminal
import argparse
import json


def main():
    #Handle arguments from terminal/command-line
    try:
        user_action = handle_args()
    except Exception as e:
        print(f"Failed to parse arguments: {e}")
    except SystemExit as se:
        exit()

    #Start application
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(run_prax(action=user_action))
    

async def run_prax(action = None):
    # Log setup
    logger = log_setup()

    # Praximedes setup
    praximedes = Praximedes()

    # Custom key words list
    CHILL_MODE_WORDS = ["chill mode", "relaxed mode"]
    TERMINATE_WORDS = ["terminate", "stop listening"]
    
    # Greet message and wake word setup
    wake_word = "computer"
    praximedes.speak("Ready to listen for commands, boss")
    praximedes.speak(f"My wake word is: {wake_word}")
    print("Say 'alpha nova' to start")

    # Listen until termination
    while True:
        recognizer = sr.Recognizer()
        my_audio = listen_for_wake_word(recognizer)
        print(my_audio)
        
        # Take action when wake word was said
        if (wake_word in str(my_audio)) or (action != None):

            # Try to transcribe what the user is saying and do an action
            try:
                if not action:
                    action = praximedes.transcribe_action().lower()
                
                # Check for key word 
                if any(word in action for word in CHILL_MODE_WORDS):
                    await praximedes.engage_chillmode()
                elif all(word in action for word in ["turn off", "lights"]):
                    await praximedes.LED_turnOff()
                elif all(word in action for word in ["turn on","lights"]):
                    await praximedes.LED_turnOn()
                elif all(word in action for word in ["change","color"]):
                    pattern = r'change\s+(?:the\s+)?color\s+(?:of\s+)?(?:led\s+)?(?:lights\s+)?+to\s+(\w+)'
                    matches = re.findall(pattern,action, re.IGNORECASE)
                    print(f"matches :{matches}")
                    if len(matches) == 0 or matches[0].lower() == "anything":
                        matches = ['random']
                    await praximedes.LED_changeColor(matches[0])
                #-------- ON DEVELOPMENT --------
                elif any(word in action for word in ["my spotify playlists", "my playlists"]):
                    playlists = praximedes.spotify_controller.get_playlists()
                    praximedes.speak(f"Here are your spotify visible playlists: {", ".join(playlists[:-1])} and {playlists[-1]}.")
                elif any(word in action for word in ["spotify devices", "spotify connected devices"]):
                    spotify_devices = praximedes.spotify_controller.get_connected_devices()
                    devices = [d['name'] for d in [device for device in spotify_devices]]
                    devices_id = [d['id'] for d in [device for device in spotify_devices]]
                    print(f"IDs in order: {devices_id}")
                    #praximedes.speak(f"You have {len(devices)} {"devices" if len(devices)>1 else "device"} available for spotify{"... Sad" if len(devices) == 0 else (f": {devices[0]}" if len(devices) == 1 else f": {devices[:-1]} and {devices[-1]}")}")
                    if len(devices) == 0:
                        praximedes.speak("You have no available devices for spotify... Sad")
                    elif len(devices) == 1:
                        praximedes.speak(f"You have 1 device available for spotify: {devices[0]}")
                    else:
                        praximedes.speak(f"You have {len(devices)} devices available for spotify: {devices[:-1]} and {devices[-1]}")
                elif any(word in action for word in ["play", "play song"]):
                    words = action.split()

                    # Check if "on device" is present in the input
                    if "on" in words and "device" in words:
                        device_index = words.index("device")
                        device = words[device_index + 1]  # Get the device name
                        words = words[:device_index]  # Remove "on device" part from the words list
                    if "by" in words and "from" in words:
                        # Scenario: "Play song la corriente by bad bunny from album Un Verano Sin Ti"
                        artist_index = words.index("by")
                        artist = " ".join(words[artist_index + 1:words.index("from")])
                        album_index = words.index("from")
                        album = " ".join(words[album_index + 1:])
                        song = " ".join(words[2:artist_index])  # Assuming song title is before "by"
                        keywords = words[2:artist_index] + words[artist_index + 1:album_index]
                    elif "by" in words:
                        # Scenario: "Play la corriente by bad bunny"
                        artist_index = words.index("by")
                        artist = " ".join(words[artist_index + 1:])
                        song = " ".join(words[1:artist_index])  # Assuming song title is before "by"
                        keywords = words[1:artist_index]
                        album = None
                    else:
                        # Scenario: "Play la corriente"
                        song = " ".join(words[1:])
                        keywords = words[1:]
                        artist = None
                        album = None
                    print(f"{song}, {album}, {artist}, {keywords}")
                    praximedes.spotify_controller.play_song(artist=artist,track=song,album=album)
                elif any(word in action for word in ["they not like us"]):
                    praximedes.spotify_controller.Play_on_thisPC()
                    praximedes.spotify_controller.play_song(artist="kendrick lamar", track="not like us", at_second=74, device_id=praximedes.spotify_controller.get_active_device())
                    #They not like us!!
                    praximedes.engine.setProperty('rate',173)
                    await asyncio.sleep(0.6)
                    praximedes.speak("<pitch middle='8'>They not like us - They not like us: THEY NOT LIKE us!</pitch>")
                    #Reset settings
                    praximedes.set_voice_settings()
                elif any(word in action for word in ["scan for led devices"]):
                    await praximedes.led_lights_handler.scan_devices()
                #-------- Spotify basic actions --------
                elif any(word in action for word in ["pause"]):
                    praximedes.spotify_controller.pause()
                elif any(word in action for word in ["resume"]):
                    praximedes.spotify_controller.resume()
                elif any(word in action for word in ["next song"]):
                    praximedes.spotify_controller.next_track()
                #--------------------------------
                # Check for key word to terminate program
                elif any(word in action for word in TERMINATE_WORDS):
                    praximedes.speak("Terminating program...")
                    raise SystemExit("Exiting the program...")
                else:
                    praximedes.speak('You did not include a key word')
                    logger.warning("No keyword was included")
                

            #If user did not say anything
            except (AttributeError, TypeError) as e:
                print(e)
                traceback.print_exception(type(e),e,e.__traceback__.tb_next)
                praximedes.speak("Praximedes was unable to hear anything!")
            

            # Report errors and exceptions
            except Exception as e:
                print(e)
                praximedes.speak(f"Something went wrong with the command: {action}")
        
        action = None


# Argument Parser handler
def handle_args():
    # Parse arguments
    parser = argparse.ArgumentParser(description="Perform actions via command-line arguments.")
    
    # Add arguments
    parser.add_argument(
        '-m', '--mac', type=str, help="MAC address of the LED device."
    )
    parser.add_argument(
        '-n', '--name', type=str, help="Name of the LED device."
    )
    parser.add_argument(
        '-a', '--action', type=str, help="Action to perform: 'turn on lights', 'turn off lights', or 'change color to [color]', 'scan for led devices'."
    )
    
    # Parse the arguments
    args = parser.parse_args()
    current_dir = os.path.dirname(__file__)

    # Update led devices
    if args.mac and args.name:
        name = str(args.name)
        mac = str(args.mac)

        devices_dir = os.path.join(current_dir,"..","config","devices.json")
        
        # Get current devices
        with open(devices_dir, "r") as devices_file:
            devices = json.load(devices_file)
        
        # Ensure 'LED_devices' is a dictionary in the JSON
        if 'LED_devices' not in devices or not isinstance(devices['LED_devices'], dict):
            devices['LED_devices'] = {}

        # Add device as default (on top of dictionary)
        updated_devices = {name: mac}
        updated_devices.update(devices['LED_devices'])
        devices['LED_devices'] = updated_devices

        # Write updated devices to JSON file
        with open(devices_dir, "w") as devices_file:
            json.dump(devices,devices_file, indent=2)
            print(f"Updated {devices_file} succesfully! added {name}: {mac} as default")
        
        raise SystemExit("Exiting the program...")

    # Return action from 
    return str(args.action) if args.action else None


# Setup for logs
def log_setup():
    #Logger setup
    logs_folder = "logs"
    
    # Check if the folder exists; if not, create it
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
        print(f"'{logs_folder}' folder created.")
    else:
        print(f"'{logs_folder}' folder: good ✅")

    #Configure logger to get logs
    log_dir = os.path.join(os.path.dirname(__file__),'..','logs')
    logging.basicConfig(filename=os.path.join(log_dir,'mainLogs.log'), 
                            level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - %(message)s')
    logger = logging.getLogger("mainLogs")
    logger.setLevel(logging.INFO)
    logger.info(f"-----PRAXIMEDES SESSION STARTED-----")

    #Return current state of logger
    return logger


# Listen for wake word
def listen_for_wake_word(recognizer):
    with sr.Microphone() as source:
        #Adjust for ambien sound
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Noise calibration
        
        try:
            # Listen for wake word
            print("Listening for wake word...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.WaitTimeoutError:
            return None  # No audio detected
        except sr.UnknownValueError:
            return None  # Speech not recognized
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return None


if __name__ == "__main__":
    main()