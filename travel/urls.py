from django.conf.urls import patterns, url, include
from travel.views import *


urlpatterns = patterns('',
    url(r'^$', travel_search, name="travel_search"),
    url(r'^(?P<station_id>\d+)/$', guide_list, name="guide_list"),
    url(r'^(?P<station_id>\d+)/(?P<username>\w+)/$', guide, name="guide"),
    url(r'^(?P<station_id>\d+)/(?P<username>\w+)/invite_guide/$', invite_guide, name="invite"),
)
