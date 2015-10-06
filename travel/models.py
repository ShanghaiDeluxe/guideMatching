from django.contrib.auth.models import User
from django.db import models


class MatchTravel(models.Model):
    to_user = models.ForeignKey(User, related_name="matchTo")
    from_user = models.ForeignKey(User, related_name="matchFrom")
    to_status = models.CharField(max_length=30, default="inviteTo")
    from_status = models.CharField(max_length=30, default="inviteFrom")
    match_station = models.CharField(max_length=30, default="matchStation")
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('to_user', 'from_user'), )


class DefaultStation(models.Model):
    station = models.TextField(max_length=20)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class Comment(models.Model):
    to_user = models.ForeignKey(User, related_name="commentTo")
    from_user = models.ForeignKey(User, related_name="commentFrom")
    content = models.TextField(max_length=500)
    when = models.ForeignKey(MatchTravel)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        unique_together = (('to_user', 'from_user'), )
