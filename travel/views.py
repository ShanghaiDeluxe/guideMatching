import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, Http404
from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext
from django.template.loader import get_template
from travel.models import DefaultStation
from user.models import MyStation, MyUser


@login_required(login_url='/login/')
def travel_search(request):
    stations = DefaultStation.objects.all().order_by('line', 'station')
    context = RequestContext(request, {
        'lines': ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'B', 'S', 'A', 'G'],
        'stations': stations
    })

    return render_to_response("travel/search.html", context)


@login_required(login_url='/login/')
def station_info(request, station_id):
    users_list = []
    try:
        station = DefaultStation.objects.get(station_code=station_id)
        my_stations = MyStation.objects.filter(station=station)
    except ObjectDoesNotExist:
        raise Http404

    for my_station in my_stations:
        users_list.append([User.objects.get(id=my_station.user_id), MyUser.objects.get(id=my_station.user_id)])

    context = RequestContext(request, {
        'station': station,
        'users_list': users_list,
        'users_len': len(users_list),
    })

    return render_to_response('travel/station.html', context)


@login_required(login_url='/login/')
def guide_list(request):
    return HttpResponse("guide_list")


@login_required(login_url='/login/')
def guide(request):
    return HttpResponse("guide")
