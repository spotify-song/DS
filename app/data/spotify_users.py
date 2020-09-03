# imports

# import sys 
import json
import spotipy
# import webbrowser
import numpy as np
import pandas as pd
from os import getenv
import spotipy.util as util
from dotenv import load_dotenv
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth



class User:

#     lib_read_scope = 'user-library-read'           # Gets user's saved tracks
#     user_top_scope = 'user-top-read'               # Gets user's top saved tracks/artists
#     pub_playlist_scope = 'playlist-modify-public'  # Creates playlist, adds items to playlist
    
    spot_creds = None     # Gathers credentials for song data
    spot_session = None   # Starts a spotify session
    user_token = None     # Requests a token for a given user
    accs_token = None     # Uses credentials access token (can be used for refresh tokens)
    refresh_token = None  # Refresh token obtained from accs_token from client creds
    
    
    def __init__(self):
        
        load_dotenv()
        
        self.client_secret = getenv('SPOTIFY_CLIENT_SECRET')
        self.client_id = getenv('SPOTIFY_CLIENT_ID')
        self.uri = getenv('uri')                             # URI should redirect to app site
        self.pub_playlist_scope = 'playlist-modify-public'   # Creates playlist, adds items to playlist
        self.lib_read_scope = 'user-library-read'            # Gets user's saved tracks
        self.user_top_scope = 'user-top-read'                # Gets user's top saved tracks/artists
        self.user = None
        
    
    def auth_user_lib_read(self, user=None, scope=None):
        '''
        This function will gather all of the music in the library of a single user.
        
        Input: 
            - user: The Spotify username as a string
            - scope: Is the authentication requirement necessitated by the program to proceed
        '''
        client_secret = self.client_secret
        scope = self.lib_read_scope
        client_id = self.client_id
        uri = self.uri
        user = user
        
        token = util.prompt_for_user_token(
            username=user,
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            rediret_uri=uri
        )
        
        spot_session = spotipy.Spotify(
            auth=token
        )
        
        