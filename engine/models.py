from __future__ import unicode_literals

from django.db import models

class Song(models.Model):
    sid = models.CharField(default='', max_length = 40)
    title = models.CharField(default='', max_length = 100)
    artist = models.CharField(default='', max_length = 100)
    danceability = models.DecimalField(max_digits=4, decimal_places=1)
    energy = models.DecimalField(max_digits=4, decimal_places=1)
    key = models.DecimalField(max_digits=2, decimal_places=0)
    loudness = models.DecimalField(max_digits=4, decimal_places=1)
    mode = models.DecimalField(max_digits=1, decimal_places=0)
    speechiness = models.DecimalField(max_digits=4, decimal_places=1)
    acousticness = models.DecimalField(max_digits=4, decimal_places=1)
    instrumentalness = models.DecimalField(max_digits=4, decimal_places=1)
    valence = models.DecimalField(max_digits=4, decimal_places=1)
    tempo = models.DecimalField(max_digits=4, decimal_places=0)
    duration = models.DecimalField(max_digits=6, decimal_places=0)
    popularity = models.DecimalField(max_digits=3, decimal_places=0)
    # new features
    preview_url = models.CharField(default='', max_length = 120)
    cover_url = models.CharField(default='', max_length = 120)
    # new album features
    release_date = models.DateField()


    def __unicode__(self):
    	return "{} - {}".format(self.title, self.artist)

    class Meta:
        ordering = ('title',)

class Playlist(models.Model):
    songs = models.ManyToManyField(Song)
    title = models.CharField(default='', max_length = 100)
    pid = models.CharField(default='', max_length = 40)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)