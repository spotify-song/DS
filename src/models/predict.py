import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class RecommendRequest(BaseModel):
    '''
    The user inputs their and a friend's profile name.
    '''
    user_id_1: str = Field(..., example='avargas-274')
    user_id_2: str = Field(..., example='spotify')


class RecommendItem(BaseModel):
    '''
    the playlist URI that is built based on user inputs.
    '''
    playlist_name: str = Field(..., example="User1 and User2's playlist bb")
    playlist_uri: str = Field(..., example='spotify:playlist:2J33VEAP3HnxACz0ntmKau')


class RecommendResponse(BaseModel):
    '''
    Returning playlist_uri of the playlist created, so that the user can go
    directly to it on their account.
    '''
    playlist_uri: RecommendItem = Field(..., example='spotify:playlist:2J33VEAP3HnxACz0ntmKau')


@router.post('/playlist_gen')
async def playlist_generator(user_ids: RecommendRequest,
                             playlist: RecommendItem):
    '''
    Routes for generating a playlist inside a user's spotify profile.

    ### User inputs profile names
    - 'user_id_1': String of their Spotify profile ID
    - 'user_id_2': String of second person's Spotify profile ID

    ### Response
    - 'playlist_name': This is the name of the playlist
    - 'playlist_uri': This is the link to the newly created playlist
    '''
    return {
        'playlist': [
            {
                'playlist_name': playlist.playlist_name,
                'playlist_uri': playlist.playlist_uri
            }
        ]
    }





# class User(BaseModel):
#     '''Use this data model to parse the request body JSON.'''
#
#     x1: float = Field(..., example=3.14)
#     x2: int = Field(..., example=-42)
#     x3: str = Field(..., example='banjo')
#
#     def to_df(self):
#         '''Convert pydantic object o pandas dataframe with 1 row.'''
#         return pd.DataFrame([dict(self)])
#
#     @validator('x1')
#     def x1_must_be_positive(cls, value):
#         '''Validate that x1 is a positive number.'''
#         assert value > 0, f'x1 == {value}, must be > 0'
#         return value

# @router.post('/predict')
# async def predict(user: User):
#     '''
#     Make Random baseline predictions for classification problem
#
#     ### Request body
#     - 'x1': positive float
#     - 'x2': integer
#     - 'x3': string
#
#     ### Response
#     - 'prediction': boolean, at random
#     - 'predict_proba': float between 0.5 and 1.0,
#     represeting the predicted class's probability
#
#     Replace the placeholder docstring and fake predictions with the details
#     for your own model.
#     '''
#
#     X_new = user.to_df()
#     log.info(X_new)
#     y_pred = random.choice([True, False])
#     y_pred_proba = random.random() / 2 + 0.5
#     return {
#         'prediction': y_pred,
#         'probability': y_pred_proba
#     }
