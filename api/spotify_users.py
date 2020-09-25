# imports
import sys
import json
import random
from os import getenv

import spotipy
import numpy as np
import pandas as pd
import spotipy.util as util
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from json.decoder import JSONDecodeError
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

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

        # change for deplpoyment
        self.uri = getenv('uri')

        # Scopes: User top track; creates playlist
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

    def check_for_user(self, current_user_info, spot_cc):
        """
        Checks for user in DB.

        Input:
            - current_user_info: This object contains ID and displa_name for
              the user
            - spot_cc: Object for the spotify credentials connection

        Output:
            - : User() object from the my_db module
                 contains q.id (user id) and q.display_name (user display name)
        """
        session = self.Session()
        engine = self.engine
        Base = self.base
        current_user_info = current_user_info
        spot_cc = spot_cc

        user1 = User(
                    id=current_user_info['id'],
                    display_name=current_user_info['display_name']
                    )

        # update user and commit, then update token, and commit
        display_name_q = session.query(
                                        User
                                        ).filter(
                                                User.display_name ==
                                                user1.display_name
                                                ).first()

        # checking if user exists, if not then add user and token
        # if exists, check if token exists, if not add
        # if token exists, update using refresh_key
        if display_name_q is None:
            session.add(user1)
            session.commit()
            token = Tokens(
                        # Instead of of "user_dict['Tokens Info']"" it should
                        # be "token_info"
                        access_token=token_info['access_token'],
                        token_type=token_info['token_type'],
                        expires_in=token_info['expires_in'],
                        refresh_token=token_info['refresh_token'],
                        scope=token_info['scope'],
                        expires_at=token_info['expires_at'],
                        # Still user "user1" because the id is not changing,
                        # simply adding mans to the db
                        user_token=user1
                        )
            session.add(token)
            session.commit()
        # Else, check if user has corresponding token that is not expired
        else:
            print(f"User {user1.display_name} already exists in DataBase;\
                    checking for token")
            token_q = session.query(
                                    Tokens
                                    ).filter(
                                            Tokens.user == user1.id
                                            ).first()
            if token_q is None:
                print(f"We don't have a token for {user1.display_name},\
                        adding new token")
                token = Tokens(
                            # "token_info" to add tokens to db
                            access_token=token_info['access_token'],
                            token_type=token_info['token_type'],
                            expires_in=token_info['expires_in'],
                            refresh_token=token_info['refresh_token'],
                            scope=token_info['scope'],
                            expires_at=token_info['expires_at'],
                            # Still user "user1" because the id is not changing
                            # simply adding mans to the db
                            user_token=user1
                            )
                session.add(token)
                session.commit()
            # if the token exists refresh it, and update the value in table
            else:
                print(f"{user1.display_name} has a token, updating it")
                accs_token_refresh = spot_cc.refresh_access_token(
                                                        token_q.refresh_token
                                                        )
                token_info = spot_cc.get_access_token(as_dict=True)
                update_token = update(Tokens).where(
                                                Tokens.user == user1.id
                                                    ).values(
                                                    access_token=token_info[
                                                                'access_token'
                                                                    ],
                                                    expires_in=token_info[
                                                                'expires_in'
                                                                    ],
                                                    refresh_token=token_info[
                                                                'refresh_token'
                                                                    ],
                                                    expires_at=token_info[
                                                                'expires_at'
                                                                    ]
                                                            )
                session.execute(update_token)
                session.commit()

        return session, user1, token_info

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

    def create_playlsit(self,
                        user1_top_aud_feat,
                        user2_top_aud_feat,
                        spot_sesh,
                        current_user_info,
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
        current_user_info = current_user_info
        spot_session = spot_sesh

        if user2 is not None:
            playlist_name = f"Mine and {user2}'s playlist baby"
        else:
            playlist_name = f"{current_user_info['display_name']}'s lonely\
                            playlist"

        user1_df = pd.DataFrame(user1_top_aud_feat)
        user2_df = pd.DataFrame(user2_top_aud_feat)
        users_top_trx = pd.concat([user1_df, user2_df])
        users_top_trx = users_top_trx.drop_duplicates(
                                                    inplace=False,
                                                    subset='id'
                                                    )
        users_top_trx_id = random(sample(list(users_top_trx['id']), 5))
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
                                                    user=current_user_info[
                                                                        'id'
                                                                        ],
                                                    name=playlist_name,
                                                    public=True
                                                )
        spot_session.user_playlist_add_tracks(
                                            user=current_user_info['id'],
                                            playlist_id=playlist['id'],
                                            tracks=tracks
                                            )

        return playlist['uri']

    def user_top_50(self, user_id):
        '''
        This method will create the client credentials to query users for their
        tokens.

        Input:
            - user: Spotify username as a string of alphaneumeric characters
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
        session = self.Session()
        # disp_name_update = UpdateTables()

        # OAuth Credentials; only used when token is cached
        spot_cc = spotipy.oauth2.SpotifyOAuth(
                                            username=user_id,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            cache_path=cache_path,
                                            scope=scope,
                                            redirect_uri=uri
                                            )

        # Testing the util.prompt_for_user_token() method
        accs_token = util.prompt_for_user_token(
                                            username=user_id,
                                            client_id=client_id,
                                            client_secret=client_secret,
                                            cache_path=cache_path,
                                            scope=scope,
                                            redirect_uri=uri
                                            )

        spot_session = spotipy.Spotify(auth=accs_token)
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
        top_50_aud_feat = spot_session.audio_features(tracks=top_50_trx_ids)

        # Updates users/tokens tables
        # disp_name_update.update_users_info(
        #                         display_name=current_user_info['display_name'],
        #                         token_info=token_info,
        #                         id=current_user_info['id']
        #                         )

        return {
            'spotify connect': spot_cc,
            'Current User Info': current_user_info,
            'Tokens Info': token_info,
            f'Top Track IDs {user_id}': top_50_trx_ids,
            'Track Audio Features': top_50_aud_feat,
            'Spot Sesh': spot_session
        }
