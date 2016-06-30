from django.http import JsonResponse
from django.shortcuts import render_to_response

#spotify tools
from spot.pl import initialize as retrieve_songs
from spot.pl import get_playlists as retrieve_playlists

import json
from json import loads as dict #converts json back to dictionary

#generate serializer for retrieving db data
from django.core import serializers
json_serializer = serializers.get_serializer("json")()

import models

def index(request):
	#return render(request, 'playlister/table.html', context)
    #playlist = models.Playlist.objects.get(title='the relaxed')
    #songs = json_serializer.serialize(playlist.songs.all(), ensure_ascii=True)
    return render_to_response('index.html')

# def index(request):
#     #return render(request, 'playlister/table.html', context)
#     playlist = models.Playlist.objects.get(title='study')
#     print playlist
#     songs = json_serializer.serialize(playlist.songs.all(), ensure_ascii=True)
#     return render_to_response('index.html', {'playlist': songs})


def graph(request):
    playlist = models.Playlist.objects.get(title='Starred')
    songs = json_serializer.serialize(playlist.songs.all(), ensure_ascii=True)
    return render_to_response('graph/graph.html', {'playlist': songs})
    #return render_to_response('graph/graph.html')

# def getsongs(request):
#     '''returns json response of given playlist title'''
#     title = request.GET.get('title', '')
#     songs = models.Playlist.objects.get(title=title).songs.all()
#     json_songs = json_serializer.serialize(songs, ensure_ascii=True)
#     return JsonResponse(dict(json_songs), safe=False )

def getsongs(request):
    '''returns json response of given playlist title'''
    title = request.GET.get('title', '')
    
    songs = retrieve_songs(title)
    print songs
    #json_songs = json_serializer.serialize(songs, ensure_ascii=True)
    return JsonResponse(songs, safe=False )

def getplaylists(request):
    '''returns json response of given playlist title'''
    #playlists = models.Playlist.objects.all()
    playlists = retrieve_playlists('rino21111')
    #json_playlists = json_serializer.serialize(playlists, ensure_ascii=True)
    return JsonResponse(playlists, safe=False )
















