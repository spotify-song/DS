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


class Users(BaseModel):
    """User ID."""

    user_id_1: str = Field(..., example='avargas-274')
    # user_id_2: str = Field(..., exmaple='spotify')


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


# route to get user IDs
@router.post('/users/{token_info,user_id}')
async def users(refresh_token, user_id):
    """Take token_info dict, and a user_id.

    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist
    """
    user_dude = UserData()
    token_things = user_dude.get_user_top_trx(
                                            refresh_token=refresh_token,
                                            user_id=user_id
                                            )
    return token_things['Spotify_ID']


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
