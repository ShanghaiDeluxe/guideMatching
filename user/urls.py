from django.conf.urls import patterns, url, include
import os
from user.views import *


urlpatterns = patterns('',
    url(r'^$', user_info, name="user_info"),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^signup/$', signup, name="signup"),
    url(r'^lost/$', lost, name="lost"),
    url(r'^status/$', status, name="status"),
    url(r'^status/(?P<post_id>\d+)$', post, name="post"),
)
