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
        
    
    def user_auth(self, user=None):
        '''
        This method will create the client credentials to query users for their tokens
        
        Input: 
            - user: The Spotify username as a string
            - scope: Is the authentication requirement necessitated by the program to proceed
            
        Output:
            - Top Tracks Sesh:
            - User: The string of characters that is the user so we can store it in the DB
            - Top Track IDs: List of strings of the top 50 tracks for a user
        '''
        client_secret = self.client_secret
        scope = self.user_top_scope
        client_id = self.client_id
        uri = self.uri
        user = user.lstrip('spotify:user:')
        
        # OAuth Credentials
        spot_cc = spotipy.oauth2.SpotifyOAuth(username=user,
                                              client_id=cilent_id,
                                              client_secret=client_secret,
                                              scope=scope,
                                              redirect_uri=uri)
        
        # Token access for given user, given scope
        top_trx_accs_token = spot_cc.get_access_token(as_dict=True)
        
        # Starts session with current user
        top_trx_session = spotipy.Spotify(auth=top_trx_accs_token)
        
        # Generates a list of all the song IDs in a user's library
        top_trx = top_trx_session.current_user_top_tracks(limit=50, time_range='medium_range')
        top_50_trx_ids = [top_tracks['items'][x]['id'] for x in range(len(top_tracks['items']))]
        
        return {
            'Top Tracks Sesh': top_trx_session,
            'User': user,
            'Top Track IDs': top_50_trx_ids
        }
        
        def playlist_generator(self, user1=None, user2=None):
            '''
            This method generates a playlist from two users that have provided access to the system
            
            Input:
                - user1/2:  User names should be a string of characters, if one of the two users is not provided
                            If a user does not provide app token access, spotify will also be used to generate recommendations
            Output:
                - URI: A spotify link to the generated playlist given the two users.
            '''
            if user1 == None and user2 == None:
                raise Exception('You need to provide at least one Username')
            elif user1 != None and user2 != None:
                # Here is where we need to query the DB to see if the user exists
                
                
                
                
                
                
#         def auth_user_lib_read(self, user=None, scope=None):
#         '''
#         This method will gather all of the music in the library of a single user.
        
#         Input: 
#             - user: The Spotify username as a string
#             - scope: Is the authentication requirement necessitated by the program to proceed
            
#         Output:
#             - not sure yet
#         '''
#         # Generates a token for the given user with the 'user-lib-read' scope
#         token = util.prompt_for_user_token(username=user,
#                                            client_id=client_id,
#                                            client_secret=client_secret,
#                                            scope=scope,
#                                            rediret_uri=uri)


#         def aut_user_playlist_read(self, user=None, scope=None):
#             '''
#             This method reads through the user's playlists and obtains all of the tracks
            
#             Input:
#                 - user: The Spotify username as a string of alphanumeric values
#                 - scope: Is the authentication requirement necessitated byt the program to proceed
            
#             Output:
#                 - JSON: Containing song audio features for a series of songs for a given user
#             '''
            
            
            
            
            
            
#             '''Note, you can use recommendations feature to provide the best possible reccomendations for users, include the target value using both of the  users total top favorite tracks averages'''
