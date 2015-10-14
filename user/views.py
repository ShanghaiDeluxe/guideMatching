from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import Context, RequestContext
from django.template.loader import get_template
from travel.models import DefaultStation
from user.forms import UserInfoForm
from user.models import MyUser, MyStation


def user_info(request):
    if request.method == "POST":
        form = UserInfoForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                my_user = MyUser.objects.get(id=request.user.id)
            except ObjectDoesNotExist:
                raise Http404

            if not request.user.check_password(request.POST['password']):
                return HttpResponse("비밀번호가 틀립니다.")

            modified_place(request, form)
            my_user = modified_my_user(request, form, my_user)
            request = modified_request_user(request, form)

            if 'profile_picture' in request.FILES:
                handle_uploaded_file(request.FILES['profile_picture'], my_user.profile_picture.name)

        else:
            return HttpResponse(form.errors)
    else:
        try:
            my_user = MyUser.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise Http404

        form = UserInfoForm()

    my_stations = []
    for station in MyStation.objects.filter(user=request.user):
        my_stations.append(station)

    context = RequestContext(request, {
        'form': form,
        'profile_picture': my_user.profile_picture,
        'places': my_stations,
        'gender': my_user.gender,
        'about_me': my_user.about_me,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
    })
    context.update(csrf(request))

    return render_to_response('user/user.html', context)


def modified_place(request, form):
    if 'place' in request.POST and request.POST['place'] != '':
        MyStation.objects.filter(user=request.user).delete()
        if '0' not in form.cleaned_data['place']:
            try:
                for station_temp in form.cleaned_data.pop('place'):
                    station = DefaultStation.objects.get(station_code=station_temp)
                    MyStation.objects.create(station=station, user=request.user)
            except ObjectDoesNotExist:
                raise Http404


def modified_my_user(request, form, my_user):
    if 'picture_delete' in request.POST and request.POST['picture_delete'] == '1':
        my_user.profile_picture.delete()
    if 'profile_picture' in request.FILES:
        my_user.profile_picture = form.cleaned_data['profile_picture']
    if 'gender' in request.POST:
        my_user.gender = form.cleaned_data['gender'].strip()
    if 'about_me' in request.POST:
        my_user.about_me = form.cleaned_data['about_me'].strip()

    my_user.save()
    return my_user


def modified_request_user(request, form):
    if 'first_name' in request.POST:
        request.user.first_name = form.cleaned_data['first_name'].strip()
    if 'last_name' in request.POST:
        request.user.last_name = form.cleaned_data['last_name'].strip()
    if 'email' in request.POST:
        request.user.email = form.cleaned_data['email'].strip()

    if 'change_password_check' in request.POST and request.POST['change_password_check'] != '':
        try:
            request.user.set_password(form.cleaned_data['change_password_check'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return request
        except ObjectDoesNotExist:
            raise Http404

    request.user.save()
    return request


def handle_uploaded_file(f, name):
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def status(request):
    return HttpResponse("status")


def post(request):
    return HttpResponse("post")
