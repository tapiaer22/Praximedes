#For modules
import logging.handlers
import os
import sys
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


def main():
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(run_prax())
    
async def run_prax(action = None):
    #Logger setup
    log_dir = os.path.join(os.path.dirname(__file__),'..','logs')
    logging.basicConfig(filename=os.path.join(log_dir,'mainLogs.log'), 
                            level=logging.INFO, 
                            format='%(asctime)s - %(levelname)s - %(name)s.%(funcName)s - %(message)s')
    logger = logging.getLogger("main_log")
    logger.setLevel(logging.INFO)
    logger.info(f"-----PRAXIMEDES SESSION STARTED-----")


    #Key words to enter Chill mode
    CHILL_MODE_WORDS = ["chill mode", "relaxed mode"]
    praximedes = Praximedes()

    #Try to transcribe what the user is saying.
    try:
        if not action:
            action = praximedes.transcribe_action().lower()
        #Check for key word 
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
        #--------------------------------
        else:
            praximedes.speak('You did not include a key word')
            logger.warning("No keyword was included")
        

    #If user did not say anything, or catch exceptions
    except (AttributeError, TypeError) as e:
        print(e)
        traceback.print_exception(type(e),e,e.__traceback__.tb_next)
        praximedes.speak("Praximedes was unable to hear anything!")


if __name__ == "__main__":
    main()