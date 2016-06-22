import keys # local module handling API key
import unicodedata
import json

from engine import models


#set up access with key.py
sp = keys.get_access()
username = keys.username


def get_songids(playlist):
  '''returns comma separated list (string) of all playlist song 
  ids in order'''
  ids = []
  for song in playlist['songs']:
    ids.append(song['id'])
  return ids


#converts from unicode to ascii
def to_ascii(string):
  return unicodedata.normalize('NFKD', string).encode('ascii','ignore') 


def get_playlists(user):
  '''returns list of playlists for user as [name, id],... '''
  playlists = sp.user_playlists(user)
  pls = []
  for playlist in playlists['items']:
      pname = to_ascii(playlist['name'])
      pid = to_ascii(playlist['id'])
      pls.append([pname,pid])
  return pls

def get_id(pls, name):
  '''returns playlist id if input is an existing 
     playlist, otherwise returns blank string '''
  for pl in pls:
    if name == pl[0]:
      return pl[1] 
  return ''


def get_songs(sp, p_id, p_name):
  '''returns songs in playlist (limit 100) as the Playlist Class'''
  playlist = sp.user_playlist(username, playlist_id=p_id)
  #pl = Playlist(p_name, p_id)
  pl = {'id': p_id, 'name': p_name, 'songs': []}
  for track in playlist['tracks']['items']:
    artist = to_ascii(track['track']['artists'][0]['name'])
    name = to_ascii(track['track']['name'])
    s_id = to_ascii(track['track']['id'])
    pop = to_ascii(track['track']['popularity'])
    #song = Song(s_id, name, artist)
    song = {'id': s_id, 'name': name, 'artist': artist, 'popularity': pop}
    pl['songs'].append(song)
  return pl


def existing_playlist(name):
  '''return type: Playlist with all Songs loaded'''
  print 'getting playlists...'
  playlists = get_playlists(username)
  playlist_id = get_id(playlists, name)
  if playlist_id:
      return get_songs(sp, playlist_id, name)
  else:
    print 'ERROR: playlist name invalid'
    return ''

def set_features(songs, l_features):
  '''sets all class variables for the songs corresponding to each'''
  for song, features in zip(songs, l_features):
    song['danceability'] = features['danceability']
    song['energy'] = features['energy']
    song['key'] = features['key']
    song['loudness'] = features['loudness']
    song['mode'] = features['mode']
    song['speechiness'] = features['speechiness']
    song['acousticness'] = features['acousticness']
    song['instrumentalness'] = features['instrumentalness']
    song['valence'] = features['valence']
    song['tempo'] = features['tempo']
    song['duration'] = features['duration_ms']

    #would like to get genres as well, but demands more requests


def get_features(song_ids):
  '''returns json of all song features corresponding to input ids'''
  features = sp.audio_features(song_ids) #ERROR: only works with first 100 ids
  return features

def initialize(pl_name):
  '''returns Dict of specified playlist with all songs and features'''
  playlist = existing_playlist(pl_name)
  print "happy"
  features = get_features(get_songids(playlist))
  print "happy1"
  set_features(playlist['songs'], features)
  print "happy2"
  return playlist

def store_db(pl_name):
  playlist = initialize(pl_name)



def main():
  # getting playlist using pl.py
  name = raw_input('input playlist name:\n> ')
  playlist = existing_playlist(name)

  #get JSON of features for each song in playlist
  #necessary to minimize api calls
  features = get_features(get_songids(playlist))

  #store features into playlist song classes
  set_features(playlist['songs'], features)

  #Print JSON
  print(json.dumps(playlist))


if __name__ == '__main__':
  main()