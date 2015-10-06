from django.conf import settings
from django.contrib import auth
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import Context
from django.template.loader import get_template
from user.models import User


def user_info(request):
    return HttpResponse("user_info")


def status(request):
    return HttpResponse("status")


def post(request):
    return HttpResponse("post")
