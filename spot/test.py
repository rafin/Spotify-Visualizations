# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# from spotipy.util import prompt_for_user_token
# import os, ast

# spotify_keys = os.environ["SPOTIFY_KEYS"]
# spotify_keys = ast.literal_eval(spotify_keys)

# CLIENT_ID = spotify_keys[0]['uid']
# CLIENT_SECRET = spotify_keys[0]['usec']
# REDIRECT_URI = 'localhost:8000'
# SCOPE = 'user-library-read'
# CACHE = '.spotipyoauthcache'

# #sp_oauth = SpotifyOAuth( CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,scope=SCOPE,cache_path=CACHE )
#     #      SpotifyOAuth( client_id,         client_secret,        redirect_uri,        scope,      cache_path       )
# token = prompt_for_user_token('rino21111',scope=SCOPE,client_id=CLIENT_ID, 
#             client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
# print(token)


import spotipy
import spotipy.util as util
import os, ast

#Spotify API keys
scope = "playlist-read-private"
uir = "http://plotify.herokuapp.com/"
username = "3"

spotify_uid = os.environ["SPOTIFY_UID"]
spotify_usec = os.environ["SPOTIFY_USEC"]
print "retrieved keys from OS"


token = util.prompt_for_user_token(username, scope, spotify_uid, spotify_usec, uir)
print token