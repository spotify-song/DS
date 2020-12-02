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

user_person = UserData()


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
@router.post('/add_or_update_user_data/{refresh_token,user_id}')
async def users(refresh_token, user_id):
    """Update user track and token info.

    ### Path Parameter
    'refresh_token': provide the API path paramter only the string of alphanumeric
    values, and nothing more.

    'user_id': The API requires the user_id parameter in order to obtain
    pertinant data for analysis.

    ### Response
    'NA': still undefined, but will be determined shortly
    """
    # generates spot_cc, db session, spot_session, and user Spotify_ID
    user_data = user_person.add_update_user(
                                        refresh_token=refresh_token,
                                        user_id=user_id
                                        )
    # user song library list
    user_lib_tracks = user_person.user_song_library(
                                                user_data['spot_session']
                                                )
    user_playlist_tracks = user_person.get_playlists_trx(
                                                user_data['spot_session'],
                                                user_id=user_id
                                                )
    total_tracks_list = user_lib_tracks + user_playlist_tracks

    # track features gathered
    track_features = user_person.get_audio_features(
                                                total_tracks_list,
                                                user_data['spot_session']
                                                )
    track_table_update = user_person.track_db_update(
                                                    track_features,
                                                    user_data['session']
                                                    )

    return {
            "all_user_songs": total_tracks_list,
            "Number of tracks": len(total_tracks_list),
        }


# User overall stats
@router.post('/overall_stats/{user_id}')
async def overall_stats(user_id):
    """Stats based on user's top listening history."""
    return {f"Supposed to return {user_id}'s top stats of all time."}


# generates user visuals and stats
@router.post('/user_top_track_stats/{user_id}')
async def stats(user_id):
    """Generate user statistics and visualizations."""
    return {f"{user_id}'s stats go here"}


@router.post('/users_compatability_score/{user_id_1,user_id_2}')
async def compatabilities(user_id_1, user_id_2):
    """Compatability scores are generated for 2 users given their music tastes.

    The compatabilities are generated based on the statistics from the user's
    libraries, genres and other music listening tendencies.
    """


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
