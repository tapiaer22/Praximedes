import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os, time, json, logging


class Spotify_Controller:
    def __init__(self, SPOTIFY_CLIENT_ID,
                 SPOTIFY_CLIENT_SECRET,
                 SPOTIFY_REDIRECT_URI=None,
                 SPOTIFY_SCOPE=None,
                 logs=True):
        #For directory use
        self.__current_dir = os.path.dirname(__file__)                      #Used to access config files
        self.__config_dir = os.path.join(self.__current_dir,'..','config')  #Used for config files

        #If the user want default options
        if SPOTIFY_REDIRECT_URI == None: SPOTIFY_REDIRECT_URI="http://localhost:3000"
        if SPOTIFY_SCOPE == None: SPOTIFY_SCOPE="streaming,user-read-playback-state,user-modify-playback-state"
        
        #Assign values
        self.SPOTIFY_CLIENT_ID = SPOTIFY_CLIENT_ID
        self.SPOTIFY_CLIENT_SECRET = SPOTIFY_CLIENT_SECRET
        self.SPOTIFY_REDIRECT_URI = SPOTIFY_REDIRECT_URI
        self.SPOTIFY_SCOPE = SPOTIFY_SCOPE

        #Authenticate
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIFY_CLIENT_ID,
                                                            client_secret=self.SPOTIFY_CLIENT_SECRET,
                                                            redirect_uri=self.SPOTIFY_REDIRECT_URI,
                                                            scope=self.SPOTIFY_SCOPE))
        
        #Log status of spotify controller
        self.logs = logs
        if self.logs:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.info(f"{self.__class__.__name__} initialized")
    
    #Methods that return data
    def get_playlists(self):
        # Get user playlists
        result = []
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            result.append(playlist['name'])
        # Log playlists
        if self.logs: self.logger.info(f"Obtained spotify playlists: {result}")
        return result
