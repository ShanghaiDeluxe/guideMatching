from django.db import models
from user.models import User


class MatchTravel(models.Model):
    to_email = models.ForeignKey(User, related_name="matchTo")
    from_email = models.ForeignKey(User, related_name="matchFrom")
    to_status = models.CharField(max_length=30, default="inviteTo")
    from_status = models.CharField(max_length=30, default="inviteFrom")
    match_station = models.CharField(max_length=30, default="matchStation")
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('to_email', 'from_email'), )


class DefaultStation(models.Model):
    station = models.TextField(max_length=20)
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    to_email = models.ForeignKey(User, related_name="commentTo")
    from_email = models.ForeignKey(User, related_name="commentFrom")
    content = models.TextField(max_length=500)
    when = models.ForeignKey(MatchTravel)
    extra = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('to_email', 'from_email'), )
