from django.db import models


class User(models.Model):
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    password_check = models.CharField(max_length=100, blank=False)
    profile_picture = models.ImageField(max_length=1024, upload_to='static/profile', blank=True)
    name = models.CharField(max_length=50, default="No Name", blank=True)
    sex = models.CharField(max_length=10, blank=True)
    about_me = models.TextField(max_length=500, blank=True)
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Language(models.Model):
    email = models.ForeignKey(User, related_name="language")
    language = models.CharField(max_length=20)
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MyStation(models.Model):
    email = models.ForeignKey(User, related_name="station")
    station = models.TextField(max_length=20)
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
