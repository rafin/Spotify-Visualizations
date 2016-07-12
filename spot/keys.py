import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os, ast

#Spotify API keys
scope = "playlist-read-private"
uir = "http://localhost:8888"
username = ""

spotify_keys = os.environ["SPOTIFY_KEYS"]
spotify_keys = ast.literal_eval(spotify_keys)
print "IN KEYS.PY"


#set up access
def get_private_access():
  print "IN KEYS.PY"
  for key in spotify_keys:
    try:
      token = util.prompt_for_user_token(username, scope, key["uid"], key["usec"], uir)
      print "SUCCESS"
      return spotipy.Spotify(auth=token)
    except:
      print "FAILED TO LOAD"
      continue

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