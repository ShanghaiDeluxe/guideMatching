from django.contrib.auth.models import User
from django.db import models


class DefaultStation(models.Model):
    station = models.CharField(max_length=20)
    station_code = models.CharField(max_length=5, unique=True)
    line = models.CharField(max_length=10)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class MatchTravel(models.Model):
    to_user = models.ForeignKey(User, related_name="matchTo", unique=False)
    from_user = models.ForeignKey(User, related_name="matchFrom", unique=False)
    to_status = models.CharField(max_length=30, default="invite")
    from_status = models.CharField(max_length=30, default="receive")
    match_station = models.ForeignKey(DefaultStation, related_name="matchTo", unique=False)
    is_active = models.BooleanField(blank=False, default=True)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class Comment(models.Model):
    content = models.TextField(max_length=500)
    when = models.OneToOneField(MatchTravel, related_name="matchForm")
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
