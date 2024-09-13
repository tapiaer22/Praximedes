#For async functionalities
import asyncio, os
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
        pass
