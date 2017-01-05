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

from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie

def index(request):
    s_auth_url = keys.auth_url(1)
    p_auth_url = keys.auth_url(0)
    return render_to_response('index.html', {'p_auth_url': p_auth_url, 's_auth_url': s_auth_url})

def plot(request, token, username):
    return render_to_response('plot.html', {'token': token, 'name': username})

def sift(request, token, username):
    return render_to_response('sift.html', {'token': token, 'name': username})

def getsongs(request):
    '''returns json response of given playlist title'''
    username = request.GET.get('username', '')
    title = unquote(request.GET.get('title', ''))
    token = request.GET.get('token','')
    #if title is a list of titles instead of just 1
    print(title);
    if '~[' in title: 
        titles = title.split('~[')
        songs = []
        for title in titles:
            songs += pl.pl_data(title, username, token)['songs']
        songs = {"songs":songs}
    else:
        songs = pl.pl_data(title, username, token)
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
    # name = request.GET.get('name', '')
    # ids = request.GET.get('songs', '')
    # try:
    #     pl.new_playlist(name, ids)
    #     return JsonResponse("Success creating new playlist", safe=False)
    # except:
    #     return JsonResponse("Failed to Create new Playlist", safe=False)
    print "RECIEVED REQUEST: " + request.method
    if request.is_ajax():
        if request.method == 'POST':
            print 'Raw Data: {}'.format(request.body)
            title = request.POST.get("title","")
            print 'title: {}'.format(title)
            songs = request.POST.get("songs","")
            #format songs
            print songs
            songs = songs[1:-1]
            print songs
            songs = songs.replace('"', '')
            print  songs
            pl.new_playlist(title, songs)
    return JsonResponse({"success":"yes"})

def authorize_plot(request):
    code = request.GET.get('code', '')
    token = keys.get_token(code, 0)
    #get username
    sp = keys.get_access(token)
    username = sp.current_user()['id']

    url = reverse('plot', args=(), kwargs={'token': token, 'username': username})
    return HttpResponseRedirect(url)

def authorize_sift(request):
    code = request.GET.get('code', '')
    token = keys.get_token(code, 1)
    #get username
    sp = keys.get_access(token)
    username = sp.current_user()['id']

    url = reverse('sift', args=(), kwargs={'token': token, 'username': username})
    return HttpResponseRedirect(url)

