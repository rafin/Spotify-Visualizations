import keys # local module handling API key
import unicodedata
import datetime

from pprint import pprint

#from engine import models

#set up access with key.py
sp = None
username = None

def set_access():
  global sp
  sp = keys.get_access()

def to_ascii(string):
  '''converts from unicode to ascii'''
  if string == None:
    return string
  return unicodedata.normalize('NFKD', string).encode('ascii','ignore') 

def correct_spaces(string):
  string = to_ascii(string)
  string = string.replace("  ", " ")
  if string[0] == " ":
    string = string[1:]
  if string[-1] == " ":
    string = string[:-1]
  return string

def feature(playlist, feature):
  '''returns comma separated list (string) of all feature values
  in specifed playlist in order'''
  ids = []
  for song in playlist['songs']:
    ids.append(song[feature])
  return ids

def get_playlists(user):
  '''returns list of playlists for user as [name, id],... '''
  if sp == None:
    set_access()
    print "setting access"
    print sp
  if(user != ""):
    playlists = sp.user_playlists(user)
    pls = []
    for playlist in playlists['items']:
        pname = correct_spaces(playlist['name'])
        pid = to_ascii(playlist['id'])
        puser = to_ascii(playlist['owner']['id'])
        pls.append([pname,pid,puser])
    return pls
  else:
    print "error retrieving playlists"
    return "notfound"

def get_ids(pls, name):
  '''returns playlist id if input is an existing 
     playlist, otherwise returns blank string '''
  print pls
  for pl in pls:
    if name == pl[0]:
      return pl[1], pl[2] 
  return ''


def get_songs(sp, p_id, p_name, userid):
  '''returns songs in playlist (limit 100) as the Playlist Class'''
  print username
  print p_id
  hundred = sp.user_playlist_tracks(userid, playlist_id=p_id)
  #pprint(hundred)
  playlist = hundred
  start = 0
  #do one call per 100 songs in playlist
  while len(hundred['items']) >= 100:
    start += 100
    hundred = sp.user_playlist_tracks(userid, playlist_id=p_id, offset=start)
    print start
    playlist['items'] += hundred['items']

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
  '''return type: Playlist with all Songs loaded'''
  playlists = get_playlists(username)
  print name
  playlist_id, user_id = get_ids(playlists, name)
  if playlist_id:
      return get_songs(sp, playlist_id, name, user_id)
  else:
    print 'ERROR: playlist name invalid'
    return ''

def release(date):
  year = int(date[0:4])
  month = day = 1
  if len(date) > 7:
    day = int(date[8:])
  if len(date) > 5:
    month = int(date[5:7])
  return datetime.date(year, month, day)


def set_features(songs, l_features, album_features):
  '''sets all class variables for the songs corresponding to each'''
  for song, features, afeatures in zip(songs, l_features, album_features):
    release_date = release(afeatures['release_date'])
    song['danceability'] = round(features['danceability'] * 100, 2) #0:1
    song['energy'] = round(features['energy'] * 100, 2) #0:1
    song['key'] = features['key'] # 0:11
    song['loudness'] = round(features['loudness'], 1) #-60:0
    song['mode'] = features['mode'] # 0 or 1
    song['speechiness'] = round(features['speechiness'] * 100, 2) #0:1
    song['acousticness'] = round((features['acousticness']) * 100, 2) #0:1
    song['instrumentalness'] = round(features['instrumentalness'] * 100, 2) #0:1
    song['valence'] = round(features['valence'] * 100, 2) #0:1
    song['tempo'] = round(features['tempo'], 0) #40:220 (varies, tempo)
    song['duration'] = round(features['duration_ms'] / 1000, 0) #(varies)
    song['release_date'] = release_date

    #would like to get genres as well, but demands more requests

def get_features(song_ids):
  '''returns json of all song features corresponding to input ids'''
  print "Getting song features"
  features = []
  while(song_ids != None):
    print len(song_ids)
    if len(song_ids) > 100:
      hundred = song_ids[0:100]
      song_ids = song_ids[100:]
    else:
      hundred = song_ids
      song_ids = None
    features += sp.audio_features(hundred)
  return features

def get_album_features(album_ids):
  '''returns json of selected album features corresponding to input ids'''
  print "Getting album features"
  afeatures = []
  while(album_ids != None):
    print len(album_ids)
    if len(album_ids) > 20:
      fifty = album_ids[0:20]
      album_ids = album_ids[20:]
    else:
      fifty = album_ids
      album_ids = None
    afeatures += sp.albums(fifty)['albums']
  return afeatures

def initialize(pl_name, url_username):
  '''returns Dict of specified playlist with all songs and features'''
  print "Retrieved playlist data for : {}".format(pl_name)
  print "pl_name = {}, url_username = {}".format(pl_name, url_username)
  global username
  username = url_username
  if sp == None:
    set_access()
  playlist = existing_playlist(pl_name)



  features = get_features(feature(playlist, 'id'))
  album_features = get_album_features(feature(playlist, 'album_id'))
  set_features(playlist['songs'], features, album_features) #FIX
  return playlist

def store_db(pl_name):
  '''similar to initialize, but stores the data into database through models'''
  #check if pl_name already in db
  if sp == None:
    set_access()
  if models.Playlist.objects.filter(title=pl_name).count() > 0:
    print "Playlist Already in Database."
    return
  #verified that playlist isn't already stored, get it as a dict
  playlist = initialize(pl_name)
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
      s, created = models.Song.objects.get_or_create(sid=song['id'], title=song['name'],
                    artist=song['artist'], danceability=song['danceability'],
                    energy=song['energy'], key=song['key'], loudness=song['loudness'],
                    mode=song['mode'], speechiness=song['speechiness'],
                    acousticness=song['acousticness'], 
                    instrumentalness=song['instrumentalness'], valence=song['valence'],
                    tempo=song['tempo'], duration=song['duration'], popularity=song['popularity'],
                    preview_url=song['preview_url'],
                    release_date=song['release_date'])
      if not created:
        print "{}, Already in Database.".format(song['name'])
    #add song into playlist model
    p.songs.add(s)
  print "All Songs Processed"


def main():
  # getting playlist using pl.py
  if sp == None:
    set_access()
  name = raw_input('input username:\n> ')
  playlists = get_playlists(name)

    #get JSON of features for each song in playlist
    #necessary to minimize api calls
  #features = get_features(feature(playlist, 'id'))
  #album_features = get_album_features(feature(playlist, 'album_id'))

    #store features into playlist song classes
  #set_features(playlist['songs'], features, album_features) #FIX

  #Print JSON
  pprint(playlists)



if __name__ == '__main__':
  main()