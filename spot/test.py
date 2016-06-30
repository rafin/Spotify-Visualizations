import keys # local module handling API key
import unicodedata
import datetime

from pprint import pprint

#set up access with key.py
sp = keys.get_access()
username = keys.username

playlists = sp.user_playlists(username)
pls = []
for playlist in playlists['items']:
  pname = playlist['name']
  pid = playlist['id']
  puser = playlist['owner']['id']
  pls.append([pname,pid,puser])
print pls