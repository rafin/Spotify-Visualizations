from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sift/(?P<token>[-\w]+)/(?P<username>[-\w]+)$', views.sift, name='sift'),
    url(r'^plot/(?P<token>[-\w]+)/(?P<username>[-\w]+)$', views.plot, name='plot'),
	url(r'^getsongs/$', views.getsongs, name='getsongs'),
    url(r'^getsongslite/$', views.getsongslite, name='getsongslite'),
    url(r'^getplaylists/$', views.getplaylists, name='getplaylists'),
    url(r'^newplaylist/$', views.newplaylist, name='newplaylist'),
    url(r'^authorize_plot/$', views.authorize_plot, name='authorize_plot'),
    url(r'^authorize_sift/$', views.authorize_sift, name='authorize_sift')
]