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

# Loading environment variables
load_dotenv()

# Connecting to Spotify API
uri = getenv('uri')
SPOTIFY_CLIENT_ID = getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET')
user1 = 'spotify'
user2 = 'queen'
scope = 'user-top-read'



