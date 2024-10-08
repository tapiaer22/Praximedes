#For async functionalities
import asyncio, os, sys
import random
#Classes for Praximedes tools
from Spotify_Controller import Spotify_Controller
import spotipy
from LED_Source import LED_Source
import speech_recognition as sr, pyttsx3
#For Logging
import logging
#For saved data, settings, and other functionalities
import json
sys.coinit_flags = 0



#Praximedes voice assistant class
class Praximedes:
    def __init__(self, logs=True, print_speech=True, confirmation_message="Hell yeah boss..."):
        self.__current_dir = os.path.dirname(__file__)                      #Used to access config files
        self.__config_dir = os.path.join(self.__current_dir,'..','config')  #Used for config files
        self.engine = pyttsx3.init()                                        #Used for the voice assistant
        self.recognizer = sr.Recognizer()                                   #Used to listen, recognize, and transcribe
        self.logs = logs
        if self.logs: self.logger = logging.getLogger(self.__class__.__name__)


        #Try to connect with Spotify API for Spotify feature
        try:
            with open(os.path.join(self.__config_dir,'spotify_client_info.json'), "r") as json_file:
                CLIENT_INFO = json.load(json_file)
            self.spotify_controller = Spotify_Controller(CLIENT_INFO["SPOTIFY_CLIENT_ID"],CLIENT_INFO["SPOTIFY_CLIENT_SECRET"])
        except Exception as e:
            self.spotify_controller = None



        #Try to assign LED lights device
        try:
            with open(os.path.join(self.__config_dir,'devices.json'), "r") as json_file:
                DEVICES = json.load(json_file)
            first_key = list(DEVICES["LED_devices"].keys())[0]
            mac_add = DEVICES["LED_devices"][first_key]
            self.led_lights_handler = LED_Source(mac_add, logs=True)
        except Exception as e:
            self.led_lights_handler = None
        
        
        #Praximedes settings for class
        self.print_speech = print_speech
        self.confirmation_message = confirmation_message
        self.voice_settings ={
            "voice": "female",  #voice: either 'male' or 'female' (using pyttsx3)
            "rate": 180,        #rate: WPM range 60 - 300
            "volume": 1.0       #volume: vol range 0.0 - 1.0
        }
        self.set_voice_settings()

        #Log status of Praximedes
        if self.logs: self.logger.info("Praximedes initialized :]")

    #Say a message
    def speak(self, message=""):
        if message == "":
            message = "You forgot to include a message for me to say!"
        self.engine.say(message)
        if self.print_speech == True:
            print(message)
        self.engine.runAndWait()

    #Message after succesfully executing a command
    def confirm_command_message(command):
        def wrapper(self, *args, **kwargs):
            if self.logs: self.logger.info(f"Function called: {command.__name__}")
            self.speak(self.confirmation_message)
            command(self, *args,**kwargs)
        async def async_wrapper(self, *args, **kwargs):
            if self.logs: self.logger.info(f"Async Function called: {command.__name__}")
            self.speak(self.confirmation_message)
            if (command.__name__[:3] == "LED" or command.__name__ == "engage_chillmode") and (not self.led_lights_handler.client or not self.led_lights_handler.client.is_connected):
                await self.led_lights_handler.connect()
            await command(self, *args,**kwargs)
        
        if asyncio.iscoroutinefunction(command):
            return async_wrapper
        else:
            return wrapper
    
    #Personalize speech generator
    def set_voice_settings(self,voice="female",rate=180,volume=1.0):
        if voice == 'male':
            self.engine.setProperty('voice',r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
        else:
            self.engine.setProperty('voice',r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
            voice = "female"
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        self.voice_settings['voice'] = voice
        self.voice_settings['rate'] = rate if rate >= 60 and rate <= 300 else  180
        self.voice_settings['volume'] = volume if volume >= 0 and volume <= 1 else 1.0
        if self.logs: self.logger.info(f"Set voice settings: voice={self.voice_settings['voice']}, rate={self.voice_settings['rate']}, volume={self.voice_settings['volume']}")
    
    #Voice to text with mic
    def transcribe_action(self, language="en"):
        #Turn on Mic
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.speak("Wassup boss. Whats the mission?")
            print("Listening...")

            # Capture the audio input
            audio = self.recognizer.listen(source, timeout=5)

            print("Recognizing...")

            try:
                # Use Google Speech Recognition to transcribe the audio
                query = self.recognizer.recognize_google(audio, language=language)
                print(f"Transcribed message: {query}")
                if self.logs: self.logger.info(f"Transcribed message: {query}")
                return query

            except sr.UnknownValueError:
                if self.logs: self.logger.warning(f"Praximedes could not understand what you said")
                self.speak("Sorry, I could not understand what you said.")
            except sr.RequestError as e:
                if self.logs: self.logger.error(f"There was an issue with the speech recognition service: {e}")
                self.speak(f"Sorry, there was an issue with the speech recognition service.")
                print(f"Details: {e}")
    
    #Chill Mode
    @confirm_command_message
    async def engage_chillmode(self):
        self.speak("Entering Chill Mode!")

        # Load chill mode settings
        with open(os.path.join(self.__config_dir,"custom.json")) as file:
            data = json.load(file)
        chill_mode = data["Chill_mode"]

        # Try to turn on LED Lights
        try:
            await self.led_lights_handler.ChillMode()
            self.speak("Turning on LED Lights!")
        except Exception as e:
            self.speak(f"Unable to connect with led lights: {e}")

        # Try Running Spotify
        try:
            self.spotify_controller.Play_ChillSong(track=chill_mode["Song"], artist=chill_mode["Artist"], playlist_uri=chill_mode["Playlist_uri"])
            self.speak("Playing Spotify")
        # If No device is found to be active
        except spotipy.SpotifyException as e:
            if self.logs: self.logger.error(f"Could not run spotify: {e}")
            print(e)
            self.speak("Cannot Play music on Spotify! No active device was found!")
        else:
            #Chill Mode successfull!
            self.speak("Be ready")
            self.engine.setProperty('rate',90)
            self.speak("<pitch middle='-10'>To</pitch>")
            self.engine.setProperty('rate',50)
            self.speak("<pitch middle='-20'>Reeelax...</pitch>")
            #Reset settings
            self.set_voice_settings(self.voice_settings['voice'],
                                    self.voice_settings['rate'],
                                    self.voice_settings['volume'])
            if self.logs: self.logger.info("Engaged on chill mode")

    #LED Lights-----
    #LED turn on
    @confirm_command_message
    async def LED_turnOn(self):
        try:
            await self.led_lights_handler.change_power(state="ON")
            self.speak("Turning on LED Lights!")
        except Exception as e:
            print(e)
            self.speak("Unable to connect with LED lights")
    
    #LED turn off
    @confirm_command_message
    async def LED_turnOff(self):
        try:
            await self.led_lights_handler.change_power(state="OFF")
            self.speak("Turning off LED Lights!")
        except Exception as e:
            print(e)
            self.speak("Unable to connect with LED lights")
    
    #LED change color of lights
    @confirm_command_message
    async def LED_changeColor(self,color_string = None):
        try:
            # Set to lower case
            if color_string: color_string = color_string.lower()

            # Get colors from json file in config
            with open(os.path.join(self.__config_dir,'colors.json'), "r") as json_file:
                colors = json.load(json_file)

            # Select random color in saved json file
            if color_string == 'random' or color_string == None:
                self.speak("Picking a color at random...")
                color_names = list(colors.keys())
                color_string = random.choice(color_names)
                R,G,B = colors[color_string]

            # Find color string in json file
            else:
                # If color exist in json file
                if color_string in colors:
                    R,G,B = colors[color_string]
                # If color does not exist in json file
                else:
                    if self.logs: self.logger.error(f"Unknown color string: {color_string}")
                    raise ValueError(f"Unknown color string: {color_string}")
                
            # Send command to change color
            await self.led_lights_handler.change_color(R,G,B)

            # Log message
            if self.logs: self.logger.info(f"Changing color of LED lights to {color_string}")
            # Speak the message
            self.speak(f"Changing color of LED lights to {color_string}")
        
        #Error handling
        except ConnectionError as conn_e:
            self.speak(f"Sorry, I was not able to connect with the LED lights device.")
            self.logger.error(f"Failed to connect to device: {conn_e}")
        except Exception as e:
            self.speak(f"Sorry, I Failed to change the color of LED lights: {e}")
            self.logger.error(f"Failed to change color of LED: {e}")
    #---------------
    #Fix functionality in ML at main.py main to get colors that are more than 1 word long