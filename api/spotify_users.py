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

    def get_user_top_trx(self, token_info: str, user_id: str):
        """Fetches user top track IDs from SpotifyAPI.
        
        Makes calls to the SpotifyAPI to gather a given user's top tracks
        from the last 7 days (short term), 6 months (medium term), and all
        time (long term).

        Args:
            token_info: JSON object containing access and refresh token information
              for the user
            user_id: Spotify ID as a string object

        Returns:
            A dict of key/value pairs contianing objects utilized in the following methods
            
            spot_cc: Spotify authentication object which will by used in other methods
            session: DataBase session object that is can be used for other methods
              running asyncronously
            spot_session: Spotify API client that is used to obtain user and track data
            user_id: Integer value for the database ID
            terms: Terms are broken down into three key/val pairs containing lists of strings
              for short term, medium term, and long term
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
                                        User.spot_id ==
                                        user_id
                                        ).first()

        spot_cc = spotipy.oauth2.SpotifyOAuth(
                                        username=user_id_q.display_name,
                                        client_id=client_id,
                                        client_secret=client_secret,
                                        cache_path=cache_path,
                                        scope=scope,
                                        redirect_uri=redirect_uri,
                                        )

        token_info = spot_cc.refresh_access_token(token_info['refresh_token'])

        # update token in DB
        token = Tokens()
        user_token_q = session.query(Tokens).filter(Tokens.user==user_id_q.id).first()
        user_token_q.access_token = token_info['access_token']
        session.commit()

        spot_session = spotipy.Spotify(auth=token_info['access_token'])
        
        terms = ['short_term', 'medium_term', 'long_term']
        trk_ids_lst = []

        for term in terms:
            top_trx = spot_session.current_user_top_tracks(
                                                limit=50,
                                                time_range=term
                                                )
            globals()[term + '_trx'] = [top_trx[
                                            'items'
                                                ][x][
                                                    'id'
                                                        ] for x in range(
                                                                        len(
                                                                            top_trx[
                                                                                'items'
                                                                                ]))]
            if len(globals()[term + '_trx']) != 0:
                trk_ids_lst.append(globals()[term + '_trx'])
            else:
                continue

        return {
                "spot_cc": spot_cc,
                "session": session,
                "spot_session": spot_session,
                "user_id": user_id_q.id,
                "short_term_trx": short_term_trx,
                "medium_term_trx": medium_term_trx,
                "long_term_trx": long_term_trx
                }

    def add_tracks(self, trx_ids, aud_feat, session):
        """Adds track audio feature information to DB.

        Args:
            top_50_trx_ids: List of 50 alpha-neumeric track IDs
            top_50_aud_feat: List of dicts containing feat data
            session: DB connection object

        Returns:
            Updates DB with the track id and track feature data
            session: object
        """
        aud_feat = aud_feat
        trx_ids = trx_ids
        session = session

        trx = []
        for k, v in enumerate(aud_feat):
            trk_sesh = session.query(
                                    Tracks
                                    ).filter(
                                            Tracks.spot_id == trx_ids[k]
                                            ).first()
            if trk_sesh is not None:
                continue
            globals()['trk_' + str(k)] = Tracks(
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
                                        time_signature=v['time_signature'],
                                        spot_id=trx_ids[k]
                                        )
            trx.append(globals()['trk_' + str(k)])

        session.add_all(trx)
        session.commit()

        return session

    def add_playlist(self, paylist_uri, session, user_id):
        """
        Adds newly created playlist to DB with current user.

        Args:
            playlist_uri: string of characters in the following form:
                'spotify:playlist:2Pk3OLPiVXIZHieWs5ZGHp'
            session: DB object session
            user_id: integer

        Returns:
            Updates playlist DB
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

    def get_playlists_trx(self, spot_session, user_id):
        """
        Gets all user playlists tracks

        Args:
            spot_session: Object from get_user_top_trs()
            user_id: String from get_user_top_trs() dict

        Returns:
             
        """
        spot_session = spot_session
        user_id = user_id

        playlists = spot_session.user_playlists(user_id)


        if len(playlists['items']) == 0:
            raise Exception('user has no playlists')

        playlist_ids = []
        for i in range(len(playlists['items'])):
            playlist_ids.append(playlists['items'][i]['id'])

        all_tracks_ids = []
        for playlist_id in playlist_ids:
            playlist_trx = spot_session.playlist_tracks(
                                                    playlist_id,
                                                    offset=1,
                                                    fields='items.track.id'
                                                    )
            for trx in playlist_trx['items']:
                if trx['track'] is None:
                    continue
                all_tracks_ids.append(trx['track']['id'])

        return {
                "all_tracks_ids": all_tracks_ids,
                }
    

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

        Args:
            user1_top_aud_feat: Top 50 track audio features (dict)
            user2_top_aud_feat: Top 50 track audio features (dict)

        Returns:
            uri: playlist containing a number of random tracks based on the
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
