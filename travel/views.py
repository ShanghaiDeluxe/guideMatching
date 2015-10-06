from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from travel.forms import SearchForm
from user.models import MyStation


def travel_search(request):
    return HttpResponse("travel_search")


def guide_list(request):
    return HttpResponse("guide_list")


def guide(request):
    return HttpResponse("guide")
