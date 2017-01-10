from unicodedata import normalize
import datetime
from operator import itemgetter
import keys # local module handling API key
import analysis

from pprint import pprint

# set up access with these global vars
sp = None


def set_access(token=None):
    global sp
    global username
    # if token == None:
    #     sp = keys.get_access()
    #     print "have public access only"
    #     return
    sp = keys.get_access(token)
    print "have private access"


def to_date(date):
    '''converts a string in any day/month/year format
        to a datetime object, defaulting to 1/1 if no
        month or day is found (year is required)
    '''
    year = int(date[0:4])
    month = day = 1
    if len(date) > 7:
        day = int(date[8:])
    if len(date) > 5:
        month = int(date[5:7])
    #return datetime.date(year, month, day)
    return year


def correct_spaces(string):
    '''removes double spaces and beginning and ending
        spaces from a string
    '''
    string = string.replace("  ", " ")
    if string[0] == " ":
        string = string[1:]
    if string[-1] == " ":
        string = string[:-1]
    return string


def feature(playlist, feature):
    '''returns comma separated list (string) of specified feature value
        in specifed playlist in order
    '''
    ids = []
    for song in playlist['songs']:
        ids.append(song[feature])
    return ids


def get_playlists(user, token=None):
    '''returns list of playlists for user as [name, id],...
        --- 1 request per 50 playlists ---
    '''
    if token != None:
        set_access(token)
    else:
        set_access()
    if(user != ""):
        playlists = []
        fifty = "start"
        start = 0
        print "user = ", user
        #to shorten delay, cap at 200 playlists
        while (fifty == "start" or len(fifty['items']) == 50) and start < 200:
                #monitor
            fifty = sp.user_playlists(user, offset=start)
                #-------#
            playlists += fifty['items']
            print u"retrieved {} playlists".format(len(playlists))
            start += 50
        pls = []
        for playlist in playlists:
            if playlist['name'] == None:
                continue
            pname = correct_spaces(playlist['name'])
            pid = playlist['id']
            puser = playlist['owner']['id']
            pls.append([pname,pid,puser])
        print "playlists successfully retrieved"
        return sorted(pls, key=lambda d: d[0].lower())
    print "username is blank"
    return "no user"


def get_songs(p_id, p_name, userid):
    '''returns songs in playlist as list of dicts
        generates data: id, name, artists, popularity,
        --- 1 request per 100 songs ---
    '''
    hundred = sp.user_playlist_tracks(userid, playlist_id=p_id)
    playlist = hundred
    start = 0
    while len(hundred['items']) >= 100:
        start += 100
        hundred = sp.user_playlist_tracks(userid, playlist_id=p_id, offset=start)
        playlist['items'] += hundred['items']
        print u"retrieved {} songs".format(len(playlist['items']))
    
    pl = {'id': p_id, 'name': p_name, 'songs': []}
    for track in playlist['items']:
        try:
            artist = track['track']['artists'][0]['name']
            artist_id = track['track']['artists'][0]['id']
            name = track['track']['name']
            s_id = track['track']['id']
            if s_id == None:
                continue
            pop = track['track']['popularity']
            if track['track']['preview_url'] != None:
                preview = track['track']['preview_url']
            else:
                preview = ""
            #cover = track['track']['album']['images'][2]['url'])
            album_id = track['track']['album']['id']
            song = {'id': s_id, 'name': name, 'artist': artist,
                    'popularity': pop, 'preview_url': preview,
                    'album_id': album_id, 'artist_id': artist_id}
            pl['songs'].append(song)
        except:
            playlist['items'].remove(track)
            print "song discarded"
    return pl


def existing_playlist(name, username, token=None):
    '''return type: Playlist with all Songs loaded
        uses the username global var
    '''
    playlists = get_playlists(username, token)
    playlist_id = user_id = None
    for playlist in playlists:
        if name == playlist[0]:
            playlist_id = playlist[1]
            user_id = playlist[2]
        if playlist_id:
            return get_songs(playlist_id, name, user_id)
    print 'ERROR: playlist name invalid'
    return ''


def clean_data(songs, l_features, afeatures):
    '''sets all class variables for the songs corresponding to each
    '''
    playlist = []
    i = 1
    for song, features, afeatures in zip(songs, l_features, afeatures):
        release_date = to_date(afeatures['release_date'])
        if features == None or afeatures == None:
            continue
        for k,v in features.iteritems():
            if v == None or v == "":
                features[k] = 0
        song['order'] = i
        song['danceability'] = round(features['danceability'] * 100, 2)
        song['energy'] = round(features['energy'] * 100, 2)
        song['loudness'] = round(features['loudness'], 1)
        song['speechiness'] = round(features['speechiness'] * 100, 2)
        song['acousticness'] = round((features['acousticness']) * 100, 2)
        song['instrumentalness'] = round(features['instrumentalness'] * 100, 2)
        song['valence'] = round(features['valence'] * 100, 2)
        song['tempo'] = round(features['tempo'], 0)
        song['duration'] = round(features['duration_ms'] / 1000, 0)
        song['release_date'] = release_date
        playlist.append(song)
        i += 1
    return playlist

def clean_data_lite(songs, l_features):
    '''sets all class variables for the songs corresponding to each
    '''
    playlist = []
    i = 1
    for song, features in zip(songs, l_features):
        if features == None:
            continue
        for k,v in features.iteritems():
            if v == None or v == "":
                features[k] = 0
        song['order'] = i
        song['danceability'] = round(features['danceability'] * 100, 2)
        song['energy'] = round(features['energy'] * 100, 2)
        song['loudness'] = round(features['loudness'], 1)
        song['speechiness'] = round(features['speechiness'] * 100, 2)
        song['acousticness'] = round((features['acousticness']) * 100, 2)
        song['instrumentalness'] = round(features['instrumentalness'] * 100, 2)
        song['valence'] = round(features['valence'] * 100, 2)
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
        print u"have {} song features to retrieve left".format(len(song_ids))
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



def get_genres(artist_ids):
    '''returns genres for input artist_ids in list of lists
        generates data: genres
        --- 1 request per 50 songs ---
    '''
    artists = []
    while(artist_ids != None):
        print len(artist_ids)
        if len(artist_ids) > 50:
            fifty = artist_ids[0:50]
            artist_ids = artist_ids[50:]
        else:
            fifty = artist_ids
            artist_ids = None
        artists += sp.artists(fifty)['artists']
    sorted_genres = {}
    genres = []
    for artist in artists:
        genres.append(artist['genres'])
        for genre in artist['genres']:
            sorted_genres[genre] = (sorted_genres.get(genre, 0) + 1)
    sorted_genres = sorted(sorted_genres.items(), key=itemgetter(1),
                         reverse=True)
    return genres, sorted_genres

def pl_data(pl_name, username, token=None):
    '''returns Dict of specified playlist with all songs and features
    '''
    playlist = existing_playlist(pl_name, username, token)
    if playlist == "":
        return ""
    features = get_song_features(feature(playlist, 'id'))
    album_features = get_album_data(feature(playlist, 'album_id'))
    #genres, sorted_genres = get_genres(feature(playlist, 'artist_id'))
    songs = clean_data(playlist['songs'], features, album_features)
    sorted_genres = []
    means = analysis.simple_stats(songs)
    #intervals = analysis.confidence_interval(songs)

    # add pca values
    pca_data = analysis.pca(songs)
    songs = analysis.merge_pca(songs, pca_data['coords'])
    # add tsne values (slow on large playlists)
    tsne_data = analysis.tSNE(songs) ## DEBUG
    songs = analysis.merge_tsne(songs, tsne_data)

    return {'sorted_genres': sorted_genres, 'songs': songs, 
            'means': means,'pcaweights': pca_data['weights']}


def new_playlist(playlist_name, ids):
    '''create playlist
    '''

    username = sp.current_user()['id']
    playlist = sp.user_playlist_create(username, playlist_name)
    pid = playlist['id']
    ids = ids.split(",")
    while(ids != None):
        print "LOOP"
        if len(ids) > 100:
            print "LOOP 1"
            hundred = ids[0:100]
            ids = ids[100:]
        else:
            print "LOOP 2"
            hundred = ids
            ids = None
        sp.user_playlist_add_tracks(username, pid, hundred)    

