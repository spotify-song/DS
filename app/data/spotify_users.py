import json
import base64
import datetime
from os import getenv
from urllib.parse import urlencode

import requests
from dogenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET')

lib_read_scope = 'user-library-read'  # Gets user's saved tracks
user_top_scope = 'user-top-read'      # Gets user's top saved tracks/artists
pub_playlist_scope = 'playlist-modify-public'  # Creates playlist, adds items to playlist


class SpotifyUser():
    accs_token = None
    token_exp = None
    token_exp_delta = None
    refresh_accs_token = None
    spot_cc = None
    SPOTIFY_CLIENT_ID = None
    SPOTIFY_CLIENT_SECRET = None
    token_url = "https://accounts.spotify.com/api/token"
    
    
    def __init__(self, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret