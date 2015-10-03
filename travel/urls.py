from django.conf.urls import patterns, url, include
import os
from travel.views import *


urlpatterns = patterns('',
    url(r'^$', travel_search, name="travel_search"),
    url(r'^guide/$', guide_list, name="guide_list"),
    url(r'^guide/(?P<guide_id>\d+)$', guide, name="guide"),
)
