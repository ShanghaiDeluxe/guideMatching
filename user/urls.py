from django.conf.urls import patterns, url, include
import os
from user.views import *


urlpatterns = patterns('',
    url(r'^$', user_info, name="user_info"),
    url(r'^status/$', status, name="status"),
    url(r'^status/(?P<post_id>\d+)$', post, name="post"),
)
