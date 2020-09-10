# imports

import sys
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

    spot_creds = None     # Gathers credentials for song data
    spot_session = None   # Starts a spotify session
    user_token = None     # Requests a token for a given user
    accs_token = None     # Uses cred access token (also to refresh tokens)
    refresh_token = None  # Obtained from accs_token from client creds

    def __init__(self):

        load_dotenv()

        self.client_secret = getenv('SPOTIFY_CLIENT_SECRET')
        self.client_id = getenv('SPOTIFY_CLIENT_ID')
        # redirects to app site
        self.uri = getenv('uri')
        # Creates/adds playlist; Gets saved tracks; top saved tracks/artists
        self.scope = 'playlist-modify-public user-library-read user-top-read'
        self.user = None
        self.cache_path = ('../.user_cache')

    def user_top_50(self, user):
        '''
        This method will create the client credentials to query users for their
        tokens.

        Input:
            - user: The Spotify username as a string
            - scope: Is the authentication requirement necessitated by the
                     program to proceed

        Output:
            - Top Tracks Sesh:
            - User: The string of characters that is the user so we can store
                    it in the DB
            - Top Track IDs: List of strings of the top 50 tracks for a user
        '''
        client_secret = self.client_secret
        cache_path = self.cache_path
        client_id = self.client_id
        scope = self.scope
        uri = self.uri
        user = user

        # OAuth Credentials; only used when token is cached
        spot_cc = spotipy.oauth2.SpotifyOAuth(username=user,
                                              client_id=client_id,
                                              client_secret=client_secret,
                                              cache_path=cache_path,
                                              scope=scope,
                                              redirect_uri=uri)
        # accs_token = spot_cc.get_access_token()

        # Testing the util.prompt_for_user_token() method
        top_trx_accs_token = util.prompt_for_user_token(
                                            username=user,
                                            # username='agustinvargas',
                                            # username='gabriela_ayala19',
                                            # username='dintherye',
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            cache_path=cache_path,
                                            scope=scope,
                                            redirect_uri=uri)

        spot_session = spotipy.Spotify(auth=top_trx_accs_token)

        # Token access for given user, given scope
        token_info = spot_cc.get_access_token(as_dict=True)

        # Starts session with current user
        # top_trx_session = spotipy.Spotify(auth=top_trx_accs_token)

        # Generates a list of all the song IDs in a user's library
        top_trx = spot_session.current_user_top_tracks(
                                                limit=50,
                                                time_range='medium_term'
                                                )
        top_50_trx_ids = [top_trx['items'][x]['id'] for x in range(
                                                len(
                                                    top_trx['items']
                                                    )
                                                )
                          ]

        return {
            'Top Tracks tokens': 'token_info',
            'User': {user},
            'Top Track IDs': top_50_trx_ids
        }

    def playlist_generator(self, user1=None, user2=None):
        '''
        This method generates a playlist from two users that have provided
        access to the system

        Note: You can use recommendations feature to provide the best
        possible reccomendations for users, include the target value using
        both of the  users total top favorite tracks averages

        Input:
            - user1/2:
                User names should be a string of characters, if one of the two
                users is not provided
                If a user does not provide app token access, spotify will also
                be used to generate recommendations
        Output:
            - URI: A spotify link to the generated playlist given the two users
        '''
        # if user1 is None and user2 is None:
        #     raise Exception('You need to provide at least one Username')
        # elif user1 is not None and user2 is not None:
