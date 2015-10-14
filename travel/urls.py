from django.conf.urls import patterns, url, include
from travel.views import *


urlpatterns = patterns('',
    url(r'^$', travel_search, name="travel_search"),
    url(r'^(?P<station_id>\w+)/$', station_info, name="line_number"),
    url(r'^guide/$', guide_list, name="guide_list"),
    url(r'^guide/(?P<guide_id>\d+)$', guide, name="guide"),
)
