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
@router.get('/users/{user_id_1,user_id_2}')
async def users(user_id_1, user_id_2):
    '''
    This function takes in a series of user IDs
    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist
    '''
    user_id_1 = user_id_1
    user_id_2 = user_id_2
    user_data_1 = UserData()
    user_data_2 = UserData()
    user1 = user_data_1.user_top_50(user_id=user_id_1)
    user2 = user_data_2.user_top_50(user_id=user_id_2)
    
    session_1, user_1, token_info_1 = user1.check_for_user(
                                            current_user_info=user1['Current User Info'],
                                            spot_cc=user1['spotify connet']
                                            )
    session_2, user_2, token_info_2 = user2.check_for_user(
                                            current_user_info=user2['Current User Info'],
                                            spot_cc=user2['spotify connet']
                                            )
    playlist = CreatePlaylist()
    playlist_uri, playlist_user = playlist.create_playlist(
                                                    user1_top_aud_feat=user1['Track Audio Features'],
                                                    user2_top_aud_feat=user2['Track Audio Features'],
                                                    spot_sesh=user1['Spot Sesh'],
                                                    current_user_info=user1['Current User Info'],
                                                    user2=user_2.display_name
                                                    )
    
    
    
    return {"playlist uri": playlist_uri}


@router.post('/uri/{playlistname}')
async def auth(playlistname):
    '''
    This function will return the playlist uri generated from the given users
    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    '''
    return {'Playlist URI': playlistname}
# get token from both users to be able to access both of their libraries
