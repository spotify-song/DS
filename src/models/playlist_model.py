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
    # user_id_2: str = Field(..., exmaple='spotify')


class UserGroup(BaseModel):
    '''collection of user ids'''
    user_ids: List[User] = Field(..., example=['user id 1', 'user id 2'])


class PlaylistURI(BaseModel):
    '''The URIs that will be generated from the analysis'''
    playlist_uri: str = Field(..., example='a long string of digits')


# route to get user IDs
@router.get('/users/{user_id_1,user_id_2}')
async def users(user_id_1: User, user_id_2: User):
    '''
    This function takes in a series of user IDs
    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist
    '''
    return {'user_ids': [user_id_1, user_id_2]}


@router.post('/uri/')
async def URI(playlist_uri: PlaylistURI):
    '''
    This function will return the playlist uri generated from the given users
    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    '''
    return {'Playlist URI': playlist_uri.playlist_uri}
# get token from both users to be able to access both of their libraries
