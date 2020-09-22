# imports
import sys
import json
from os import getenv

import spotipy
# import webbrowser
import numpy as np
import pandas as pd
import spotipy.util as util
from dotenv import load_dotenv
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

import models.my_db
from models.my_db import User, Tokens, Tracks, UserPlaylist


class UserData:

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

    def check_for_user(self, user_id):
        """
        Checks for user in DB.

        Input:
            - User_ID: alpha neumeric values

        Output:
            - True: if user exists in DB
            - False: False if user does not exist in DB
        """
        user_id = user_id
        q = session.query(User).filter(User.id == user_id).fisrts()
        

    def user_top_50(self, user_id):
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
        user_id = user_id
        # disp_name_update = UpdateTables()

        # OAuth Credentials; only used when token is cached
        spot_cc = spotipy.oauth2.SpotifyOAuth(username=user_id,
                                              client_id=client_id,
                                              client_secret=client_secret,
                                              cache_path=cache_path,
                                              scope=scope,
                                              redirect_uri=uri)
        # accs_token = spot_cc.get_access_token()

        # Testing the util.prompt_for_user_token() method
        top_trx_accs_token = util.prompt_for_user_token(
                                            username=user_id,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            cache_path=cache_path,
                                            scope=scope,
                                            redirect_uri=uri)

        spot_session = spotipy.Spotify(auth=top_trx_accs_token)
        current_user_info = spot_session.current_user()

        # If display_name and userID != user_id return error
        if (current_user_info['display_name'] != user_id) and\
           (current_user_info['id'] != user_id):
            raise Exception('Must enter valid user ID or Display name')

        # Token access for given user, given scope
        token_info = spot_cc.get_access_token(as_dict=True)

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

        # Track audio features for one tracks
        top_50_aud_feat = spot_session.audio_features(tracks=top_50_trx_ids)

        # Updates users/tokens tables
        # disp_name_update.update_users_info(
        #                         display_name=current_user_info['display_name'],
        #                         token_info=token_info,
        #                         id=current_user_info['id']
        #                         )

        return {
            'Display Name': current_user_info['display_name'],
            'Tokens Info': token_info,
            'User ID': current_user_info['id'],
            'Top Track IDs': top_50_trx_ids,
            'Track Audio Features': top_50_aud_feat
        }
