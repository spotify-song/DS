import logging
import random
import os
from os import getenv
from dotenv import load_dotenv

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import List
from sqlalchemy import create_engine


import sys
sys.path.insert(0, '../')
from api.models.my_db import *
from api.spotify_users import UserData, CreatePlaylist


log = logging.getLogger(__name__)


router = APIRouter()


class User(BaseModel):
    '''User ID'''
    user_id_1: str = Field(..., example='avargas-274')
    # user_id_2: str = Field(..., exmaple='spotify')


class UserGroup(BaseModel):
    '''collection of user ids'''
    user_ids: List[User] = Field(..., example=['user id 1', 'user id 2'])


class PlaylistURI(BaseModel):
    '''The URIs that will be generated from the analysis'''
    playlist_uri: str = Field(..., example='a long string of digits')


# route to get user IDs
@router.post('/users/{token_info,user_id}')
async def users(token_info, user_id):
    """
    This function takes in a series of user IDs
    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist
    """
    

    return {
            "this link will take all of the songs from each user and update the database"
            }


@router.post('/uri/{playlistname}')
async def auth(playlistname):
    '''
    This function will return the playlist uri generated from the given users
    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    '''
    return {"updates database with all of the user's music"}
# get token from both users to be able to access both of their libraries
