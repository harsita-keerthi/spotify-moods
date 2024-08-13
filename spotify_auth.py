import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, url_for

def create_spotify_auth():
    return SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="user-library-read playlist-modify-public"
    )

def get_token():
    sp_oauth = create_spotify_auth()
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return token_info

def get_spotify_client():
    token_info = get_token()
    if isinstance(token_info, dict):
        return spotipy.Spotify(auth=token_info['access_token'])