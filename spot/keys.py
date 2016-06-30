import spotipy
import spotipy.util as util
import os, ast

#Spotify API keys
scope = "playlist-read-private"
uir = "http://localhost:8888"
username = "rino21111"

spotify_uid = os.environ["SPOTIFY_UID"]
spotify_usec = os.environ["SPOTIFY_USEC"]
print "IN KEYS.PY"
print spotify_uid
print spotify_usec



#set up access
def get_access():
    try:
      token = util.prompt_for_user_token(username, scope, spotify_uid, spotify_usec, uir)
      print "SUCCESS"
      return spotipy.Spotify(auth=token)
    except:
      print "FAILED TO LOAD"

print get_access()