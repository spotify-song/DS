import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import List
# from the users class module import users


router = APIRouter()


class User(BaseModel):
    '''User ID'''
    user_id_1: str = Field(..., example='avargas-274')
    user_id_2: str = Field(..., exmaple='spotify')

class UserGroup(BaseModel):
    '''collection of user ids'''
    user_ids: List[User] = Field(..., example=['user id 1', 'user id 2'])

class PlaylistURI(BaseModel):
    '''The URIs that will be generated from the analysis'''
    playlist_uri: str = Field(..., example='a long string of digits')

# route to get user IDs
@router.get('/users/{something else}')
async def users(playlisturi: str):
    '''
    This function takes in a series of user IDs
    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist
    '''
    return playlisturi


@router.get('/viz/{user_ids}')
async def viz(user_ids: str):
    '''
    This function will return the playlist uri generated from the given users
    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    '''
    return user_ids
# get token from both users to be able to access both of their libraries
