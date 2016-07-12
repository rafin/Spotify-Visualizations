from unicodedata import normalize
import datetime

import keys # local module handling API key

from pprint import pprint

#----------------------------------------------------------------------
# set up access with these global vars
sp = None
username = None

def set_access():
  global sp
  sp = keys.get_access()

#----------------------------------------------------------------------
def to_ascii(string):
  '''converts from unicode to ascii'''
  if string == None:
    return string
  return normalize('NFKD', string).encode('ascii','ignore')

def to_date(date):
  '''converts a string in any day/month/year format
     to a datetime object, defaulting to 1/1 if no
     month or day is found (year is required)'''
  year = int(date[0:4])
  month = day = 1
  if len(date) > 7:
    day = int(date[8:])
  if len(date) > 5:
    month = int(date[5:7])
  return datetime.date(year, month, day)

def correct_spaces(string):
  '''removes double spaces and beginning and ending
     spaces from a string'''
  string = to_ascii(string)
  string = string.replace("  ", " ")
  if string[0] == " ":
    string = string[1:]
  if string[-1] == " ":
    string = string[:-1]
  return string

#----------------------------------------------------------------------
def feature(playlist, feature):
  '''returns comma separated list (string) of specified feature value
     in specifed playlist in order'''
  ids = []
  for song in playlist['songs']:
    ids.append(song[feature])
  return ids

def get_playlists(user):
  '''returns list of playlists for user as [name, id],... 
     --- 1 request per 50 playlists ---
  '''
  if sp == None:
    set_access()
  if(user != ""):
    playlists = []
    fifty = "start"
    start = 0
    #to prevent overflow, cap at 200 playlists
    while (fifty == "start" or len(fifty['items']) == 50) and start < 200:
      fifty = sp.user_playlists(user, offset=start)
      playlists += fifty['items']
      print "retrieved {} playlists".format(len(playlists))
      start += 50
    pls = []
    for playlist in playlists:
        pname = correct_spaces(playlist['name'])
        pid = to_ascii(playlist['id'])
        puser = to_ascii(playlist['owner']['id'])
        pls.append([pname,pid,puser])
    print "playlists successfully retrieved"
    return sorted(pls, key=lambda d: d[0].lower())
  else:
    print "error retrieving playlists"
    return "no public playlists"

def get_songs(sp, p_id, p_name, userid):
  '''returns songs in playlist as list of dicts
     generates data: id, name, artists, popularity,
     --- 1 request per 100 songs ---
  '''
  hundred = sp.user_playlist_tracks(userid, playlist_id=p_id)
  playlist = hundred
  start = 0
  #do one call per 100 songs in playlist
  while len(hundred['items']) >= 100:
    start += 100
    hundred = sp.user_playlist_tracks(userid, playlist_id=p_id, offset=start)
    playlist['items'] += hundred['items']
    print "retrieved {} songs".format(len(playlist['items']))

  pl = {'id': p_id, 'name': p_name, 'songs': []}
  for track in playlist['items']:
    artist = to_ascii(track['track']['artists'][0]['name'])
    name = to_ascii(track['track']['name'])
    s_id = to_ascii(track['track']['id'])
    if s_id == None:
      print track
      continue
    pop = track['track']['popularity']
    if track['track']['preview_url'] != None:
      preview = to_ascii(track['track']['preview_url'])
    else:
      preview = ""
    #cover = to_ascii(track['track']['album']['images'][2]['url'])
    album_id = to_ascii(track['track']['album']['id'])
    song = {'id': s_id, 'name': name, 'artist': artist,
            'popularity': pop, 'preview_url': preview,
            'album_id': album_id}
    pl['songs'].append(song)
  return pl


def existing_playlist(name):
  '''return type: Playlist with all Songs loaded
     uses the username global var'''
  playlists = get_playlists(username)
  print name
  playlist_id = user_id = None
  for playlist in playlists:
    if name == playlist[0]:
      playlist_id = playlist[1]
      user_id = playlist[2] 
  if playlist_id:
      return get_songs(sp, playlist_id, name, user_id)
  else:
    print 'ERROR: playlist name invalid'
    return ''


def clean_data(songs, l_features, album_features):
  '''sets all class variables for the songs corresponding to each'''
  playlist = []
  i = 1
  for song, features, afeatures in zip(songs, l_features, album_features):
    release_date = to_date(afeatures['release_date'])
    for k,v in features.iteritems():
      if v == None or v == "":
        features[k] = 0
    song['order'] = i
    song['danceability'] = round(features['danceability'] * 100, 2) #0:1
    song['energy'] = round(features['energy'] * 100, 2) #0:1
    song['loudness'] = round(features['loudness'], 1) #-60:0
    song['speechiness'] = round(features['speechiness'] * 100, 2) #0:1 v
    song['acousticness'] = round((features['acousticness']) * 100, 2)
    song['instrumentalness'] = round(features['instrumentalness'] * 100, 2)
    song['valence'] = round(features['valence'] * 100, 2)
    song['tempo'] = round(features['tempo'], 0) #40:220 (varies, tempo)
    song['duration'] = round(features['duration_ms'] / 1000, 0) #(varies)
    song['release_date'] = release_date
    playlist.append(song)
    i += 1
  return playlist

def get_song_features(song_ids):
  '''returns json of all song features corresponding to input ids
     --- 1 request per 100 songs ---
  '''
  print "Getting song features"
  features = []
  while(song_ids != None):
    print "have {} song features to retrieve left".format(len(song_ids))
    if len(song_ids) > 100:
      hundred = song_ids[0:100]
      song_ids = song_ids[100:]
    else:
      hundred = song_ids
      song_ids = None
    features += sp.audio_features(hundred)
  return features

def get_album_data(album_ids):
  '''returns json of data for albums corresponding to input ids
     --- 1 request per 20 songs ---
  '''
  print "Getting album features"
  afeatures = []
  while(album_ids != None):
    print len(album_ids)
    if len(album_ids) > 20:
      twenty = album_ids[0:20]
      album_ids = album_ids[20:]
    else:
      twenty = album_ids
      album_ids = None
    afeatures += sp.albums(twenty)['albums']
  return afeatures

#----------------------------------------------------------------------
def pl_data(pl_name, url_username):
  '''returns Dict of specified playlist with all songs and features
     uses username global var'''
  print "Retrieved playlist data for : {}".format(pl_name)
  print "pl_name = {}, url_username = {}".format(pl_name, url_username)
  global username
  username = url_username
  if sp == None:
    set_access()
  playlist = existing_playlist(pl_name)
  features = get_song_features(feature(playlist, 'id'))
  album_features = get_album_data(feature(playlist, 'album_id'))
  playlist = clean_data(playlist['songs'], features, album_features)
  return playlist

#----------------------------------------------------------------------
def store_db(pl_name):
  '''similar to initialize, but stores the data into database through models'''
  if sp == None:
    set_access()
  #check if pl_name already in db
  if models.Playlist.objects.filter(title=pl_name).count() > 0:
    print "Playlist Already in Database."
    return
  #verified that playlist isn't already stored, get it as a dict
  playlist = pl_data(pl_name)
  #initialize playlist model
  p, created = models.Playlist.objects.get_or_create(title=playlist['name'], pid = playlist['id'])
  if not created:
      print "ERROR: playlist already in Database (2nd)"
      return
  #store each song
  #NOTE: double checks for duplicates, might change in future
  for song in playlist['songs']:
    if models.Song.objects.filter(sid=song['id']).count() > 0:
      print "{}, Already in Database.".format(song['name'])
      s = models.Song.objects.get(sid=song['id'])
    else:
      s, created = models.Song.objects.get_or_create(
          sid=song['id'],
          title=song['name'],
          artist=song['artist'], 
          danceability=song['danceability'],
          energy=song['energy'], 
          loudness=song['loudness'],
          speechiness=song['speechiness'], 
          acousticness=song['acousticness'], 
          instrumentalness=song['instrumentalness'], 
          valence=song['valence'],
          tempo=song['tempo'], 
          duration=song['duration'], 
          popularity=song['popularity'],
          preview_url=song['preview_url'],
          release_date=song['release_date'])
      if not created:
        print "{}, Already in Database.".format(song['name'])
    #add song into playlist model
    p.songs.add(s)
  print "All Songs Processed"

#----------------------------------------------------------------------
if __name__ == '__main__':
    # getting playlist using pl.py
  if sp == None:
    set_access()
  name = raw_input('input username:\n> ')
  playlists = get_playlists(name)

  #Print JSON
  pprint(playlists)