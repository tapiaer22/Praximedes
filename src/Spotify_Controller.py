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
    
    def get_connected_devices(self) -> list:
        # Log message
        if self.logs: self.logger.info("Getting connected devices")
        # Get active devices using spotify
        devices = self.sp.devices()
        return devices.get("devices")
    
    def get_saved_devices(self) -> dict:
        # Log message
        if self.logs: self.logger.info("Obtained saved deviced")
        # Get saved devices from config directory
        with open(f"{self.__config_dir}/devices.json", "r") as json_file:
            saved_devices = json.load(json_file)
        return saved_devices["Spotify_devices"]

    def get_current_user_profile(self):
        # Log message
        if self.logs: self.logger.info("Getting current user info")
        # Get user info as dict
        return self.sp.current_user()
    
    #Methods that perform actions
    def Play_on_thisPC(self) -> None:
        # Log message
        if self.logs: self.logger.info("Opening spotify on this PC")
        # Start spotify in this PC
        os.system("start spotify")
        time.sleep(3)
        os.system("spotify next")
        os.system("spotify pause")

    def get_active_device(self):
        # Check for connected devices
        devices = self.get_connected_devices()
        n_devices = len(devices)
        device_id = None

        # Loop through devices to find an active one
        for i in range(n_devices):
            if devices[i]["is_active"] == True:
                device_id = devices[i]['id']
        
        # Log message
        if self.logs: self.logger.info(f"Active device in spotify: {device_id}")
        print(f"Active device in spotify: {device_id}")

        #Return active device id, or None if no active device exist
        return device_id
    
    def Play_ChillSong(self, artist: str="Santa Fe", track: str="Tu y Yo", playlist_uri = None):
        #Define a song query for song
        song_query=""
        if artist: song_query+="artist:" + artist + " "
        if track:  song_query+="track:" + track
        
        #Check for active devices 
        device_id = self.get_active_device()
        # If no active device, set this PC as active
        if device_id == None:
            # Log message
            if self.logs: self.logger.info("No active device found! Playing spotify in this device")
            print(f"No active device found! Playing spotify in this device")
            # Set this PC as active
            self.Play_on_thisPC()
            saved_devices = self.get_saved_devices()
            first_key = list(saved_devices.keys())[0]
            device_id=saved_devices[first_key]

        #Search for a song and save URI
        results = self.sp.search(q=song_query, limit=1, type='track')
        track_uri = results['tracks']['items'][0]['uri']
        # Log message
        if self.logs: 
            self.logger.info(f"Playing: {track} by {artist} {f"in playlist {playlist_uri}" if playlist_uri else ""} on device {device_id}")
            print(f"Playing: {track} by {artist} {f"in playlist {playlist_uri}" if playlist_uri else ""} on device {device_id}")
        #Start playback
        if playlist_uri: self.sp.start_playback(device_id=device_id, context_uri=playlist_uri,offset={"uri": track_uri})
        else: self.sp.start_playback(device_id=device_id, uris=[track_uri])
