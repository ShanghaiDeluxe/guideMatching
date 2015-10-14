from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import models
from django.template.context import Context
from django.template.loader import get_template
from travel.models import DefaultStation


class MyUser(models.Model):
    user = models.ForeignKey(User, related_name="my_user")
    profile_picture = models.ImageField(max_length=1024, upload_to='static/profile/%Y/%m/%d/%h/%m/%s', blank=True)
    gender = models.CharField(max_length=10, blank=True)
    about_me = models.TextField(max_length=500, blank=True)
    cert_code = models.CharField(max_length=20, blank=True)
    is_auth = models.BooleanField(default=False, blank=False)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def send(self):
        subject = '인증번호'
        template = get_template('send_code.txt')
        context = Context({
            'name': self.user.username,
            'code': self.cert_code,
        })
        message = template.render(context)
        send_mail(
            subject, message, settings.EMAIL_HOST_USER, [self.user.email]
        )


class Language(models.Model):
    user = models.ForeignKey(User, related_name="language")
    language = models.CharField(max_length=20)
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)


class MyStation(models.Model):
    user = models.ForeignKey(User, related_name="station_user")
    station = models.ForeignKey(DefaultStation, related_name="station_station")
    extra = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
