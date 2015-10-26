from django.conf.urls import patterns, url
from user.views import *


urlpatterns = patterns('',
    url(r'^$', user_info, name="user_info"),
    url(r'^match_list/$', match_list, name="match_list"),
    url(r'^match_list/(?P<match_id>\d+)/call_status/$', status, name="call_status"),
    url(r'^match_list/(?P<match_id>\d+)/receive_status/$', status, name="receive_status"),
    url(r'^match_list/(?P<match_id>\d+)/complete_status/$', status, name="complete_status"),

    url(r'^match_list/(?P<match_id>\d+)/call_status/cancel/$', cancel_guide, name="call_cancel"),
    url(r'^match_list/(?P<match_id>\d+)/receive_status/cancel/$', cancel_guide, name="receive_cancel"),

    url(r'^match_list/(?P<match_id>\d+)/receive_status/accept/$', accept_guide, name="receive_accept"),

    url(r'^match_list/(?P<match_id>\d+)/call_status/complete/$', complete_guide, name="call_complete"),
    url(r'^match_list/(?P<match_id>\d+)/receive_status/complete/$', complete_guide, name="receive_complete"),

    url(r'^match_list/(?P<match_id>\d+)/complete_status/review/$', review, name="review"),
)
