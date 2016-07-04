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
    print "spotify_keys = {}".format(spotify_keys)
    print "spotify_keys_untouched = {}".format(os.environ["SPOTIFY_KEYS"])
    print "client_id = {}".format(spotify_keys[0]["uid"])
    print "client_secret = {}".format(spotify_keys[0]["usec"])
    print "client_id 1 = {}".format(spotify_keys[1]["uid"])
    print "client_secret 1 = {}".format(spotify_keys[1]["usec"])
    for key in spotify_keys:
        try:
            token = SpotifyClientCredentials(client_id=key["uid"], client_secret=key["usec"]).get_access_token()
            print "SUCCESS"
            return spotipy.Spotify(auth=token)
        except:
            print "FAILED TO LOAD"
            continue

# import spotipy
# import spotipy.util as util
# from spotipy.oauth2 import SpotifyClientCredentials
# import os, ast

# #Spotify API keys
# scope = "playlist-read-private"
# uir = "http://localhost:8000"
# username = ""

# spotify_uid = os.environ["SPOTIFY_UID"]
# spotify_usec = os.environ["SPOTIFY_USEC"]

# #set up access
# def get_private_access():
#     try:
#         token = util.prompt_for_user_token(username, scope, spotify_uid, spotify_usec, uir)
#         print "SUCCESS"
#         return spotipy.Spotify(auth=token)
#     except:
#         print "FAILED TO LOAD"

# def get_access():
#     print spotify_uid
#     print spotify_usec
#     token = SpotifyClientCredentials(client_id=spotify_uid, client_secret=spotify_usec).get_access_token()
#     print "SUCCESS"
#     return spotipy.Spotify(auth=token)
#     print "FAILED TO LOAD"
