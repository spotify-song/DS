# imports
import sys
import json
import random
from os import getenv

import spotipy
import psycopg2
import numpy as np
import pandas as pd
import spotipy.util as util
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from json.decoder import JSONDecodeError
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# use in production
# import api.models.my_db
# from api.models.my_db import *

# use in jupyter
import models.my_db
from models.my_db import *


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
        self.user_id = getenv('USER_ID')

        # change for deplpoyment
        self.uri = getenv('uri')

        # Scopes: User top track; creates playlist
        self.scope = 'playlist-modify-public user-library-read user-top-read'
        self.cache_path = '../.user_cache'

        # Connects to DB
        self.engine = create_engine(getenv('DATABASE_URL'))
        self.Session = sessionmaker(
                                autocommit=False,
                                autoflush=False,
                                bind=self.engine
                                )
        self.base = declarative_base()

    def get_user_top_trx(self, token_info, user_id):
        """
        Checks for user in DB.

        Input:
            - current_user_info: This object contains ID and displa_name for
              the user
            - spot_cc: Object for the spotify credentials connection

        Output:
            - session: DB Session
            - user1: User object
            - token_info: not sure this is entrirely necessary yet
        """
        client_secret = self.client_secret
        cache_path = self.cache_path
        client_id = self.client_id
        user_id = user_id
        session = self.Session()
        redirect_uri = self.uri
        engine = self.engine
        scope = self.scope
        Base = self.base

        user = User()
        user_id_q = session.query(
                                User
                                ).filter(
                                        User.id ==
                                        user_id
                                        ).first()

        spot_cc = spotipy.oauth2.SpotifyOAuth(
                                        username=user_id_q.display_name,
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        cache_path=cache_path,
                                        scope=scope,
                                        redirect_uri=redirect_uri,
                                        show_dialog=True
                                        )

        expired_token = spot_cc.is_token_expired(token_info)

        if expired_token:
            token = Tokens()
            user_token_q = session.query(Tokens).filter(Tokens.user==user_id_query.id).first()
            token_refresh = spot_cc.refresh_access_token(auth=token_info['refresh_token'])
            user_token_q.access_token = token_refresh['access_token']
            session.commit()
        else:
            spot_session = spotipy.Spotify(auth=token_info['access_token'])

        # 6 month term
        top_trx = spot_session.current_user_top_tracks(
                                                limit=50,
                                                time_range='medium_term'
                                                )
        top_50_trx_ids = [top_trx[
                            'items'
                                ][x][
                                    'id'
                                        ] for x in range(
                                                        len(
                                                            top_trx[
                                                                'items'
                                                                ]
                                                            )
                                                        )
                          ]
        # Track audio features for one tracks
        top_50_aud_feat = spot_session.audio_features(
                                                    tracks=top_50_trx_ids
                                                    )

        return {
                "spot_cc": spot_cc,
                "session": session,
                "spot_session": spot_session,
                "user_id": user.id,
                "top_50_trx_ids": top_50_trx_ids,
                "top_50_aud_feat": top_50_aud_feat
                }

    def add_tracks(self, top_50_trx_ids, top_50_aud_feat, session):
        """
        This function is used when the user does not have their top 50 trx in
        our db, and we need to add them after adding the user.

        Input:
            - top_50_trx_ids: List of 50 alpha-neumeric track IDs
            - top_50_aud_feat: List of dicts containing feat data

        Output:
            - Updates DB with the track id and track feature data
            - DB session: object
        """
        top_50_aud_feat = top_50_aud_feat
        top_50_trx_ids = top_50_trx_ids
        session = session

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

    def add_playlist(self, paylist_uri, session, user_id):
        """
        Adds newly created playlist to DB with current user.

        Input:
            - Plalist URI: string of characters in the following form:
                'spotify:playlist:2Pk3OLPiVXIZHieWs5ZGHp'

        Output:
            - Updates playlist DB
        """
        user_id = user_id
        session = session
        playlist_uri = playlist_uri

        playlist = UserPlaylist(
                            uesr_id=user_id,
                            user=playlist_uri,
                            tracks_id=None
                            )
        session.add(playlist)
        session.commit()

        return None

    def get_playlists_trx(self, spot_session, user2):
        """
        Gets user 2 playlists and tracks
        """
        spot_session = spot_session
        user2 = user2

        playlists = spot_session.user_playlists(user2)

        if len(playlists['items']) < 10:
            playlist_ids = []
            for playlist_item in playlists['items']:
                playlist_ids.append(playlist_item['id'])

            all_tracks_ids = []
            for playlist_id in playlist_ids:
                playlist_trx = spot_session.playlist_tracks(
                                                        playlist_id,
                                                        offset=1,
                                                        fields='items.track.id'
                                                        )
                for trx in playlist_trx['items']:
                    all_tracks_ids.append(trx['track']['id'])
        else:
            playlist_ids = []
            for i in range(10):
                playlist_ids.append(playlists['items'][i]['id'])

            all_tracks_ids = []
            for playlist_id in playlist_ids:
                playlist_trx = spot_session.playlist_tracks(
                                                        playlist_id,
                                                        offset=1,
                                                        fields='items.track.id'
                                                        )
                for trx in playlist_trx['items']:
                    all_tracks_ids.append(trx['track']['id'])

        user2_top_50_aud_feat = spot_session.audio_features(
                                                    tracks=random.sample(
                                                                all_tracks_ids,
                                                                50
                                                                )
                                                        )

        return user2_top_50_aud_feat


class CheckForUser:
    spot_creds = None     # Gathers credentials for song data
    spot_session = None   # Starts a spotify session
    user_token = None     # token for a given user
    accs_token = None     # Uses cred access token (also to refresh tokens)
    refresh_token = None  # Obtained from accs_token from client creds

    def __init__(self):

        load_dotenv()

        # Spot Creds/Auth
        self.client_secret = getenv('SPOTIFY_CLIENT_SECRET')
        self.client_id = getenv('SPOTIFY_CLIENT_ID')
        self.user_id = getenv('USER_ID')

        # change for deplpoyment
        self.uri = getenv('uri')

        # Scopes: User top track; creates playlist; reads full library
        self.scope = 'playlist-modify-public user-library-read user-top-read'
        self.cache_path = '../.user_cache'

        # Connects to DB
        self.engine = create_engine(getenv('DATABASE_URL'))
        self.Session = sessionmaker(
                                autocommit=False,
                                autoflush=False,
                                bind=self.engine
                                )
        self.base = declarative_base()

    def check_user(self, refresh_token):
        """
        Checks to see if user exists in DB

        Input:
            - Refresh_token: String of alphanumeric values
            - Access_token: String of alphanumeric values
        Returns:
            - True: Bool, if user exists and token is usuable
            - False: Bool, else
            
        """



class CreatePlaylist:
    def __init__(self):
        load_dotenv()

        # Spot Creds/Auth
        self.client_secret = getenv('SPOTIFY_CLIENT_SECRET')
        self.client_id = getenv('SPOTIFY_CLIENT_ID')

        # change for deplpoyment
        self.uri = getenv('uri')

        # Scopes: User top track; creates playlist
        self.scope = 'playlist-modify-public user-library-read user-top-read'
        self.user = None
        self.cache_path = ('../.user_cache')

    def create_playlist(self,
                        user1_top_aud_feat,
                        user2_top_aud_feat,
                        spot_session,
                        user_info,
                        user2=None
                        ):
        """
        This function will take the top 50 tracks for 2 users and generate a
        playlist (uri) for the users to share.

        Input:
            - user1_top_aud_feat: Top 50 track audio features (dict)
            - user2_top_aud_feat: Top 50 track audio features (dict)

        Output:
            - uri: playlist containing a number of random tracks based on the
                   two user's playlists and libraries.
        """
        user1_top_aud_feat = user1_top_aud_feat
        user2_top_aud_feat = user2_top_aud_feat
        user_info = user_info
        user2 = user2
        spot_session = spot_session

        if user2 is not None:
            playlist_name = f"Mine and {user2}'s music child"
        else:
            playlist_name = f"{user_info['display_name']}'s lonely\
                            playlist"

        user1_df = pd.DataFrame(user1_top_aud_feat)
        user2_df = pd.DataFrame(user2_top_aud_feat)
        users_top_trx = pd.concat([user1_df, user2_df])
        users_top_trx = users_top_trx.drop_duplicates(
                                                    inplace=False,
                                                    subset='id'
                                                    )
        users_top_trx_id = random.sample(list(users_top_trx['id']), 5)
        recs = spot_session.recommendations(
                                    seed_tracks=users_top_trx_id,
                                    limit=50,
                                    target_danceability=users_top_trx[
                                                                'danceability'
                                                                ].mean(),
                                    target_energy=users_top_trx[
                                                                'energy'
                                                                ].mean(),
                                    target_loudness=users_top_trx[
                                                                'loudness'
                                                                ].mean(),
                                    target_speechiness=users_top_trx[
                                                                'speechiness'
                                                                ].mean(),
                                    target_acousticness=users_top_trx[
                                                                'acousticness'
                                                                ].mean(),
                                    target_valence=users_top_trx[
                                                                'valence'
                                                                ].mean(),
                                    target_liveness=users_top_trx[
                                                                'liveness'
                                                                ].mean(),
                                    target_tempo=users_top_trx[
                                                                'tempo'
                                                                ].mean()
                                    )
        tracks = []
        for _ in recs['tracks']:
            tracks.append(_['id'])

        playlist = spot_session.user_playlist_create(
                                                    user=user_info[
                                                                    'id'
                                                                    ],
                                                    name=playlist_name,
                                                    public=True
                                                )
        spot_session.user_playlist_add_tracks(
                                            user=user_info['id'],
                                            playlist_id=playlist['id'],
                                            tracks=tracks
                                            )

        return {
            "URI": playlist['uri'],
            "user": playlist['owner']['id']
        }
