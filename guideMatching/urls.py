"""guideMatching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from guideMatching.views import index, login, signup, lost, send_code

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={
            'next_page': '/login/',
        }
    ),
    url(r'^signup/$', signup, name="signup"),
    url(r'^lost/$', lost, name="lost"),
    url(r'^send_code/$', send_code, name="send_code"),

    url(r'^user/', include("user.urls", namespace="user")),
    url(r'^travel/', include("travel.urls", namespace="travel")),
)
