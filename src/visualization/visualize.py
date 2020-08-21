from typing import List
from fastapi import APIRouter, HTTPException
import pandas as pd


router = APIRouter()


@router.get('/viz/{user_ids}')
async def viz(user_ids: str):
    '''
    This function will return the playlist uri generated from the given users
    ### Path Parameter
    'user_ids':  list of strings of IDs corresponding the user profiles

    ### Reponse
    URI code to navigate user to the playlist generated.
    '''
    return None
