import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
from typing import List
# ML pkg
# import joblib
# import os

# Vectorizer
# some model
# opening file and loading it


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


# @router.get('/index')
# async def index():
#     return {'text': "hello API builders"}
#
# @router.get('/items/{name}')
# async def get_items(name):
#     return {'name': name}
#
# @router.get('predict/{name}')
# async def predict(name):
#     vectorizedd_name = 'some model'
    # return {'model prediction': model_prediction}

# route to get user IDs
@router.get('/users/{user_id_1,user_id_2}')
async def users(user_id_1, user_id_2):
    '''
    This function takes in a series of user IDs
    ### Path Parameter
    'playlist_uri':  list of strings of IDs corresponding the user profiles

    ### Response
    'playlist_uri': string of alphanumeric values that generate a playlist

    ### Pseudo Code
    if user_id 1 and 2 exist:
        Run user 1 and 2 through model
        return palylist uri
    else:
        Generate spotify token for user 1, and
        request user 1 to send link to user 2
        Generate token for user 2
        return playlist uri
    '''
    return {"user_ids": [user_id_1, user_id_2],
            "playlist_uri": f"{user_id_1} and {user_id_2}'s plylist baby"}


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
