# imports
import sys
import json
from os import getenv

import spotipy
import numpy as np
import pandas as pd
import spotipy.util as util
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from json.decoder import JSONDecodeError
from sqlalchemy.ext.declarative import declarative_base
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

        # Spot Creds/Auth
        self.client_secret = getenv('SPOTIFY_CLIENT_SECRET')
        self.client_id = getenv('SPOTIFY_CLIENT_ID')

        # redirects to app site
        self.uri = getenv('uri')

        # Creates/adds playlist; Gets saved tracks; top saved tracks/artists
        # and stores user cache in the specified path
        self.scope = 'playlist-modify-public user-library-read user-top-read'
        self.user = None
        self.cache_path = ('../.user_cache')

        # Connects to DB
        self.engine = create_engine(getenv('DATABASE_URL'))
        self.Session = sessionmaker(
                            autocommit=False,
                            autoflush=False,
                            bind=self.engine
                            )
        self.base = declarative_base()

    def add_tracks(self, top_50_trx_ids, top_50_aud_feat):
        """
        This function is used when the user does not have their top 50 trx in
        our db, and we need to add them after adding the user.

        Adds tracks to db if the user is not in DB.

        Input:
            - top_50_trx_ids: List of 50 alpha-neumeric track IDs
            - top_50_aud_feat: List of dicts containing feat data

        Output:
            - Updates DB with the track id and track feature data
        """
        session = Session()
        top_50_trx_ids = top_50_trx_ids
        top_50_aud_feat = top_50_aud_feat

        trx = []
        for k, v in enumerate(top_50_aud_feat):
            trk_sesh = session.query(
                                    Tracks
                                    ).filter(
                                            Tracks.id == top_50_trx_ids[k]
                                            ).first()
            if trk_sesh is not None:
                continue
            globals()['trk_' + str(k)] = Tracks(
                                        id=top_50_trx_ids[k],
                                        danceability=v['danceability'],
                                        energy=v['energy'],
                                        key=v['key'],
                                        loudness=v['loudness'],
                                        mode=v['mode'],
                                        speechiness=v['speechiness'],
                                        acousticness=v['acousticness'],
                                        instrumentalness=v['instrumentalness'],
                                        valence=v['valence'],
                                        liveness=v['liveness'],
                                        tempo=v['tempo'],
                                        duration_ms=v['duration_ms'],
                                        time_signature=v['time_signature']
                                        )
            trx.append(globals()['trk_' + str(k)])

        session.add_all(trx)
        session.commit()

        return session

    def check_for_user(self, user_id, session):
        """
        Checks for user in DB.

        Input:
            - User_ID: alpha neumeric values

        Output:
            - q: User() object from the my_db module
                 contains q.id (user id) and q.display_name (user display name)
        """
        session = session
        engine = self.engine
        Base = self.base
        user_id = user_id

        q = session.query(User).filter(User.id == user_id).first()

        if q is None:
            session.add(user)
            session.commit()

        return q

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
