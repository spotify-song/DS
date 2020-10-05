import sys
import json
import spotipy
import webbrowser
import numpy as np
import pandas as pd
from os import getenv
import spotipy.util as util
from dotenv import load_dotenv
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyClientCredentials


class UserDataFrames:
    def __init__(self, user_1='queen', user_2='spotify', top_songs=30):
        self.user_1 = user_1
        self.user_2 = user_2
        self.top_songs = top_songs
