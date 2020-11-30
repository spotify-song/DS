"""Spotify client authorizations."""

# import json
import base64
import datetime
from os import getenv
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = getenv('SPOTIFY_CLIENT_SECRET')

# Gets user's saved tracks; Creates playlist, adds items to playlist
scope = 'user-library-read user-top-read playlist-modify-public'


class SpotifyClientAuth():
    """Spot client auth class."""

    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    refresh_access_token = None
    spot_cc = None
    SPOTIFY_CLIENT_ID = None
    SPOTIFY_CLIENT_SECRET = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(
            self,
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            *args,
            **kwargs
                ):
        """Initiate class vars."""
        super().__init__(*args, **kwargs)
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET

    def get_client_credentials(self):
        """Return a base64 encoded string."""
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id is None or client_secret is None:
            raise Exception('client_id and client_secret need to be set')
        client_creds = f'{client_id}: {client_secret}'
        client_cred_b64 = base64.b64encode(client_creds.encode())
        return client_cred_b64.decode()

    def get_token_headers(self):
        """Header for credentials."""
        client_creds_b64 = self.get_client_credentials()
        return {
            'Authorization': f'Basic {client_creds_b64}'
        }

    def get_token_data(self):
        """User token info."""
        return {
            'grant_type': 'client_credentials'
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception('Could not authenticate client.')
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        return headers

    def get_features(self, song_id):
        endpoint = f'https://api.spotify.come/v1/audio-features/{song_id}'
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query, search_type='track'):
        headers = self.get_resource_header()
        endpoint = 'https://api.spotify.come/v1/search'
        data = urlencode({'q': query, 'type': search_type.lower()})
        lookup_url = f'{endpoint}?{data}'
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
