from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^graph/$', views.graph, name='graph'),
	url(r'^getsongs/$', views.getsongs, name='getsongs'),
    url(r'^getplaylists/$', views.getplaylists, name='getplaylists')
]