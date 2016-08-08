from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from urllib import unquote

#spotify tools
from spot import pl
from spot import keys

import json
from json import loads as dict #converts json back to dictionary

#generate serializer for retrieving db data
from django.core import serializers
json_serializer = serializers.get_serializer("json")()

import models

def index(request):
    s_auth_url = keys.auth_url(1)
    p_auth_url = keys.auth_url(0)
    return render_to_response('index.html', {'p_auth_url': p_auth_url, 's_auth_url': s_auth_url})

def plot(request, token, username):
    return render_to_response('plot.html', {'token': token, 'name': username})

def sift(request, token, username):
    return render_to_response('sift.html', {'token': token, 'name': username})

# def index(request):
#     #return render(request, 'playlister/table.html', context)
#     playlist = models.Playlist.objects.get(title='study')
#     print playlist
#     songs = json_serializer.serialize(playlist.songs.all(), ensure_ascii=True)
#     return render_to_response('index.html', {'playlist': songs})

# def getsongs(request):
#     '''returns json response of given playlist title'''
#     title = request.GET.get('title', '')
#     songs = models.Playlist.objects.get(title=title).songs.all()
#     json_songs = json_serializer.serialize(songs, ensure_ascii=True)
#     return JsonResponse(dict(json_songs), safe=False )

def getsongs(request):
    '''returns json response of given playlist title'''
    username = request.GET.get('username', '')
    title = unquote(request.GET.get('title', ''))
    print " in views.py: title = {}, username = {}".format(title, username)
    songs = pl.pl_data(title, username)
    #json_songs = json_serializer.serialize(songs, ensure_ascii=True)
    return JsonResponse(songs, safe=False )

def getsongslite(request):
    '''returns json response of given playlist title'''
    username = request.GET.get('username', '')
    title = unquote(request.GET.get('title', ''))
    print " in views.py: title = {}, username = {}".format(title, username)
    songs = pl.pl_data_lite(title, username)
    #json_songs = json_serializer.serialize(songs, ensure_ascii=True)
    return JsonResponse(songs, safe=False )

def getplaylists(request):
    '''returns json response of given playlist title'''
    #playlists = models.Playlist.objects.all()
    username = request.GET.get('username', '')
    token = request.GET.get('token', '')
    playlists = pl.get_playlists(username, token)
    #json_playlists = json_serializer.serialize(playlists, ensure_ascii=True)
    return JsonResponse(playlists, safe=False)

def newplaylist(request):
    name = request.GET.get('name', '')
    ids = request.GET.get('songs', '')
    try:
        pl.new_playlist(name, ids)
        return JsonResponse("Success creating new playlist", safe=False)
    except:
        return JsonResponse("Failed to Create new Playlist", safe=False)

def authorize_plot(request):
    code = request.GET.get('code', '')
    token = keys.get_token(code, 0)
    #get username
    sp = keys.get_private_access(token)
    username = pl.to_ascii(sp.current_user()['id'])

    url = reverse('plot', args=(), kwargs={'token': token, 'username': username})
    print "URL IN AUTHORIZE ="
    print url
    return HttpResponseRedirect(url)

def authorize_sift(request):
    code = request.GET.get('code', '')
    token = keys.get_token(code, 1)
    #get username
    sp = keys.get_private_access(token)
    username = pl.to_ascii(sp.current_user()['id'])

    url = reverse('sift', args=(), kwargs={'token': token, 'username': username})
    print "URL IN AUTHORIZE ="
    print url
    return HttpResponseRedirect(url)














