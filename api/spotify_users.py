"""Module contains class and methods for user analysis, DB updates."""

# imports
import random
from os import getenv

import spotipy
# import psycopg2
# import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
# from json.decoder import JSONDecodeError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
# from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# use in production
# import api.models.my_db
from api.models.my_db import User, Tokens, Tracks, UserPlaylist

# use in jupyter
# import models.my_db
# from models.my_db import *


class UserData:
    """I am so tired, and need a job."""

    spot_creds = None     # Gathers credentials for song data
    spot_session = None   # Starts a spotify session
    user_token = None     # Requests a token for a given user
    accs_token = None     # Uses cred access token (also to refresh tokens)
    refresh_token = None  # Obtained from accs_token from client creds

    def __init__(self):
        """Initiate class vars."""
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
        """Fetch user top track IDs from SpotifyAPI.

        Makes calls to the SpotifyAPI to gather a given user's top tracks
        from the last 7 days: short term, 6 months: medium term, and all
        time: long term.

        Args:
            token_info: JSON object containing access and refresh token
            information for the user
            user_id: Spotify ID as a string object

        Returns:
            A dict of key/value pairs contianing objects utilized in the
            following methods
            spot_cc: Spotify authentication object which will by used in
            other methods
            session: DataBase session object that is can be used for other
            methods running asyncronously
            spot_session: Spotify API client that is used to obtain user
            and track data
            user_id: Integer value for the database ID
            terms: Terms are broken down into three key/val pairs
            containing lists of strings for short term, medium term, and
            long term
        """
        client_secret = self.client_secret
        cache_path = self.cache_path
        client_id = self.client_id
        user_id = user_id
        session = self.Session()
        redirect_uri = self.uri
        # engine = self.engine
        scope = self.scope
        # Base = self.base

        # user = User()
        user_id_q = session.query(
                                User
                                ).filter(
                                        User.spot_id == user_id
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
        # token = Tokens()
        user_token_q = session.query(
                                    Tokens
                                    ).filter(
                                            Tokens.user == user_id_q.id
                                            ).first()
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
                "long_term_trx": long_term_trx,
                "track_ids": trk_ids_lst
                }

    def user_song_library(self, spot_session):
        """Gathers all the saved tracks for a given user.

        Args:
            spot_session: Spotify object which will by used in other methods

        Returns:
            saved_tracks: List of all the saved tracks for a given user
        """
        lst = []
        offset = 0
        result = spot_session.current_user_saved_tracks(offset=offset)
        while result['next'] is not None:
            result = spot_session.current_user_saved_tracks(offset=offset)
            lst.append(result['items'])
            offset += 20

        trk_ids_lst = []
        for val in lst:
            for trk in val:
                trk_ids_lst.append(trk['track']['id'])

        return trk_ids_lst

    def get_audio_features(self, track_ids, spot_session):
        """Obtain song characteristics from the SpotifyAPI.

        The function takes in a list of song IDs as string values, and
        obtains audio features for individual songs.

        Args:
            track_ids: list of strings
            spot_session: Spotify object which will by used in other methods

        Returns:
            audio_features: Dictionary containing a list of audio features for
            each song ID provided
        """
        offset = 50
        onset = 0

        audio_feats = []
        while offset:
            if offset >= len(track_ids):
                audio_feats.append(spot_session.audio_features(
                                                    tracks=track_ids[onset:]
                                                    ))
                break
            audio_feats.append(spot_session.audio_features(
                                            tracks=track_ids[onset:offset]
                                            ))
            onset += 50
            offset += 50

        audio_features_lst = []
        for audio_feat in audio_feats:
            for feature in audio_feat:
                audio_features_lst.append(feature)

        return audio_features_lst

    def add_track_aud_feat(self, aud_feat, session):
        """Add track audio feature information to DB.

        Args:
            aud_feat: list of dictionary key value pairs containing audio
            features for given tracks
            session: DB connection object

        Returns:
            Updates DB with the track id and track feature data
            session: object
        """
        trx = []
        for k, v in enumerate(aud_feat):
            trk_sesh = session.query(
                                    Tracks
                                    ).filter(
                                            Tracks.spot_id == v['id']
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
                                        spot_id=v['id']
                                        )
            trx.append(globals()['trk_' + str(k)])

        session.add_all(trx)
        session.commit()

        return session

    def get_playlists_trx(self, spot_session, user_id):
        """Get all user playlists tracks.

        Args:
            spot_session: Object from get_user_top_trs()
            user_id: String from get_user_top_trs() dict

        Returns:
            all_tracks_ids: dictionary of tracks IDs obtained from user
            library
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

    def add_playlist(self, playlist_uri, session, user_id):
        """Add newly created playlist to DB with current user.

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


class CreatePlaylist:
    """Generate playlist of mutual interests for users."""

    def __init__(self):
        """Initiate."""
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
        """Take the top 50 tracks for 2 users and generate a playlist_uri.

        Args:
            user1_top_aud_feat: Top 50 track audio features ~dict~
            user2_top_aud_feat: Top 50 track audio features ~dict~

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
            playlist_name = f"{user_info['display_name']}'s lonely playlist"

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
