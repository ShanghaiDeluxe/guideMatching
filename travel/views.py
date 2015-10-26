import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError
from django.http.response import Http404, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.status import HTTP_400_BAD_REQUEST
from travel.models import DefaultStation, MatchTravel
from user.models import MyStation, MyUser, Language


@login_required(login_url='/login/')
def travel_search(request):
    context = RequestContext(request, {
        'lines': ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'B', 'A', 'G'],
    })

    return render_to_response("travel/search.html", context)


@login_required(login_url='/login/')
def guide_list(request, station_id):
    users_list = []

    try:
        station = DefaultStation.objects.get(station_code=station_id)
        my_stations = MyStation.objects.filter(station=station)
        for my_station in my_stations:
            user = User.objects.get(id=my_station.user_id)
            my_user = MyUser.objects.get(id=my_station.user_id)
            before_match1 = MatchTravel.objects.filter(to_user=user, from_user=request.user, is_active=0)
            before_match2 = MatchTravel.objects.filter(to_user=request.user, from_user=user, is_active=0)
            match_travels1 = MatchTravel.objects.filter(to_user=user, from_user=request.user, is_active=1)
            match_travels2 = MatchTravel.objects.filter(to_user=request.user, from_user=user, is_active=1)

            if (len(match_travels1) > 1) and (len(match_travels2) > 1 and ((len(match_travels1) + len(match_travels2)) > 1)):
                raise Exception(HTTP_400_BAD_REQUEST)

            if len(match_travels1) == 1:
                if len(match_travels2) == 0:
                    if (len(before_match1) + len(before_match2)) > 0:
                        users_list.append([user, my_user, 1, 1])
                    else:
                        users_list.append([user, my_user, 1, 0])
                else:
                    raise Exception(HTTP_400_BAD_REQUEST)

            elif len(match_travels1) == 0:
                if len(match_travels2) == 1:
                    if (len(before_match1) + len(before_match2)) > 0:
                        users_list.append([user, my_user, 1, 1])
                    else:
                        users_list.append([user, my_user, 1, 0])

                elif len(match_travels2) == 0:
                    if (len(before_match1) + len(before_match2)) > 0:
                        users_list.append([user, my_user, 0, 1])
                    else:
                        users_list.append([user, my_user, 0, 0])

                else:
                    raise Exception(HTTP_400_BAD_REQUEST)

            else:
                raise Exception(HTTP_400_BAD_REQUEST)

    except ObjectDoesNotExist:
        raise Http404

    context = RequestContext(request, {
        'station': station,
        'users_list': users_list,
        'users_len': len(users_list),
    })

    return render_to_response('travel/station.html', context)


@login_required(login_url='/login/')
def guide(request, station_id, username):
    try:
        user = User.objects.get(username=username)
        station = DefaultStation.objects.get(station_code=station_id)
        if not MyStation.objects.filter(user=user, station=station):
            raise Http404

        my_stations = MyStation.objects.filter(user=user)
        my_user = MyUser.objects.get(user=user)
        my_languages = Language.objects.filter(user=user)
        match_travels1 = MatchTravel.objects.filter(from_user=request.user, to_user=user)
        match_travels2 = MatchTravel.objects.filter(from_user=user, to_user=request.user)
    except ObjectDoesNotExist:
        raise Http404
    status = ask_status(request.user, user, match_travels1, match_travels2)

    user_list = (user, my_user)

    context = RequestContext(request, {
        'default_picture': 'static/profile/default_picture.jpg',
        'user_list': user_list,
        'status': status,
        'places': my_stations,
        'languages': my_languages,
    })
    return render_to_response('travel/user.html', context)


def ask_status(login_user, user, match_travels1, match_travels2):
    status1 = False
    status2 = False

    if login_user == user:
        return 1

    if len(match_travels1) != 0:
        if len(match_travels2) == 0:
            for match_travel in match_travels1:
                if match_travel.is_active == 1:
                    return 2
            return 0
        else:
            for match_travel in match_travels1:
                if match_travel.is_active == 1:
                    status1 = True
                    break

            for match_travel in match_travels2:
                if match_travel.is_active == 1:
                    status2 = True
                    break

            if status1 and status2:
                raise Exception(HTTP_400_BAD_REQUEST)

            elif (status1 and (not status2)) or ((not status1) and status2):
                return 2

            elif (not status1) and (not status2):
                return 0

            else:
                return -1
    else:
        if len(match_travels2) == 0:
            return 0
        else:
            for match_travel in match_travels2:
                if match_travel.is_active == 1:
                    return 2
            return 0


@login_required(login_url='/login/')
def invite_guide(request, station_id, username):
    if request.method == "POST":
        try:
            user = User.objects.get(username=username)
            station = DefaultStation.objects.get(station_code=station_id)
            many_match = MatchTravel.objects.filter(to_user=user, from_user=request.user,
                                                    match_station=station, is_active=1)
        except ObjectDoesNotExist:
            raise Http404

        if len(many_match) > 0:
            return JsonResponse({'result': '0'})

        try:
            MatchTravel.objects.create(to_user=user, from_user=request.user, match_station=station)
            return JsonResponse({'result': '1'})
        except DatabaseError as e:
            raise Exception(HTTP_400_BAD_REQUEST)
