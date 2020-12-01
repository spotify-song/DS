"""Model that interacts with the app generated in main."""

import logging
import random
import os
from os import getenv
from dotenv import load_dotenv

import urllib.parse
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import Dict
from sqlalchemy import create_engine


import sys
sys.path.insert(0, '../')
from api.models.my_db import User, Tokens, Tracks, UserPlaylist
from api.spotify_users import UserData, CreatePlaylist


log = logging.getLogger(__name__)


router = APIRouter()

user_dude = UserData()


class Users(BaseModel):
    """User ID."""

    user_id_1: str = Field(..., example='avargas-274')


class UserToken(BaseModel):
    """The URIs that will be generated from the analysis."""

    user_token: dict = Field(..., example={
                                        "access_token": "randome string",
                                        "token_type": "Bearear or som",
                                        "expires_in": "some time in sec",
                                        "scope": "see spotify dev site",
                                        "expires_at": "timeline",
                                        "refreh_token": "random strings again"
                                        })


# route updates user data
@router.post('/add_or_update_user_data/{token_info,user_id}')
async def users(refresh_token, user_id):
    """Update user track and token info.

    ### Path Parameter
    'token_info': provide the API path paramter only the string of alphanumeric
    values, and nothing more.

    'user_id': The API requires the user_id parameter in order to obtain
    pertinant data for analysis.

    ### Response
    'NA': still undefined, but will be determined shortly
    """
    # gather's user token and pertinant info
    token_things = user_dude.get_user_top_trx(
                                            refresh_token=refresh_token,
                                            user_id=user_id
                                            )
    artists_i_follow = token_things['spot_session'].current_user_followed_artists()
    # user song library list
    user_lib_tracks = user_dude.user_song_library(token_things['spot_session'])
    playlist_tracks = user_dude.get_playlists_trx(
                                                token_things['spot_session'],
                                                user_id=user_id
                                                )
    new_track_list = user_lib_tracks + playlist_tracks

    # track features gathered
    track_features = user_dude.get_audio_features(
                                                new_track_list,
                                                token_things['spot_session']
                                                )
    track_table_update = user_dude.add_track_aud_feat(
                                                    track_features,
                                                    token_things['session']
                                                    )

    return {
            "all_user_songs": new_track_list,
            "Number of tracks": len(new_track_list),
            }


# generates user visuals and stats
@router.post('/user_stats/{user_id}')
async def stats(user_id):
    """Generate user statistics and visualizations."""
    return {f"{user_id}'s stats go here"}


# Generates user playlist
@router.post('/uri/{playlistname}')
async def auth(playlistname):
    """Return the playlist uri generated from the given users.

    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    """
    return {"updates database with all of the user's music"}
# get token from both users to be able to access both of their libraries
