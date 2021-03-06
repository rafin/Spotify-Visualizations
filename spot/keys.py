import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os, ast, requests

#Spotify API keys
scope = "playlist-read-private playlist-modify-private"
#uirs = ["http://localhost:8000/authorize_plot/", "http://localhost:8000/authorize_sift/"]
uirs = ["http://plotify.herokuapp.com/authorize_plot/", "http://plotify.herokuapp.com/authorize_sift/"]

def keys():
  spotify_keys = os.environ["SPOTIFY_KEYS"]
  spotify_keys = ast.literal_eval(spotify_keys)
  return spotify_keys[0]

def auth_url(mode):
  key = keys()
  sp_oauth = SpotifyOAuth(key["uid"], key["usec"], uirs[mode], scope=scope)
  auth_url = sp_oauth.get_authorize_url()
  return auth_url

#set up access
def get_token(code, mode):
  key = keys()
  sp_oauth = SpotifyOAuth(key["uid"], key["usec"], uirs[mode], scope=scope)
  token_info = sp_oauth.get_access_token(code)
  if token_info:  
    return token_info['access_token']
  else:
    return None

def get_access(token=None):
  if token:
    print "retrieving private access"
    return spotipy.Spotify(auth=token)
    print "SUCCESS"
  else:
    print "retrieving public access"
    key = keys()
    token = SpotifyClientCredentials(client_id=key["uid"], client_secret=key["usec"]).get_access_token()
    print token
    return spotipy.Spotify(auth=token)

