import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os, ast, requests

#Spotify API keys
scope = "playlist-read-private playlist-modify-private playlist-modify-public"
#uirs = ["http://localhost:8000/authorize_plot/", "http://localhost:8000/authorize_sift/"]
uirs = ["http://plotify.herokuapp.com:8000/authorize_plot/", "http://plotify.herokuapp.com:8000/authorize_sift/"]

username = ""

spotify_keys = os.environ["SPOTIFY_KEYS"]
spotify_keys = ast.literal_eval(spotify_keys)
key = spotify_keys[0]

sp_oauth = [None, None]


def auth_url(mode):
  global sp_oauth
  sp_oauth[mode] = SpotifyOAuth(key["uid"], key["usec"], uirs[mode], scope=scope)
  auth_url = sp_oauth[mode].get_authorize_url()
  return auth_url

#set up access
def get_token(code, mode):
  token_info = sp_oauth[mode].get_access_token(code)
  if token_info:  
    return token_info['access_token']
  else:
    return None


def get_private_access(token):
  try:
    return spotipy.Spotify(auth=token)
  except:
    print "token invalid"

def get_access():
    print "at get access"
    #print "spotify_keys = {}".format(spotify_keys)
    #print "spotify_keys_untouched = {}".format(os.environ["SPOTIFY_KEYS"])
    for key in spotify_keys:
        try:
            token = SpotifyClientCredentials(client_id=key["uid"], client_secret=key["usec"]).get_access_token()
            print "SUCCESS"
            return spotipy.Spotify(auth=token)
        except:
            print "FAILED TO LOAD"
            continue

